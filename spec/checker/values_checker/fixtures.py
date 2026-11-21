"""Runs the standard's fixtures through the checker and audits what they cover.

The fixtures are the test suite. Three audits keep them honest: every rule has an invalid
fixture, every failure the checker can report is produced by some fixture, and every
constraint in the two schemas rejects some fixture (with a valid fixture exactly at each
bound). Every valid fixture must also render to its expected wrapper and reminder.
"""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import socket
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from values_checker import marketplace, render, rules

MANIFEST = "fixtures.json"
GROUPS = ("valid", "invalid", "unsupported", "collections")
EXPECTED = "expected"

_LEAF_KEYWORDS = {
    "type", "pattern", "enum", "const", "not", "oneOf",
    "minLength", "maxLength", "minItems", "maxItems", "minimum", "maximum",
}
_BOUND_KEYWORDS = ("minLength", "maxLength", "minItems", "maxItems", "minimum", "maximum")
_NAMED_SUBSCHEMAS = ("properties", "dependentSchemas")
_SINGLE_SUBSCHEMAS = ("items", "then", "propertyNames", "additionalProperties")


def block_network() -> None:
    """Validity is decided from the files alone. Any attempt to open a socket fails the run."""

    def refuse(*args, **kwargs):
        raise RuntimeError("the checker tried to use the network")

    socket.socket = refuse


def fixture_directory(entry: dict) -> str:
    """The directory a fixture owns: its group and its own name."""
    return "/".join(entry["path"].split("/")[:2])


def constraints(schema: dict, path: tuple[str, ...] = ()) -> set[str]:
    """Every constraint in a schema, named as the path a failure of it is reported under."""
    found = set()
    for keyword, value in schema.items():
        if keyword == "required":
            found |= {"/".join(path + (keyword, name)) for name in value}
        elif keyword in _LEAF_KEYWORDS or (keyword == "additionalProperties" and value is False):
            found.add("/".join(path + (keyword,)))
        elif keyword in _NAMED_SUBSCHEMAS:
            for name, subschema in value.items():
                found |= constraints(subschema, path + (keyword, name))
        elif keyword in _SINGLE_SUBSCHEMAS:
            found |= constraints(value, path + (keyword,))
    return found


def bounds_met(schema: dict, instance, path: tuple[str, ...] = ()) -> set[str]:
    """The length, item and number bounds that this instance sits exactly on."""
    met = set()
    for keyword in _BOUND_KEYWORDS:
        if keyword not in schema:
            continue
        if keyword.endswith("Length"):
            measured = len(instance) if isinstance(instance, str) else None
        elif keyword.endswith("Items"):
            measured = len(instance) if isinstance(instance, list) else None
        else:
            measured = instance if isinstance(instance, int) and not isinstance(instance, bool) else None
        if measured == schema[keyword]:
            met.add("/".join(path + (keyword,)))
    if isinstance(instance, dict):
        named = schema.get("properties", {})
        for name, value in instance.items():
            if name in named:
                met |= bounds_met(named[name], value, path + ("properties", name))
            elif isinstance(schema.get("additionalProperties"), dict):
                met |= bounds_met(schema["additionalProperties"], value, path + ("additionalProperties",))
            if "propertyNames" in schema:
                met |= bounds_met(schema["propertyNames"], name, path + ("propertyNames",))
        for name, subschema in schema.get("dependentSchemas", {}).items():
            if name in instance:
                met |= bounds_met(subschema, instance, path + ("dependentSchemas", name))
    if isinstance(instance, list) and "items" in schema:
        for item in instance:
            met |= bounds_met(schema["items"], item, path + ("items",))
    return met


@dataclass
class _Coverage:
    rules: set[str] = field(default_factory=set)
    details: set[str] = field(default_factory=set)
    bounds: dict[str, set[str]] = field(default_factory=lambda: {"V3": set(), "V7": set()})


def _compare(label: str, report: rules.Report, expected: dict, coverage: _Coverage) -> list[str]:
    """The ways a report differs from what the manifest says it must be."""
    if report.outcome != expected["outcome"]:
        return [f"{label}: outcome is {report.outcome} {report.details}, expected {expected['outcome']}"]
    problems = []
    if report.outcome == rules.INVALID:
        if report.rules != expected["rules"]:
            problems.append(f"{label}: rules are {report.rules}, expected {expected['rules']}")
        elif report.details != sorted(expected["details"]):
            problems.append(f"{label}: details are {report.details}, expected {sorted(expected['details'])}")
        else:
            coverage.rules |= set(report.rules)
            coverage.details |= set(report.details)
    elif report.outcome == rules.VALID:
        if report.body_chars != expected["body-chars"]:
            problems.append(f"{label}: body is {report.body_chars} characters, expected {expected['body-chars']}")
        if report.core_chars != expected["core-chars"]:
            problems.append(f"{label}: core is {report.core_chars} characters, expected {expected['core-chars']}")
    return problems


