"""The validity rules of the values.md standard, version 0.1, and the order they are applied in.

A check has three outcomes: valid, invalid (with the rules that failed), or unsupported
version. Each failure carries a detail code, `<rule>:<why>`. The rule identifiers belong to
the standard. The part after the colon is this checker's own.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError, validators

from values_checker import reading, skills
from values_checker.reading import Unreadable

SPEC_DIR = Path(__file__).resolve().parents[2]
FRONTMATTER_SCHEMA = SPEC_DIR / "schema" / "values.schema.json"
MCP_SCHEMA = SPEC_DIR / "schema" / "mcp.schema.json"

IMPLEMENTED_VERSION = "0.1"
FILE_NAME = "VALUES.md"
MCP_FILE = ".mcp.json"

VALID = "valid"
INVALID = "invalid"
UNSUPPORTED_VERSION = "unsupported-version"

RULES = ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10"]

# Every failure the checker can report, except those whose details are the constraints of a
# schema: the frontmatter schema for V3 and the `.mcp.json` schema for V7. `fixtures` requires
# a fixture for each one.
DETAIL_CODES = {
    "V1:file-name": "the file is not named exactly VALUES.md",
    "V1:no-file": "the folder holds no file named exactly VALUES.md",
    "V1:not-a-file": "VALUES.md is not a file",
    "V1:not-utf8": "the file is not UTF-8",
    "V1:no-frontmatter": "the first line is not exactly ---",
    "V1:frontmatter-not-closed": "no later line is exactly ---",
    "V1:frontmatter-too-long": f"the frontmatter is over {reading.FRONTMATTER_LIMIT:,} characters",
    "V2:not-yaml": "the frontmatter is not a single YAML document",
    "V2:not-a-mapping": "the frontmatter is not a mapping",
    "V2:duplicate-key": "a key appears twice in one mapping",
    "V2:anchor": "the frontmatter uses a YAML anchor",
    "V2:alias": "the frontmatter uses a YAML alias",
    "V2:explicit-tag": "the frontmatter uses an explicit YAML tag",
    "V2:key-not-string": "a mapping key is not a string",
    "V2:non-finite-number": "a number is infinite or not a number",
    "V4:empty-body": "the body is empty",
    "V4:body-too-long": f"the body is over {reading.BODY_LIMIT:,} characters",
    "V5:no-core-section": f"the body is over {reading.CORE_LIMIT:,} characters and has no core section",
    "V5:two-core-sections": "two headings match the core section name",
    "V5:empty-core": "the core section has no text",
    "V5:core-too-long": f"the core is over {reading.CORE_LIMIT:,} characters",
    "V6:reserved-text": "the body contains a tag that belongs to the injected prompt",
    "V7:not-json": f"{MCP_FILE} is not a file holding a JSON document in UTF-8",
    **skills.DETAIL_CODES,
    "V9:symbolic-link": "the folder contains a symbolic link",
    "V10:folder-name": "the folder is not named for the package",
    "V10:duplicate-name": "another package in the collection has the same name",
}

# Case is ignored for the letters A to Z only, as everywhere in the standard.
_RESERVED_TEXT = re.compile(r"<[ \t\n]*/?[ \t\n]*(values|value-system)", re.IGNORECASE | re.ASCII)
_VERSION_FORM = re.compile(r"[0-9]+\.[0-9]+")


class CouldNotJudge(Exception):
    """This checker could not read a package well enough to give any of the three outcomes.

    It is a limit of the checker and not a rule of the standard, so it is not a failure."""


@dataclass(frozen=True)
class Failure:
    code: str
    message: str

    @property
    def rule(self) -> str:
        return self.code.split(":", 1)[0]


@dataclass
class Report:
    outcome: str
    failures: list[Failure] = field(default_factory=list)
    spec_version: str | None = None
    frontmatter: dict | None = None  # set whenever it could be read, valid or not
    body: str | None = None  # the trimmed body and the core, set when the outcome is valid
    core: str | None = None

    @property
    def body_chars(self) -> int:
        return len(self.body)

    @property
    def core_chars(self) -> int:
        return len(self.core)

    @property
    def rules(self) -> list[str]:
        return sorted({failure.rule for failure in self.failures}, key=lambda rule: int(rule[1:]))

    @property
    def details(self) -> list[str]:
        return sorted({failure.code for failure in self.failures})


def _pattern(validator, pattern, instance, schema):
    """JSON Schema patterns are ECMA-262, where `$` matches only at the very end of the
    string. In Python it also matches before a final line feed, so it is translated."""
    if not validator.is_type(instance, "string"):
        return
    if pattern.endswith("$") and not pattern.endswith("\\$"):
        pattern = pattern[:-1] + r"\Z"
    if not re.search(pattern, instance):
        yield ValidationError(f"{instance!r} does not match {schema['pattern']!r}")


SchemaValidator = validators.extend(Draft202012Validator, {"pattern": _pattern})


def _patterns(schema) -> list[str]:
    if isinstance(schema, dict):
        own = [schema["pattern"]] if isinstance(schema.get("pattern"), str) else []
        return own + [found for value in schema.values() for found in _patterns(value)]
    if isinstance(schema, list):
        return [found for value in schema for found in _patterns(value)]
    return []


def _differs_from_ecma(pattern: str) -> str | None:
    r"""The first construct in a pattern that Python and ECMA-262 read differently, if any.

    `_pattern` translates a final `$`. Anywhere else `$` keeps Python's meaning. A `.` outside
    a character class stops at different line ends in the two dialects, and the shorthands
    `\d`, `\w`, `\s` and `\b` take in Unicode in Python and only ASCII in ECMA-262.
    """
    in_class = False
    position = 0
    while position < len(pattern):
        character = pattern[position]
        if character == "\\":
            if pattern[position + 1] in "dDwWsSbB":
                return pattern[position : position + 2]
            position += 2
            continue
        if character == "[":
            in_class = True
        elif character == "]":
            in_class = False
        elif character == "." and not in_class:
            return "."
        elif character == "$" and not in_class and position != len(pattern) - 1:
            return "$ before the end"
        position += 1
    return None


def load_schema(path: Path) -> dict:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    for pattern in _patterns(schema):
        differs = _differs_from_ecma(pattern)
        if differs:
            raise ValueError(f"{path}: the pattern {pattern!r} uses {differs}, which Python reads differently")
    return schema


@dataclass(frozen=True)
class Schemas:
    frontmatter: dict
    mcp: dict


def load_schemas() -> Schemas:
    return Schemas(frontmatter=load_schema(FRONTMATTER_SCHEMA), mcp=load_schema(MCP_SCHEMA))


# What two constraints of the `.mcp.json` schema mean, for a person reading the report.
_PLAIN_MESSAGES = {
    "V7:properties/mcpServers/additionalProperties/oneOf": "a server has url or command, never both and never neither",
    "V7:properties/mcpServers/additionalProperties/not": "headers is not allowed",
}


def schema_failures(schema: dict, instance, rule: str) -> list[Failure]:
    """One failure per constraint of the schema that the instance breaks.

    A value of the wrong type is reported once, for its type. `not` and `oneOf` say nothing
    useful about a value that is not the kind of thing they describe.
    """
    errors = list(SchemaValidator(schema).iter_errors(instance))
    wrong_type = {tuple(error.absolute_path) for error in errors if error.validator == "type"}
    failures = []
    for error in errors:
        if error.validator != "type" and tuple(error.absolute_path) in wrong_type:
            continue
        path = "/".join(str(step) for step in error.absolute_schema_path)
        where = "/".join(str(step) for step in error.absolute_path) or "(top level)"
        if error.validator == "required":
            for name in error.validator_value:
                if name not in error.instance:
                    failures.append(Failure(f"{rule}:{path}/{name}", f"{where}: {name!r} is required"))
        else:
            code = f"{rule}:{path}"
            failures.append(Failure(code, f"{where}: {_PLAIN_MESSAGES.get(code, error.message)}"))
    unique = {failure.code: failure for failure in failures}
    return [unique[code] for code in sorted(unique)]


def _failures(codes: list[str]) -> list[Failure]:
    return [Failure(code, DETAIL_CODES[code]) for code in codes]


def _core_section(frontmatter: dict, schema: dict) -> str | None:
    """The core section name, the default when none is given, or None when one is given and
    is not a valid value. In that last case V3 has already reported it."""
    persistence = frontmatter.get("persistence")
    reinject = persistence.get("reinject") if isinstance(persistence, dict) else None
    if not isinstance(reinject, dict) or "section" not in reinject:
        return reading.DEFAULT_SECTION
    section = reinject["section"]
    limits = schema["properties"]["persistence"]["properties"]["reinject"]["properties"]["section"]
    return section if SchemaValidator(limits).is_valid(section) else None


def check_file(path: Path, schema: dict | None = None) -> Report:
    """Applies the file rules, V1 to V6, in the standard's order of evaluation.

    A rule that cannot be evaluated because an earlier one failed is not reported.
    """
    schema = load_schema(FRONTMATTER_SCHEMA) if schema is None else schema

    # V1. A failure ends the check: nothing else can be read.
    if path.name != FILE_NAME:
        return Report(INVALID, _failures(["V1:file-name"]))
    if path.name not in os.listdir(path.parent):
        return Report(INVALID, _failures(["V1:no-file"]))
    if not path.is_file():  # a directory of that name, for one
        return Report(INVALID, _failures(["V1:not-a-file"]))
    try:
        split = reading.split_file(path.read_bytes())
    except Unreadable as unreadable:
        return Report(INVALID, _failures(unreadable.codes))

    failures: list[Failure] = []
    body = split.body
    section: str | None = None

    # V2. A failure skips the rules that need the frontmatter.
    try:
        frontmatter = reading.parse_frontmatter(split.frontmatter)
    except Unreadable as unreadable:
        frontmatter = None
        failures += _failures(unreadable.codes)

    if frontmatter is not None:
        # The version gate. A later version may change any rule, so nothing else is judged.
        version = frontmatter.get("spec-version")
        if isinstance(version, str) and _VERSION_FORM.fullmatch(version) and version != IMPLEMENTED_VERSION:
            return Report(UNSUPPORTED_VERSION, spec_version=version)
        # V3.
        failures += schema_failures(schema, frontmatter, "V3")
        section = _core_section(frontmatter, schema)

    # V4 and V6 need only the body.
    if not body:
        failures += _failures(["V4:empty-body"])
    elif len(body) > reading.BODY_LIMIT:
        failures += _failures(["V4:body-too-long"])
    if _RESERVED_TEXT.search(body):
        failures += _failures(["V6:reserved-text"])

    # V5, unless the body is empty or the section name could not be read.
    core = None
    if body and section is not None:
        try:
            core = reading.resolve_core(body, section)
        except Unreadable as unreadable:
            failures += _failures(unreadable.codes)

    if failures:
        return _invalid(failures, frontmatter)
    return Report(VALID, frontmatter=frontmatter, body=body, core=core)


def _invalid(failures: list[Failure], frontmatter: dict | None) -> Report:
    failures = sorted(failures, key=lambda failure: (int(failure.rule[1:]), failure.code, failure.message))
    return Report(INVALID, failures, frontmatter=frontmatter)


def _added(report: Report, failures: list[Failure]) -> Report:
    """The report with further failures. An unsupported version is never judged further."""
    if not failures or report.outcome == UNSUPPORTED_VERSION:
        return report
    return _invalid(report.failures + failures, report.frontmatter)


def _json_constant(text: str):
    raise ValueError(f"{text} is not JSON")


def _mcp_failures(folder: Path, schema: dict) -> list[Failure]:
    """V7: `.mcp.json`, if the folder has one, has the shape the standard defines.

    A `.mcp.json` that is a symbolic link is not read. V9 reports it.
    """
    path = folder / MCP_FILE
    if MCP_FILE not in os.listdir(folder) or path.is_symlink():
        return []
    if not path.is_file():  # a directory of that name, for one
        return _failures(["V7:not-json"])
    try:
        declared = json.loads(path.read_bytes().decode("utf-8"), parse_constant=_json_constant)
    except ValueError:  # covers bytes that are not UTF-8 and text that is not JSON
        return _failures(["V7:not-json"])
    except RecursionError:
        # The document may well be valid JSON, so calling it invalid would be a wrong verdict.
        raise CouldNotJudge(f"{path} is nested too deeply for this checker to read") from None
    return schema_failures(schema, declared, "V7")


def _link_failures(folder: Path) -> list[Failure]:
    """V9: nothing in the folder, at any depth, is a symbolic link."""
    links = []
    for directory, subdirectories, files in os.walk(folder):  # does not follow links
        for name in subdirectories + files:
            entry = Path(directory) / name
            if entry.is_symlink():
                links.append(entry.relative_to(folder).as_posix())
    return [Failure("V9:symbolic-link", f"{link} is a symbolic link") for link in sorted(links)]


def check_folder(folder: Path, schemas: Schemas | None = None) -> Report:
    """Applies the file rules to the folder's `VALUES.md`, then the folder rules, V7 to V9.

    V7, V8 and V9 are each judged on their own, whatever the file rules found. The one
    exception is an unsupported version, where nothing further is judged.

    Nothing is read through a symbolic link, since what it points at may lie outside the
    folder. V9 reports the link, and a rule that would need its content is not judged.
    """
    schemas = load_schemas() if schemas is None else schemas
    if (folder / FILE_NAME).is_symlink():
        report = Report(INVALID)
    else:
        report = check_file(folder / FILE_NAME, schemas.frontmatter)
    if report.outcome == UNSUPPORTED_VERSION:
        return report
    failures = _mcp_failures(folder, schemas.mcp)
    failures += [Failure(code, f"{where}: {DETAIL_CODES[code]}") for code, where in skills.check(folder)]
    failures += _link_failures(folder)
    return _added(report, failures)


def check_collection(directory: Path, schemas: Schemas | None = None) -> dict[str, Report]:
    """Checks every folder in a collection as a package and applies V10. Returns a report for
    each folder, by folder name.

    V10 is judged when the package's `name` could be read as a string. A package of an
    unsupported version takes no part in it.

    A package folder that is itself a symbolic link breaks V9 and is not read, because what
    it points at lies outside the collection. Anything in the collection that is not a
    folder is ignored, a link to a file and a link to nothing included.
    """
    schemas = load_schemas() if schemas is None else schemas
    reports = {}
    for folder in sorted(child for child in directory.iterdir() if child.is_dir()):
        if folder.is_symlink():
            linked = Failure("V9:symbolic-link", "the package folder is itself a symbolic link, so it was not read")
            reports[folder.name] = _invalid([linked], None)
        else:
            reports[folder.name] = check_folder(folder, schemas)

    names = {}
    for folder_name, report in reports.items():
        name = report.frontmatter.get("name") if report.frontmatter is not None else None
        if report.outcome != UNSUPPORTED_VERSION and isinstance(name, str):
            names[folder_name] = name
    for folder_name, name in names.items():
        codes = []
        if name != folder_name:
            codes.append("V10:folder-name")
        if sum(other == name for other in names.values()) > 1:
            codes.append("V10:duplicate-name")
        reports[folder_name] = _added(reports[folder_name], _failures(codes))
    return reports
