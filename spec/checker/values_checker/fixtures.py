"""Runs the standard's fixtures through the checker and audits what they cover.

The fixtures are the test suite. Three audits keep them honest: every rule has an invalid
fixture, every failure the checker can report is produced by some fixture, and every
constraint in the schema rejects some fixture (with a valid fixture exactly at each bound).
"""

from __future__ import annotations

import json
import socket
from pathlib import Path

from values_checker import reading, rules

MANIFEST = "fixtures.json"
GROUPS = ("valid", "invalid", "unsupported")

_CONSTRAINT_KEYWORDS = {
    "pattern", "enum", "const", "not",
    "minLength", "maxLength", "minItems", "maxItems", "minimum", "maximum",
}
_BOUND_KEYWORDS = ("minLength", "maxLength", "minItems", "maxItems", "minimum", "maximum")


def block_network() -> None:
    """Validity is decided from the files alone. Any attempt to open a socket fails the run."""

    def refuse(*args, **kwargs):
        raise RuntimeError("the checker tried to use the network")

    socket.socket = refuse


def constraints(schema: dict, path: tuple[str, ...] = ()) -> set[str]:
    """Every constraint in a schema, named as the path a failure of it is reported under."""
    found = set()
    for keyword, value in schema.items():
        if keyword == "required":
            found |= {"/".join(path + (keyword, name)) for name in value}
        elif keyword in _CONSTRAINT_KEYWORDS or (keyword == "additionalProperties" and value is False):
            found.add("/".join(path + (keyword,)))
        elif keyword == "properties":
            for name, subschema in value.items():
                found |= constraints(subschema, path + (keyword, name))
        elif keyword in ("items", "then"):
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
        for name, subschema in schema.get("properties", {}).items():
            if name in instance:
                met |= bounds_met(subschema, instance[name], path + ("properties", name))
    if isinstance(instance, list) and "items" in schema:
        for item in instance:
            met |= bounds_met(schema["items"], item, path + ("items",))
    return met


def run(fixtures_dir: Path, schema_path: Path = rules.FRONTMATTER_SCHEMA) -> list[str]:
    """Returns every problem found. An empty list means the fixtures pass."""
    problems: list[str] = []
    schema = rules.load_schema(schema_path)
    entries = json.loads((fixtures_dir / MANIFEST).read_text(encoding="utf-8"))["fixtures"]

    listed = set()
    rules_covered: set[str] = set()
    details_covered: set[str] = set()
    bounds_covered: set[str] = set()

    for entry in entries:
        name = entry["path"]
        listed.add("/".join(name.split("/")[:2]))
        path = fixtures_dir / name
        if not path.parent.is_dir() or path.name not in {child.name for child in path.parent.iterdir()}:
            problems.append(f"{name}: listed in {MANIFEST} but does not exist")
            continue
        if entry["scope"] != "file":
            problems.append(f"{name}: scope {entry['scope']!r} is not implemented")
            continue

        report = rules.check_file(path, schema)
        if report.outcome != entry["outcome"]:
            problems.append(
                f"{name}: outcome is {report.outcome} {report.details}, expected {entry['outcome']}"
            )
            continue
        if report.outcome == rules.INVALID:
            if report.rules != entry["rules"]:
                problems.append(f"{name}: rules are {report.rules}, expected {entry['rules']}")
            elif report.details != sorted(entry["details"]):
                problems.append(f"{name}: details are {report.details}, expected {sorted(entry['details'])}")
            else:
                rules_covered |= set(report.rules)
                details_covered |= set(report.details)
        elif report.outcome == rules.VALID:
            if report.body_chars != entry["body-chars"]:
                problems.append(f"{name}: body is {report.body_chars} characters, expected {entry['body-chars']}")
            if report.core_chars != entry["core-chars"]:
                problems.append(f"{name}: core is {report.core_chars} characters, expected {entry['core-chars']}")
            frontmatter = reading.parse_frontmatter(reading.split_file(path.read_bytes()).frontmatter)
            bounds_covered |= bounds_met(schema, frontmatter)

    for group in GROUPS:
        for child in sorted((fixtures_dir / group).iterdir()):
            if child.is_dir() and f"{group}/{child.name}" not in listed:
                problems.append(f"{group}/{child.name}: exists but has no entry in {MANIFEST}")

    for rule in rules.RULES:
        if rule not in rules_covered:
            problems.append(f"audit: no invalid fixture for rule {rule}")
    for code in sorted(rules.DETAIL_CODES):
        if code not in details_covered:
            problems.append(f"audit: no fixture produces the failure {code}")
    for constraint in sorted(constraints(schema)):
        if f"V3:{constraint}" not in details_covered:
            problems.append(f"audit: no fixture is rejected by the schema constraint {constraint}")
        if constraint.rsplit("/", 1)[-1] in _BOUND_KEYWORDS and constraint not in bounds_covered:
            problems.append(f"audit: no valid fixture sits exactly at the bound {constraint}")
    return problems