def _renderings(label: str, report: rules.Report, expected_dir: Path, entry: dict) -> list[str]:
    """A valid fixture renders to exactly its expected wrapper and reminder."""
    name = report.frontmatter["name"]
    rendered = {
        "wrapper": render.wrapper(name, report.frontmatter["steward"]["name"], report.body),
        "reminder": render.reminder(name, report.core),
    }
    problems = []
    for text, made in rendered.items():
        expected_file = expected_dir / f"{text}.txt"
        if not expected_file.is_file():
            problems.append(f"{label}: valid, but has no expected rendering {EXPECTED}/{text}.txt")
        elif made.encode("utf-8") != expected_file.read_bytes():
            problems.append(f"{label}: the rendered {text} differs from {EXPECTED}/{text}.txt")
    if "wrapper-chars" in entry and len(rendered["wrapper"]) != entry["wrapper-chars"]:
        problems.append(
            f"{label}: the rendered wrapper is {len(rendered['wrapper'])} characters, expected {entry['wrapper-chars']}"
        )
    return problems


@contextlib.contextmanager
def _built(path: Path, entry: dict):
    """The fixture as it is checked. One that needs symbolic links is copied to a temporary
    directory and the links are made there, because a link committed to git does not survive
    every checkout."""
    if "symlinks" not in entry:
        yield path
        return
    with tempfile.TemporaryDirectory() as scratch:
        copy = Path(scratch) / path.name
        shutil.copytree(path, copy)
        for link, target in entry["symlinks"].items():
            os.symlink(target, copy / link)
        yield copy


def _run_package(fixtures_dir: Path, entry: dict, schemas: rules.Schemas, coverage: _Coverage) -> list[str]:
    name = entry["path"]
    path = fixtures_dir / name
    is_file = entry["scope"] == "file"
    with _built(path, entry) as built:
        report = rules.check_file(built, schemas.frontmatter) if is_file else rules.check_folder(built, schemas)
    problems = _compare(name, report, entry, coverage)
    if report.outcome == rules.VALID == entry["outcome"]:
        coverage.bounds["V3"] |= bounds_met(schemas.frontmatter, report.frontmatter)
        if not is_file and (path / rules.MCP_FILE).is_file():
            declared = json.loads((path / rules.MCP_FILE).read_text(encoding="utf-8"))
            coverage.bounds["V7"] |= bounds_met(schemas.mcp, declared)
        problems += _renderings(name, report, (path.parent if is_file else path) / EXPECTED, entry)
    return problems


def _run_collection(fixtures_dir: Path, entry: dict, schemas: rules.Schemas, coverage: _Coverage) -> list[str]:
    name = entry["path"]
    path = fixtures_dir / name
    reports = rules.check_collection(path, schemas)
    if sorted(reports) != sorted(entry["packages"]):
        return [f"{name}: the packages are {sorted(reports)}, expected {sorted(entry['packages'])}"]
    problems = []
    for package, expected in entry["packages"].items():
        problems += _compare(f"{name}/{package}", reports[package], expected, coverage)
    if all(expected["outcome"] == rules.VALID for expected in entry["packages"].values()) and not problems:
        expected_file = path.parent / EXPECTED / "marketplace.json"
        if not expected_file.is_file():
            problems.append(f"{name}: every package is valid, but there is no {EXPECTED}/marketplace.json")
        elif marketplace.entries(reports, f"./{path.name}") != json.loads(expected_file.read_text(encoding="utf-8")):
            problems.append(f"{name}: the marketplace entries differ from {EXPECTED}/marketplace.json")
    return problems


def run(fixtures_dir: Path) -> list[str]:
    """Returns every problem found. An empty list means the fixtures pass."""
    problems: list[str] = []
    schemas = rules.load_schemas()
    for text in render.TEXTS:
        try:
            render.template(text)
        except ValueError as wrong:
            problems.append(f"prompts: {wrong}")
    entries = json.loads((fixtures_dir / MANIFEST).read_text(encoding="utf-8"))["fixtures"]

    listed = set()
    coverage = _Coverage()
    for entry in entries:
        name = entry["path"]
        listed.add(fixture_directory(entry))
        path = fixtures_dir / name
        if not path.parent.is_dir() or path.name not in {child.name for child in path.parent.iterdir()}:
            problems.append(f"{name}: listed in {MANIFEST} but does not exist")
        elif entry["scope"] == "collection":
            problems += _run_collection(fixtures_dir, entry, schemas, coverage)
        else:
            problems += _run_package(fixtures_dir, entry, schemas, coverage)

    for group in GROUPS:
        for child in sorted((fixtures_dir / group).iterdir()):
            if child.is_dir() and f"{group}/{child.name}" not in listed:
                problems.append(f"{group}/{child.name}: exists but has no entry in {MANIFEST}")

    for rule in rules.RULES:
        if rule not in coverage.rules:
            problems.append(f"audit: no invalid fixture for rule {rule}")
    for code in sorted(rules.DETAIL_CODES):
        if code not in coverage.details:
            problems.append(f"audit: no fixture produces the failure {code}")
    # The frontmatter schema's own top-level `type` cannot fail under V3: frontmatter that is
    # not a mapping has already failed V2. A `.mcp.json` that is not an object does fail V7.
    audited = (("V3", schemas.frontmatter, {"type"}), ("V7", schemas.mcp, set()))
    for rule, schema, unreachable in audited:
        for constraint in sorted(constraints(schema) - unreachable):
            if f"{rule}:{constraint}" not in coverage.details:
                problems.append(f"audit: no fixture is rejected by the {rule} schema constraint {constraint}")
            if constraint.rsplit("/", 1)[-1] in _BOUND_KEYWORDS and constraint not in coverage.bounds[rule]:
                problems.append(f"audit: no valid fixture sits exactly at the {rule} bound {constraint}")
    return problems
