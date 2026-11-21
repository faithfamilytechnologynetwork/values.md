"""Maps a valid package to a Claude Code marketplace entry, by the table in the standard.

Nothing is invented. A field that `VALUES.md` does not have is left out of the entry. It is
never written as null or as an empty value.
"""

from __future__ import annotations

import os
from pathlib import Path


def entry(frontmatter: dict, source: str) -> dict:
    """The marketplace entry for one package.

    `source` is the path from the marketplace file's root to the package folder, beginning
    `./`.
    """
    steward = frontmatter["steward"]
    author = {"name": steward["name"]}
    if "url" in steward:
        author["url"] = steward["url"]

    made = {
        "name": frontmatter["name"],
        "source": source,
        "description": f"{frontmatter['description']} Vouched for by {steward['name']} ({steward['claim']}).",
    }
    if "version" in frontmatter:
        made["version"] = frontmatter["version"]
    made["author"] = author
    if "license" in frontmatter:
        made["license"] = frontmatter["license"]
    if "tradition" in frontmatter:
        made["category"] = frontmatter["tradition"][0]
    # Tradition, then languages, then tags. A repeated value is kept once, where it first appears.
    tags = list(dict.fromkeys(
        frontmatter.get("tradition", []) + frontmatter.get("languages", []) + frontmatter.get("tags", [])
    ))
    if tags:
        made["tags"] = tags
    return made


def entries(reports: dict, collection: Path, root: Path) -> list[dict]:
    """The entries for a collection whose packages are all valid, in order of folder name.

    `reports` holds the check report for each package folder, by folder name. `root` is the
    directory the marketplace file resolves paths from. It is the collection or a directory
    above it. Anything else raises ValueError.
    """
    root = Path(os.path.abspath(root))
    listing = []
    for folder in sorted(reports):
        from_root = Path(os.path.abspath(collection / folder)).relative_to(root).as_posix()
        listing.append(entry(reports[folder].frontmatter, f"./{from_root}"))
    return listing
