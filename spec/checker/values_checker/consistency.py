"""Checks the documents under `spec/` against the machine-readable parts of the standard.

The documents are the Markdown files under `spec/`, outside `fixtures/` and `checker/`. They
carry markers, each an HTML comment alone on its line, outside any fenced code block:

    <!-- values-md:field-table -->     before the table of frontmatter fields
    <!-- values-md:rule-table -->      before the table of validity rules
    <!-- values-md:smallest-file -->   before the fenced block showing the smallest valid file
    <!-- values-md:rendering PATH -->  before a fenced block that must equal the file at PATH,
                                       an expected rendering, given from `fixtures/`

Four things are checked:

1. The field table against the frontmatter schema, in both directions. Each field's row must
   say whether it is required and give its type and limits in exactly the words `field_rows`
   makes from the schema.
2. Every fenced block that opens with a tag of the injected prompt. It is identical to its file
   in `prompts/`, or it is marked as a rendering and identical to the file the marker names.
3. The smallest file shown against `values/plain-speaking/VALUES.md`.
4. The rule table against the rules the checker implements, by identifier.

The first three markers appear exactly once each, in `specification.md`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from values_checker import reading, render, rules

SPECIFICATION = "specification.md"
NOT_DOCUMENTS = ("fixtures", "checker")
SMALLEST_FILE = "plain-speaking/VALUES.md"

FIELD_TABLE = "field-table"
RULE_TABLE = "rule-table"
SMALLEST = "smallest-file"
RENDERING = "rendering"
ONCE = (FIELD_TABLE, RULE_TABLE, SMALLEST)

_MARKER = re.compile(r"<!-- values-md:([a-z-]+)(?: ([^ ]+))? -->")
_MARKER_PREFIX = "<!-- values-md:"

# The words the field table uses for each pattern in the frontmatter schema. A pattern that
# is not here has no words, and the check stops: the table cannot describe it.
FORMS = {
    r"^[a-z0-9]+(-[a-z0-9]+)*$": "in name form",
    r'^[^<>"\r\n]*$': 'on one line without `<`, `>` or `"`',
    r"^[^\r\n]*$": "on one line",
    r"^https://[A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?(\.[A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?)*"
    r"(:[0-9]{1,5})?([/?#][A-Za-z0-9._~:/?#\[\]@!\$&'()*+,;=%-]*)?$": "in the form of an `https` URL",
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(-((0|[1-9][0-9]*|[0-9]*[a-zA-Z-][0-9a-zA-Z-]*)(\.(0|[1-9][0-9]*|[0-9]*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(\+([0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*))?$": "in Semantic Versioning 2.0.0 form",
    r"^[0-9]+\.[0-9]+$": "in the form of two numbers joined by a dot",
    r"^(([A-Za-z]{2,3}(-[A-Za-z]{3}){0,3}|[A-Za-z]{4,8})(-[A-Za-z]{4})?(-([A-Za-z]{2}|[0-9]{3}))?"
    r"(-([A-Za-z0-9]{5,8}|[0-9][A-Za-z0-9]{3}))*(-[0-9A-WY-Za-wy-z](-[A-Za-z0-9]{2,8})+)*"
    r"(-[xX](-[A-Za-z0-9]{1,8})+)?|[xX](-[A-Za-z0-9]{1,8})+|[eE][nN]-[gG][bB]-[oO][eE][dD]"
    r"|[iI]-[aA][mM][iI]|[iI]-[bB][nN][nN]|[iI]-[dD][eE][fF][aA][uU][lL][tT]"
    r"|[iI]-[eE][nN][oO][cC][hH][iI][aA][nN]|[iI]-[hH][aA][kK]|[iI]-[kK][lL][iI][nN][gG][oO][nN]"
    r"|[iI]-[lL][uU][xX]|[iI]-[mM][iI][nN][gG][oO]|[iI]-[nN][aA][vV][aA][jJ][oO]|[iI]-[pP][wW][nN]"
    r"|[iI]-[tT][aA][oO]|[iI]-[tT][aA][yY]|[iI]-[tT][sS][uU]|[sS][gG][nN]-[bB][eE]-[fF][rR]"
    r"|[sS][gG][nN]-[bB][eE]-[nN][lL]|[sS][gG][nN]-[cC][hH]-[dD][eE])$": "in the form of a BCP 47 language tag",
}

_ANNOTATIONS = {"$schema", "$id", "title", "description"}
_STRUCTURE = {"type", "properties", "required", "additionalProperties", "if", "then", "items"}
_WORDED = {"pattern", "enum", "minLength", "maxLength", "minItems", "maxItems", "minimum", "maximum"}


def _range(node: dict, lowest: str, highest: str, unit: str) -> str:
    """`1 to 20 items`, `at most 64 characters`, or nothing when the node sets no bound."""
    low, high = node.get(lowest), node.get(highest)
    if low is None and high is None:
        return ""
    if high is None:
        raise ValueError(f"the field table has no words for {lowest} without {highest}")
    return f"at most {high:,} {unit}" if low is None else f"{low:,} to {high:,} {unit}"


def _limits(node: dict, as_item: bool = False) -> str:
    """The type and limits of one schema node, in the field table's words."""
    unknown = set(node) - _ANNOTATIONS - _STRUCTURE - _WORDED
    if unknown:
        raise ValueError(f"the field table has no words for the schema keyword(s) {sorted(unknown)}")
    if "enum" in node:
        return ("one of " if as_item else "One of ") + ", ".join(f"`{value}`" for value in node["enum"])
    kind = node["type"]
    if kind == "string":
        said = "a string" if as_item else "String"
        size = _range(node, "minLength", "maxLength", "characters")
        if size:
            said += f" of {size}"
        if "pattern" in node:
            if node["pattern"] not in FORMS:
                raise ValueError(f"the field table has no words for the pattern {node['pattern']!r}")
            said += ("," if size else "") + f" {FORMS[node['pattern']]}"
        return said
    if kind == "integer":
        if "minimum" not in node or "maximum" not in node:
            raise ValueError("the field table has no words for an integer without both bounds")
        return ("an integer" if as_item else "Integer") + f" from {node['minimum']:,} to {node['maximum']:,}"
    if kind == "array":
        size = _range(node, "minItems", "maxItems", "items")
        if not size:
            raise ValueError("the field table has no words for a list of any size")
        return f"List of {size}, each {_limits(node['items'], as_item=True)}"
    if kind == "object":
        said = "an object" if as_item else "Object"
        if node.get("additionalProperties") is False:
            return f"{said} with no other keys"
        if "properties" not in node and "additionalProperties" not in node:
            return f"{said} with any keys and any JSON values"
    raise ValueError(f"the field table has no words for this part of the schema: {node!r}")


