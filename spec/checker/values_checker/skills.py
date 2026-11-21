"""Rule V8: every folder under `skills/` is a valid Agent Skill.

The rules are those of the Agent Skills reference validator, `skills-ref`, as it stood at
commit 83021e2be457a9b6679148719c1f6074f0ad975e of https://github.com/agentskills/agentskills
(`skills-ref/src/skills_ref/validator.py` and `parser.py`, Apache-2.0). They are written out
here, not imported, so that the check runs offline with nothing fetched from a git repository.

Three things here are the reference's and may surprise a reader of the values.md standard.
A name may hold letters and digits of any script, not only `a` to `z`. A skill's file may be
named `skill.md` when there is no `SKILL.md`. And the frontmatter is whatever lies between
the `---` that opens the file and the next `---` anywhere after it, not the next line that is
exactly `---`.

Nothing is read through a symbolic link. Rule V9 reports the link.

One known difference. The reference reads the frontmatter with a restricted YAML library that
also refuses flow-style lists and mappings such as `[a, b]`. The Agent Skills specification
does not ask for that, and this module does not copy it. Like the reference, it reads every
scalar as a string and refuses duplicate keys, anchors, aliases and explicit tags.
"""

from __future__ import annotations

import os
import unicodedata
from pathlib import Path

from values_checker import reading
from values_checker.reading import Unreadable

SKILLS_DIR = "skills"
NAME_LIMIT = 64
DESCRIPTION_LIMIT = 1024
COMPATIBILITY_LIMIT = 500
ALLOWED_FIELDS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}

DETAIL_CODES = {
    "V8:no-skill-md": "the skill folder has no SKILL.md",
    "V8:skill-frontmatter": "SKILL.md does not open with YAML frontmatter that is a mapping",
    "V8:skill-unexpected-field": "the frontmatter has a field Agent Skills does not define",
    "V8:skill-name-missing": "name is missing or is not a non-empty string",
    "V8:skill-name-format": f"name is over {NAME_LIMIT} characters or is not lowercase letters, digits and single hyphens",
    "V8:skill-name-folder": "name does not equal the skill's folder name",
    "V8:skill-description-missing": "description is missing or is not a non-empty string",
    "V8:skill-description-too-long": f"description is over {DESCRIPTION_LIMIT:,} characters",
    "V8:skill-compatibility": f"compatibility is not a string of at most {COMPATIBILITY_LIMIT} characters",
}


def _frontmatter(skill_md: Path) -> dict:
    """The frontmatter of a SKILL.md, found the way the reference finds it: the file starts
    with `---`, and the frontmatter runs to the next `---`."""
    try:
        text = skill_md.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        raise Unreadable("V8:skill-frontmatter") from None
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    parts = text.split("---", 2)
    if not text.startswith("---") or len(parts) < 3:
        raise Unreadable("V8:skill-frontmatter")
    try:
        return reading.parse_frontmatter(parts[1], resolve_scalars=False)
    except Unreadable:
        raise Unreadable("V8:skill-frontmatter") from None


def _name_codes(name, folder_name: str) -> list[str]:
    if not isinstance(name, str) or not name.strip():
        return ["V8:skill-name-missing"]
    name = unicodedata.normalize("NFKC", name.strip())
    well_formed = (
        len(name) <= NAME_LIMIT
        and name == name.lower()
        and not name.startswith("-")
        and not name.endswith("-")
        and "--" not in name
        and all(character.isalnum() or character == "-" for character in name)
    )
    codes = [] if well_formed else ["V8:skill-name-format"]
    if unicodedata.normalize("NFKC", folder_name) != name:
        codes.append("V8:skill-name-folder")
    return codes


def _skill_codes(skill_dir: Path) -> list[str]:
    present = set(os.listdir(skill_dir))
    file_name = next((name for name in ("SKILL.md", "skill.md") if name in present), None)
    if file_name is None:
        return ["V8:no-skill-md"]
    if (skill_dir / file_name).is_symlink():
        return []
    try:
        frontmatter = _frontmatter(skill_dir / file_name)
    except Unreadable as unreadable:
        return unreadable.codes

    codes = []
    if set(frontmatter) - ALLOWED_FIELDS:
        codes.append("V8:skill-unexpected-field")
    codes += _name_codes(frontmatter.get("name"), skill_dir.name)
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        codes.append("V8:skill-description-missing")
    elif len(description) > DESCRIPTION_LIMIT:
        codes.append("V8:skill-description-too-long")
    if "compatibility" in frontmatter:
        compatibility = frontmatter["compatibility"]
        if not isinstance(compatibility, str) or len(compatibility) > COMPATIBILITY_LIMIT:
            codes.append("V8:skill-compatibility")
    return codes


def check(package: Path) -> list[tuple[str, str]]:
    """Every V8 failure in a package folder, as (detail code, the skill folder it is in)."""
    skills = package / SKILLS_DIR
    if skills.is_symlink() or not skills.is_dir():
        return []
    found = []
    for skill_dir in sorted(child for child in skills.iterdir() if child.is_dir() and not child.is_symlink()):
        found += [(code, f"{SKILLS_DIR}/{skill_dir.name}") for code in _skill_codes(skill_dir)]
    return found
