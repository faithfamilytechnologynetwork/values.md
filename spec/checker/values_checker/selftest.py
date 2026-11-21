"""Shows that `fixtures` can fail.

Each case breaks a temporary copy of the fixtures, or the reading code, in one way and
requires `fixtures.run` to report it. A check that cannot fail proves nothing.
"""

from __future__ import annotations

import json
import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path

from values_checker import fixtures, reading


def _manifest(root: Path) -> dict:
    return json.loads((root / fixtures.MANIFEST).read_text(encoding="utf-8"))


def _save(root: Path, manifest: dict) -> None:
    (root / fixtures.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")


def _entry(manifest: dict, directory: str) -> dict:
    (entry,) = [e for e in manifest["fixtures"] if e["path"].startswith(directory + "/")]
    return entry


def _delete(root: Path, keep: Callable[[dict], bool]) -> None:
    """Removes fixtures, both from the manifest and from disk."""
    manifest = _manifest(root)
    for entry in manifest["fixtures"]:
        if not keep(entry):
            shutil.rmtree((root / entry["path"]).parent)
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
        lambda root: _delete(root, lambda e: not e["path"].startswith("invalid/v2-explicit-tag/")),
        "no fixture produces the failure V2:explicit-tag",
    ),
    (
        "the only fixture for one schema constraint removed",
        lambda root: _delete(root, lambda e: not e["path"].startswith("invalid/v3-claim-unknown/")),
        "rejected by the schema constraint properties/steward/properties/claim/enum",
    ),
    (
        "the fixture at the lower bounds removed",
        lambda root: _delete(root, lambda e: not e["path"].startswith("valid/bounds-minimum/")),
        "exactly at the bound",
    ),
    ("the fence rule switched off in the reading code", None, "fence"),
]


def run(fixtures_dir: Path) -> list[str]:
    """Returns the cases that went undetected. An empty list means every break was caught."""
    undetected = []
    with tempfile.TemporaryDirectory() as scratch:
        baseline = Path(scratch) / "baseline"
        shutil.copytree(fixtures_dir, baseline)
        if fixtures.run(baseline):
            return ["the unbroken fixtures do not pass, so nothing can be concluded"]

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