def _conditions(node: dict) -> dict[str, str]:
    """For each property an `if`/`then` pair makes required, when it is required."""
    if "if" not in node and "then" not in node:
        return {}
    condition, then = node.get("if", {}), node.get("then", {})
    keys = condition.get("required", [])
    values = condition.get("properties", {}).get(keys[0] if keys else None, {}).get("enum")
    understood = (
        len(keys) == 1
        and set(condition) == {"required", "properties"}
        and set(condition["properties"]) == set(keys)
        and values
        and set(then) == {"required"}
    )
    if not understood:
        raise ValueError(f"the field table has no words for this condition: {condition!r} then {then!r}")
    when = f"When `{keys[0]}` is " + " or ".join(f"`{value}`" for value in values)
    return {name: when for name in then["required"]}


def field_rows(schema: dict) -> dict[str, tuple[str, str]]:
    """What the field table must say: for each field, whether it is required, and its type and
    limits. A field inside an object is named with a dot, and inside a list's items with `[]`."""
    rows: dict[str, tuple[str, str]] = {}

    def add(node: dict, prefix: str) -> None:
        required = set(node.get("required", []))
        conditions = _conditions(node)
        for name, field in node["properties"].items():
            path = prefix + name
            rows[path] = (conditions.get(name) or ("Yes" if name in required else "No"), _limits(field))
            if "properties" in field:
                add(field, path + ".")
            elif "properties" in field.get("items", {}):
                add(field["items"], path + "[].")

    add(schema, "")
    return rows


