"""Renders the normative texts of the values.md standard, version 0.1.

The rendering rules: every placeholder is replaced in a single pass, so text that a
substituted value happens to contain, such as `{name}` in a body, is left as it is. The body
and core are the trimmed texts the reading rules give. Each text ends with one line feed.
"""

from __future__ import annotations

import re
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"
TEXTS = ("wrapper", "reminder", "preamble")

_PLACEHOLDER = re.compile(r"\{([a-z]+)\}")


def template(text: str, prompts_dir: Path = PROMPTS_DIR) -> str:
    """One of the three normative texts, as its file holds it."""
    content = (prompts_dir / f"{text}.txt").read_bytes().decode("utf-8")
    if "\r" in content or not content.endswith("\n") or content.endswith("\n\n"):
        raise ValueError(f"{text}.txt must use line feeds only and end with exactly one")
    return content


def substitute(text: str, values: dict[str, str]) -> str:
    """Replaces each placeholder once. A placeholder with no value is an error."""
    return _PLACEHOLDER.sub(lambda match: values[match[1]], text)


def wrapper(name: str, steward: str, body: str) -> str:
    return substitute(template("wrapper"), {"name": name, "steward": steward, "body": body})


def reminder(name: str, core: str) -> str:
    return substitute(template("reminder"), {"name": name, "core": core})
