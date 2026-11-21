"""Reads a VALUES.md file by the reading rules of the values.md standard, version 0.1.

Nothing here decides validity. Each function either returns what it read or raises
`Unreadable` with the detail codes that say why it could not.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError
from ruamel.yaml.events import (
    AliasEvent,
    DocumentEndEvent,
    DocumentStartEvent,
    MappingEndEvent,
    MappingStartEvent,
    ScalarEvent,
    SequenceEndEvent,
    SequenceStartEvent,
)

FRONTMATTER_LIMIT = 8000
BODY_LIMIT = 7500
CORE_LIMIT = 1500
DEFAULT_SECTION = "Core"

# The standard trims and skips these three characters and no others, so that two readers
# written in different languages agree. Carriage returns are gone before trimming happens.
WHITESPACE = " \t\n"


class Unreadable(Exception):
    """A reading rule could not be satisfied. `codes` are the checker's detail codes."""

    def __init__(self, *codes: str):
        super().__init__(", ".join(codes))
        self.codes = list(codes)


@dataclass(frozen=True)
class SplitFile:
    frontmatter: str
    body: str


def split_file(data: bytes) -> SplitFile:
    """Reading rules 1 to 3: encoding, line endings, frontmatter, body."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise Unreadable("V1:not-utf8") from None
    if text.startswith("\ufeff"):
        text = text[1:]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    if lines[0] != "---":
        raise Unreadable("V1:no-frontmatter")
    try:
        closing = lines.index("---", 1)
    except ValueError:
        raise Unreadable("V1:frontmatter-not-closed") from None
    frontmatter = "\n".join(lines[1:closing])
    if len(frontmatter) > FRONTMATTER_LIMIT:
        raise Unreadable("V1:frontmatter-too-long")
    body = "\n".join(lines[closing + 1 :]).strip(WHITESPACE)
    return SplitFile(frontmatter=frontmatter, body=body)


# YAML 1.2 core schema, section 10.3.2 of the YAML specification: how a plain scalar resolves.
_NULL = re.compile(r"null|Null|NULL|~|")  # the last alternative is the empty scalar
_BOOL = re.compile(r"true|True|TRUE|false|False|FALSE")
_INT = re.compile(r"[-+]?[0-9]+")
_INT_OCTAL = re.compile(r"0o[0-7]+")
_INT_HEX = re.compile(r"0x[0-9a-fA-F]+")
_FLOAT = re.compile(r"[-+]?(\.[0-9]+|[0-9]+(\.[0-9]*)?)([eE][-+]?[0-9]+)?")
_INFINITY = re.compile(r"[-+]?\.(inf|Inf|INF)")
_NOT_A_NUMBER = re.compile(r"\.(nan|NaN|NAN)")


def _resolve_plain_scalar(text: str):
    if _NULL.fullmatch(text):
        return None
    if _BOOL.fullmatch(text):
        return text.lower() == "true"
    if _INT.fullmatch(text):
        return int(text)
    if _INT_OCTAL.fullmatch(text):
        return int(text[2:], 8)
    if _INT_HEX.fullmatch(text):
        return int(text[2:], 16)
    if _FLOAT.fullmatch(text):
        return float(text)
    if _INFINITY.fullmatch(text):
        return -math.inf if text.startswith("-") else math.inf
    if _NOT_A_NUMBER.fullmatch(text):
        return math.nan
    return text


def parse_frontmatter(text: str, resolve_scalars: bool = True) -> dict:
    """Reading rule 2: YAML 1.2, core schema, a mapping, no duplicate keys, anchors or aliases.

    The YAML library is used only as a parser. Values are built here from its events, because
    the library's own loader resolves aliases silently, applies `<<` merge keys and turns
    date-like text into dates, none of which the core schema does.

    Three things are refused that the core schema could express but JSON cannot hold or a
    second reader might read differently: a mapping key that is not a string, an explicit
    tag, and a number that is infinite or not a number.

    With `resolve_scalars` off, every scalar is read as a string. `VALUES.md` is never read
    that way. It is how the Agent Skills reference validator reads a `SKILL.md` (rule V8).
    """
    try:
        events = list(YAML(typ="safe", pure=True).parse(text))
    except YAMLError:
        raise Unreadable("V2:not-yaml") from None

    found = []
    if any(isinstance(event, ScalarEvent | MappingStartEvent | SequenceStartEvent) and event.anchor for event in events):
        found.append("V2:anchor")
    if any(isinstance(event, AliasEvent) for event in events):
        found.append("V2:alias")
    if found:
        raise Unreadable(*found)

    documents = sum(isinstance(event, DocumentStartEvent) for event in events)
    if documents > 1:
        raise Unreadable("V2:not-yaml")
    if documents == 0:
        raise Unreadable("V2:not-a-mapping")

    stream = iter(events)
    for event in stream:
        if isinstance(event, DocumentStartEvent):
            break
    value = _build(stream, resolve_scalars)
    if not isinstance(value, dict):
        raise Unreadable("V2:not-a-mapping")
    return value


def _scalar(event: ScalarEvent, resolve: bool):
    plain_untagged, quoted_untagged = event.implicit
    if plain_untagged:
        if not resolve:
            return event.value
        value = _resolve_plain_scalar(event.value)
        if isinstance(value, float) and not math.isfinite(value):
            raise Unreadable("V2:non-finite-number")
        return value
    if quoted_untagged:
        return event.value
    raise Unreadable("V2:explicit-tag")


_AWAITING_KEY = object()


def _build(stream, resolve_scalars: bool):
    """Builds one document's value from the parser's events.

    It keeps its own stack and does not recurse, so frontmatter nested thousands of levels
    deep is read like any other and cannot exhaust the interpreter's stack.
    """
    document = []
    open_nodes: list = []  # the mappings and sequences not yet closed, innermost last
    pending_keys: list = []  # for each open node: the key whose value comes next, if any

    def place(value) -> None:
        if not open_nodes:
            document.append(value)
        elif isinstance(open_nodes[-1], list):
            open_nodes[-1].append(value)
        elif pending_keys[-1] is _AWAITING_KEY:
            if not isinstance(value, str):
                raise Unreadable("V2:key-not-string")
            if value in open_nodes[-1]:
                raise Unreadable("V2:duplicate-key")
            pending_keys[-1] = value
        else:
            open_nodes[-1][pending_keys[-1]] = value
            pending_keys[-1] = _AWAITING_KEY

    for event in stream:
        if isinstance(event, ScalarEvent):
            place(_scalar(event, resolve_scalars))
        elif isinstance(event, SequenceStartEvent | MappingStartEvent):
            if not event.implicit:
                raise Unreadable("V2:explicit-tag")
            open_nodes.append([] if isinstance(event, SequenceStartEvent) else {})
            pending_keys.append(_AWAITING_KEY)
        elif isinstance(event, SequenceEndEvent | MappingEndEvent):
            pending_keys.pop()
            place(open_nodes.pop())
        elif isinstance(event, DocumentEndEvent):
            break
    return document[0]


_FENCE_OPEN = re.compile(r" {0,3}(`{3,}|~{3,})(.*)")
_HEADING = re.compile(r"(#{1,2}) (.*)")


@dataclass(frozen=True)
class Fence:
    first: int  # the opening line
    last: int  # the closing line, or the last line when the fence is never closed
    closed: bool


def fences(lines: list[str]) -> list[Fence]:
    """The fenced code blocks among these lines (reading rule 5).

    A fence opens on a line indented by at most three spaces that starts with three or more
    backticks or tildes. A backtick fence's opening line holds no further backtick. It closes
    on the next line that holds only the same character, at least as many times, indented by
    at most three spaces, with optional trailing spaces. A fence that is never closed runs to
    the end of the body.
    """
    found = []
    first = 0
    closing = None
    for number, line in enumerate(lines):
        if closing is not None:
            if closing.fullmatch(line):
                found.append(Fence(first, number, closed=True))
                closing = None
            continue
        opening = _FENCE_OPEN.fullmatch(line)
        if opening and not (opening[1][0] == "`" and "`" in opening[2]):
            marker = opening[1]
            closing = re.compile(" {0,3}" + re.escape(marker[0]) + "{" + str(len(marker)) + ",} *")
            first = number
    if closing is not None:
        found.append(Fence(first, len(lines) - 1, closed=False))
    return found


def fenced(lines: list[str]) -> list[bool]:
    """For each line, whether it belongs to a fenced code block, its fence lines included."""
    inside = [False] * len(lines)
    for fence in fences(lines):
        inside[fence.first : fence.last + 1] = [True] * (fence.last + 1 - fence.first)
    return inside


@dataclass(frozen=True)
class Heading:
    line: int
    level: int
    text: str


def headings(body: str) -> list[Heading]:
    """Reading rules 5 and 6: first- and second-level ATX headings outside fences."""
    lines = body.split("\n")
    found = []
    for number, (line, in_fence) in enumerate(zip(lines, fenced(lines))):
        match = None if in_fence else _HEADING.fullmatch(line)
        if match:
            text = match[2].strip(WHITESPACE).rstrip("#").strip(WHITESPACE)
            found.append(Heading(line=number, level=len(match[1]), text=text))
    return found


def _lower_ascii(text: str) -> str:
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in text)


def resolve_core(body: str, section: str) -> str:
    """Reading rules 7 and 8: the core, or `Unreadable` with a V5 code.

    The section name is compared without regard to the case of the letters A to Z. Any other
    character must match exactly.
    """
    all_headings = headings(body)
    matches = [h for h in all_headings if h.level == 2 and _lower_ascii(h.text) == _lower_ascii(section)]
    if len(matches) > 1:
        raise Unreadable("V5:two-core-sections")
    if not matches:
        if len(body) > CORE_LIMIT:
            raise Unreadable("V5:no-core-section")
        return body
    start = matches[0].line
    later = [h.line for h in all_headings if h.line > start]
    lines = body.split("\n")
    core = "\n".join(lines[start + 1 : later[0] if later else len(lines)]).strip(WHITESPACE)
    if not core:
        raise Unreadable("V5:empty-core")
    if len(core) > CORE_LIMIT:
        raise Unreadable("V5:core-too-long")
    return core
