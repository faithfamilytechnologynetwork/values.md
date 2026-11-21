"""Shows that `fixtures` and `consistency` can fail.

Each case breaks a temporary copy of the fixtures, the reading code, or the text of a
document in one way, and requires the check to report it. A check that cannot fail proves
nothing.
"""

from __future__ import annotations

import json
import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path

from values_checker import consistency, fixtures, reading, rules


def _manifest(root: Path) -> dict:
    return json.loads((root / fixtures.MANIFEST).read_text(encoding="utf-8"))


def _save(root: Path, manifest: dict) -> None:
    (root / fixtures.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")


def _entry(manifest: dict, directory: str) -> dict:
    (entry,) = [e for e in manifest["fixtures"] if fixtures.fixture_directory(e) == directory]
    return entry


def _delete(root: Path, keep: Callable[[dict], bool]) -> None:
    """Removes fixtures, both from the manifest and from disk."""
    manifest = _manifest(root)
    for entry in manifest["fixtures"]:
        if not keep(entry):
            shutil.rmtree(root / fixtures.fixture_directory(entry))
    manifest["fixtures"] = [e for e in manifest["fixtures"] if keep(e)]
    _save(root, manifest)


def _drop_entry(root: Path) -> None:
    manifest = _manifest(root)
    manifest["fixtures"].remove(_entry(manifest, "valid/smallest"))
    _save(root, manifest)


def _add_entry_without_file(root: Path) -> None:
    manifest = _manifest(root)
    manifest["fixtures"].append({**_entry(manifest, "valid/smallest"), "path": "valid/not-there/VALUES.md"})
    _save(root, manifest)


def _flip_outcome(root: Path) -> None:
    manifest = _manifest(root)
    _entry(manifest, "valid/smallest").update(outcome="invalid", rules=["V4"], details=["V4:empty-body"])
    _save(root, manifest)


def _change_detail(root: Path) -> None:
    manifest = _manifest(root)
    _entry(manifest, "invalid/v5-two-core-sections")["details"] = ["V5:empty-core"]
    _save(root, manifest)


def _change_body_count(root: Path) -> None:
    manifest = _manifest(root)
    _entry(manifest, "valid/smallest")["body-chars"] += 1
    _save(root, manifest)


def _change_expected_wrapper(root: Path) -> None:
    expected = root / "valid/smallest/expected/wrapper.txt"
    text = expected.read_text(encoding="utf-8")
    expected.write_text(text.replace("vouches", "vouchez", 1), encoding="utf-8")


def _remove_expected_renderings(root: Path) -> None:
    shutil.rmtree(root / "valid/smallest/expected")


def _change_expected_marketplace(root: Path) -> None:
    expected = root / "collections/two-packages/expected/marketplace.json"
    listing = json.loads(expected.read_text(encoding="utf-8"))
    listing[0]["tags"].reverse()
    expected.write_text(json.dumps(listing), encoding="utf-8")


def _no_fences(lines: list[str]) -> list[bool]:
    return [False] * len(lines)


# (what is broken, how, a phrase the report must contain)
CASES: list[tuple[str, Callable[[Path], None] | None, str]] = [
    ("an entry removed from the manifest", _drop_entry, "has no entry"),
    ("an entry added with no file", _add_entry_without_file, "does not exist"),
    ("an expected outcome flipped", _flip_outcome, "outcome is valid"),
    ("a recorded detail code changed", _change_detail, "details are"),
    ("an expected body length changed", _change_body_count, "body is"),
    (
        "every fixture for rule V6 removed",
        lambda root: _delete(root, lambda e: "V6" not in e.get("rules", [])),
        "no invalid fixture for rule V6",
    ),
    (
        "the only fixture for one failure removed",
        lambda root: _delete(root, lambda e: fixtures.fixture_directory(e) != "invalid/v2-explicit-tag"),
        "no fixture produces the failure V2:explicit-tag",
    ),
    (
        "the only fixture for one schema constraint removed",
        lambda root: _delete(root, lambda e: fixtures.fixture_directory(e) != "invalid/v3-claim-unknown"),
        "rejected by the V3 schema constraint properties/steward/properties/claim/enum",
    ),
    (
        "the fixture at the lower bounds removed",
        lambda root: _delete(root, lambda e: fixtures.fixture_directory(e) != "valid/bounds-minimum"),
        "exactly at the V3 bound",
    ),
    ("an expected wrapper changed by one character", _change_expected_wrapper, "rendered wrapper differs"),
    ("a valid fixture with its expected renderings removed", _remove_expected_renderings, "has no expected rendering"),
    ("an expected marketplace entry with its tags in another order", _change_expected_marketplace, "differs from expected/marketplace.json"),
    ("the fence rule switched off in the reading code", None, "fence"),
]


def _edited(old: str, new: str) -> Callable[[str], str]:
    """An edit to the specification text: the first place `old` appears becomes `new`."""
    return lambda text: text.replace(old, new, 1)


def _without_line(start: str) -> Callable[[str], str]:
    """An edit that drops every line beginning with `start`."""
    return lambda text: "".join(line for line in text.splitlines(keepends=True) if not line.startswith(start))


_FIELD_TABLE_MARKER = "<!-- values-md:field-table -->\n"
_SMALLEST_MARKER = "<!-- values-md:smallest-file -->\n"

# (what is broken, an edit to the specification text, a phrase the report must contain)
DOCUMENT_CASES: list[tuple[str, Callable[[str], str], str]] = [
    (
        "one character changed in the quoted wrapper",
        _edited("{steward} vouches for it.", "{steward} vouchez for it."),
        "the quoted wrapper differs from prompts/wrapper.txt",
    ),
    (
        "one character changed in a wrapper shown as a fixture's rendering",
        _edited("The Sample Society vouches for it.", "The Sample Society vouchez for it."),
        "differs from fixtures/valid/remote-server/expected/wrapper.txt",
    ),
    ("a row dropped from the field table", _without_line("| `license` |"), "no row for `license`"),
    (
        "a limit changed in the field table",
        _edited("String of 1 to 1,024 characters", "String of 1 to 1,025 characters"),
        "`description` is given as",
    ),
    (
        "a field marked required that the schema leaves optional",
        _edited("| `version` | No |", "| `version` | Yes |"),
        "`version` is given as required",
    ),
    ("a marker removed", _edited(_FIELD_TABLE_MARKER, ""), "values-md:field-table is missing"),
    (
        "a marker duplicated",
        _edited(_SMALLEST_MARKER, _SMALLEST_MARKER + "\n" + _SMALLEST_MARKER),
        "values-md:smallest-file appears 2 times",
    ),
    (
        "one character changed in the smallest file shown",
        _edited("Do not flatter me.", "Do not flatter me!"),
        "the smallest file shown differs",
    ),
    ("a rule dropped from the rule table", _without_line("| V9 |"), "the rule table lists"),
]


def _run_document_cases() -> list[str]:
    documents = consistency.documents(rules.SPEC_DIR)
    if consistency.check(documents):
        return ["the unbroken documents do not pass consistency, so nothing can be concluded"]
    undetected = []
    for what, edit, phrase in DOCUMENT_CASES:
        broken = {**documents, consistency.SPECIFICATION: edit(documents[consistency.SPECIFICATION])}
        if broken == documents:
            undetected.append(f"{what}: the break could not be made, because the text to change was not found")
        elif not any(phrase in problem for problem in consistency.check(broken)):
            undetected.append(f"{what}: not reported (expected a problem mentioning {phrase!r})")
    return undetected


def run(fixtures_dir: Path) -> list[str]:
    """Returns the cases that went undetected. An empty list means every break was caught."""
    undetected = _run_document_cases()
    with tempfile.TemporaryDirectory() as scratch:
        baseline = Path(scratch) / "baseline"
        shutil.copytree(fixtures_dir, baseline)
        if fixtures.run(baseline):
            return undetected + ["the unbroken fixtures do not pass, so nothing can be concluded"]

        for number, (what, break_it, phrase) in enumerate(CASES):
            copy = Path(scratch) / f"case-{number}"
            shutil.copytree(fixtures_dir, copy)
            if break_it is None:
                original = reading.fenced
                reading.fenced = _no_fences
                try:
                    problems = fixtures.run(copy)
                finally:
                    reading.fenced = original
            else:
                break_it(copy)
                problems = fixtures.run(copy)
            if not any(phrase in problem for problem in problems):
                undetected.append(f"{what}: not reported (expected a problem mentioning {phrase!r})")
    return undetected