@dataclass(frozen=True)
class Marker:
    document: str
    line: int  # where the marker is, counted from 1
    kind: str
    argument: str | None
    target: int | None  # the index of the next line that is not blank, if there is one

    @property
    def where(self) -> str:
        return f"{self.document}, line {self.line}"


@dataclass(frozen=True)
class Block:
    document: str
    line: int  # where the opening fence is, counted from 1
    content: str  # the lines between the fences, each ended by a line feed

    @property
    def where(self) -> str:
        return f"{self.document}, line {self.line}"


def documents(spec_dir: Path) -> dict[str, str]:
    """The text of every document under `spec/`, by its path from there."""
    found = {}
    for path in sorted(spec_dir.rglob("*.md")):
        relative = path.relative_to(spec_dir)
        if relative.parts[0] not in NOT_DOCUMENTS and path.is_file():
            found[relative.as_posix()] = path.read_bytes().decode("utf-8")
    return found


def _read(document: str, text: str) -> tuple[list[str], list[Marker], dict[int, Block], list[str]]:
    """A document's lines, its markers, its fenced blocks by the index of their opening line,
    and anything wrong with how it is marked."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    problems = []
    blocks = {}
    inside = [False] * len(lines)
    for fence in reading.fences(lines):
        inside[fence.first : fence.last + 1] = [True] * (fence.last + 1 - fence.first)
        if not fence.closed:
            problems.append(f"{document}, line {fence.first + 1}: this fenced block is never closed")
            continue
        content = "".join(line + "\n" for line in lines[fence.first + 1 : fence.last])
        blocks[fence.first] = Block(document, fence.first + 1, content)

    markers = []
    for number, line in enumerate(lines):
        if inside[number] or _MARKER_PREFIX not in line:
            continue
        match = _MARKER.fullmatch(line)
        if not match:
            problems.append(f"{document}, line {number + 1}: a marker is alone on its line and has the form '<!-- values-md:kind -->'")
            continue
        target = next((later for later in range(number + 1, len(lines)) if lines[later].strip()), None)
        markers.append(Marker(document, number + 1, match[1], match[2], target))
    return lines, markers, blocks, problems


def _table(lines: list[str], start: int | None) -> list[list[str]] | None:
    """The rows of the table that starts at this line, without its two heading lines. None
    when no table starts there."""
    rows = []
    for line in lines[start:] if start is not None else []:
        if not (line.startswith("|") and line.rstrip().endswith("|")):
            break
        rows.append([cell.strip() for cell in line.rstrip()[1:-1].split("|")])
    if len(rows) < 2 or any(set(cell) - set("-: ") for cell in rows[1]):
        return None
    return rows[2:]


def _field_table_problems(where: str, rows: list[list[str]], schema: dict) -> list[str]:
    expected = field_rows(schema)
    problems = []
    seen = set()
    for row in rows:
        field = row[0].strip("`")
        if len(row) < 3 or row[0] != f"`{field}`":
            problems.append(f"{where}: the field table row {row!r} does not begin with a field in backticks, whether it is required, and its type and limits")
        elif field in seen:
            problems.append(f"{where}: the field table has two rows for `{field}`")
        elif field not in expected:
            problems.append(f"{where}: the field table has a row for `{field}`, which the schema does not define")
        else:
            required, limits = expected[field]
            if row[1] != required:
                problems.append(f"{where}: `{field}` is given as required {row[1]!r}, and the schema says {required!r}")
            if row[2] != limits:
                problems.append(f"{where}: `{field}` is given as {row[2]!r}, and the schema says {limits!r}")
        seen.add(field)
    for field in expected:
        if field not in seen:
            problems.append(f"{where}: the field table has no row for `{field}`, which the schema defines")
    return problems


def _normative_text(block: Block) -> str | None:
    """Which of the three normative texts a block opens with the tag of, if any."""
    if block.content.startswith("<value-systems>"):
        return "preamble"
    if block.content.startswith("<value-system-reminder"):
        return "reminder"
    if block.content.startswith("<value-system"):
        return "wrapper"
    return None


def check(texts: dict[str, str], spec_dir: Path = rules.SPEC_DIR) -> list[str]:
    """Returns every disagreement found. An empty list means the documents agree with the
    schema, the prompt files, the fixtures and the smallest example."""
    schema = rules.load_schema(spec_dir / "schema" / "values.schema.json")
    fixtures_dir = spec_dir / "fixtures"
    problems: list[str] = []
    lines_of: dict[str, list[str]] = {}
    markers: list[Marker] = []
    blocks: dict[tuple[str, int], Block] = {}
    for document, text in texts.items():
        lines_of[document], found, document_blocks, wrong = _read(document, text)
        markers += found
        blocks.update({(document, first): block for first, block in document_blocks.items()})
        problems += wrong

    for kind in ONCE:
        of_kind = [marker for marker in markers if marker.kind == kind]
        if not of_kind:
            problems.append(f"the marker values-md:{kind} is missing. It appears once, in {SPECIFICATION}")
        elif len(of_kind) > 1:
            places = "; ".join(marker.where for marker in of_kind)
            problems.append(f"the marker values-md:{kind} appears {len(of_kind)} times ({places}). It appears once")
        elif of_kind[0].document != SPECIFICATION:
            problems.append(f"{of_kind[0].where}: the marker values-md:{kind} belongs in {SPECIFICATION}")

    rendered = set()
    for marker in markers:
        block = blocks.get((marker.document, marker.target))
        if marker.kind not in (*ONCE, RENDERING):
            problems.append(f"{marker.where}: values-md:{marker.kind} is not a marker this check knows")
        elif (marker.argument is None) == (marker.kind == RENDERING):
            problems.append(f"{marker.where}: values-md:{RENDERING} names a file, and the other markers name nothing")
        elif marker.kind in (FIELD_TABLE, RULE_TABLE):
            rows = _table(lines_of[marker.document], marker.target)
            if rows is None:
                problems.append(f"{marker.where}: values-md:{marker.kind} is not followed by a table")
            elif not rows:
                problems.append(f"{marker.where}: the table after values-md:{marker.kind} has no rows")
            elif marker.kind == FIELD_TABLE:
                problems += _field_table_problems(marker.where, rows, schema)
            elif [row[0] for row in rows] != rules.RULES:
                listed = ", ".join(row[0] for row in rows)
                problems.append(f"{marker.where}: the rule table lists {listed}, and the checker implements {', '.join(rules.RULES)}")
        elif block is None:
            problems.append(f"{marker.where}: values-md:{marker.kind} is not followed by a fenced block")
        elif marker.kind == SMALLEST:
            smallest = spec_dir.parent / "values" / SMALLEST_FILE
            if block.content.encode("utf-8") != smallest.read_bytes():
                problems.append(f"{block.where}: the smallest file shown differs from values/{SMALLEST_FILE}")
        else:
            rendered.add((marker.document, marker.target))
            expected = fixtures_dir / marker.argument
            if fixtures_dir.resolve() not in expected.resolve().parents or not expected.is_file():
                problems.append(f"{marker.where}: {marker.argument} is not a file under fixtures/")
            elif block.content.encode("utf-8") != expected.read_bytes():
                problems.append(f"{block.where}: this block differs from fixtures/{marker.argument}, which it is marked as showing")

    for key, block in blocks.items():
        text = _normative_text(block)
        if text and key not in rendered and block.content != render.template(text, spec_dir / "prompts"):
            problems.append(f"{block.where}: the quoted {text} differs from prompts/{text}.txt and is not marked as a rendering")
    return problems
