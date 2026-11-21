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

from values_checker import reading
from values_checker.reading import Unreadable

SPEC_DIR = Path(__file__).resolve().parents[2]
FRONTMATTER_SCHEMA = SPEC_DIR / "schema" / "values.schema.json"

IMPLEMENTED_VERSION = "0.1"
FILE_NAME = "VALUES.md"

VALID = "valid"
INVALID = "invalid"
UNSUPPORTED_VERSION = "unsupported-version"

RULES = ["V1", "V2", "V3", "V4", "V5", "V6"]

# Every failure the checker can report, except V3, whose details are the constraints of the
# frontmatter schema. `fixtures` requires a fixture for each one.
DETAIL_CODES = {
    "V1:file-name": "the file is not named exactly VALUES.md",
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
}

_RESERVED_TEXT = re.compile(r"<[ \t\n]*/?[ \t\n]*(values|value-system)", re.IGNORECASE)
_VERSION_FORM = re.compile(r"[0-9]+\.[0-9]+")


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
    body_chars: int | None = None
    core_chars: int | None = None

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


def load_schema(path: Path) -> dict:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def schema_failures(schema: dict, instance, rule: str) -> list[Failure]:
    """One failure per constraint of the schema that the instance breaks."""
    failures = []
    for error in SchemaValidator(schema).iter_errors(instance):
        path = "/".join(str(step) for step in error.absolute_schema_path)
        where = "/".join(str(step) for step in error.absolute_path) or "(top level)"
        if error.validator == "required":
            for name in error.validator_value:
                if name not in error.instance:
                    failures.append(Failure(f"{rule}:{path}/{name}", f"{where}: {name!r} is required"))
        else:
            failures.append(Failure(f"{rule}:{path}", f"{where}: {error.message}"))
    unique = {failure.code: failure for failure in failures}
    return [unique[code] for code in sorted(unique)]


def _failures(codes: list[str]) -> list[Failure]:
    return [Failure(code, DETAIL_CODES[code]) for code in codes]


def _core_section(frontmatter: dict) -> str | None:
    """The core section name, the default when none is given, or None when one is given and
    is not a valid value. In that last case V3 has already reported it."""
    persistence = frontmatter.get("persistence")
    reinject = persistence.get("reinject") if isinstance(persistence, dict) else None
    if not isinstance(reinject, dict) or "section" not in reinject:
        return reading.DEFAULT_SECTION
    section = reinject["section"]
    if isinstance(section, str) and 1 <= len(section) <= 100 and "\n" not in section and "\r" not in section:
        return section
    return None


def check_file(path: Path, schema: dict | None = None) -> Report:
    """Applies the file rules, V1 to V6, in the standard's order of evaluation.

    A rule that cannot be evaluated because an earlier one failed is not reported.
    """
    schema = load_schema(FRONTMATTER_SCHEMA) if schema is None else schema

    # V1. A failure ends the check: nothing else can be read.
    if path.name != FILE_NAME or path.name not in os.listdir(path.parent):
        return Report(INVALID, _failures(["V1:file-name"]))
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
        section = _core_section(frontmatter)

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
        failures.sort(key=lambda failure: (int(failure.rule[1:]), failure.code))
        return Report(INVALID, failures)
    return Report(VALID, body_chars=len(body), core_chars=len(core))
