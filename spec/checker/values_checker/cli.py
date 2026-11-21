"""Command line for the values.md checker."""

from __future__ import annotations

import json
import os
import sys
from enum import Enum
from pathlib import Path
from typing import Annotated

import typer

from values_checker import fixtures as fixtures_module
from values_checker import marketplace as marketplace_module
from values_checker import render as render_module
from values_checker import rules
from values_checker import selftest as selftest_module

FIXTURES_DIR = rules.SPEC_DIR / "fixtures"

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Checks a VALUES.md package against the values.md standard, version 0.1.",
)


class Scope(str, Enum):
    file = "file"
    folder = "folder"
    collection = "collection"


class Text(str, Enum):
    wrapper = "wrapper"
    reminder = "reminder"


def _scope_of(path: Path) -> Scope:
    """A file is checked as a file. A directory is a package folder when it holds VALUES.md,
    and a collection of package folders otherwise."""
    if path.is_file():
        return Scope.file
    if path.is_dir():
        return Scope.folder if rules.FILE_NAME in os.listdir(path) else Scope.collection
    raise typer.BadParameter(f"{path} does not exist")


def _check_package(path: Path, scope: Scope) -> rules.Report:
    if scope == Scope.file:
        if not path.is_file():
            raise typer.BadParameter(f"{path} is not a file")
        return rules.check_file(path)
    if not path.is_dir():
        raise typer.BadParameter(f"{path} is not a directory")
    return rules.check_folder(path)


def _exit_code(reports: list[rules.Report]) -> int:
    """0 when every package is valid, 1 when any is invalid, 3 when the only thing wrong is a
    version this checker does not implement."""
    outcomes = {report.outcome for report in reports}
    if rules.INVALID in outcomes:
        return 1
    return 3 if rules.UNSUPPORTED_VERSION in outcomes else 0


def _show(label: str, report: rules.Report) -> None:
    if report.outcome == rules.VALID:
        typer.echo(f"valid: {label} (body {report.body_chars:,} characters, core {report.core_chars:,})")
    elif report.outcome == rules.UNSUPPORTED_VERSION:
        typer.echo(
            f"unsupported version: {label} targets version {report.spec_version} of the standard. "
            f"This checker implements {rules.IMPLEMENTED_VERSION} and cannot judge it."
        )
    else:
        typer.echo(f"invalid: {label} breaks {', '.join(report.rules)}")
        for failure in report.failures:
            typer.echo(f"  {failure.code}: {failure.message}")


def _collection_reports(path: Path) -> dict[str, rules.Report]:
    if not path.is_dir():
        raise typer.BadParameter(f"{path} is not a directory")
    reports = rules.check_collection(path)
    if not reports:
        raise typer.BadParameter(f"{path} holds no package folders")
    return reports


@app.command()
def check(
    path: Annotated[Path, typer.Argument(help="A VALUES.md file, a package folder, or a collection of package folders.")],
    scope: Annotated[
        Scope | None,
        typer.Option(help="What the path is. By default: a file, a folder that holds VALUES.md, or else a collection."),
    ] = None,
) -> None:
    """Decide whether a package, or every package in a collection, is valid. Exits 0 only when
    all are."""
    scope = _scope_of(path) if scope is None else scope
    if scope == Scope.collection:
        reports = _collection_reports(path)
        for folder, report in reports.items():
            _show(str(path / folder), report)
        raise typer.Exit(_exit_code(list(reports.values())))
    report = _check_package(path, scope)
    _show(str(path), report)
    raise typer.Exit(_exit_code([report]))


@app.command()
def render(
    package: Annotated[Path, typer.Argument(help="A VALUES.md file or a package folder.")],
    only: Annotated[Text | None, typer.Option(help="Print one text, exactly as a host would inject it.")] = None,
) -> None:
    """Print the wrapper and the reminder for a valid package."""
    report = _check_package(package, _scope_of(package))
    if report.outcome != rules.VALID:
        _show(str(package), report)
        raise typer.Exit(_exit_code([report]))
    name = report.frontmatter["name"]
    texts = {
        Text.wrapper: render_module.wrapper(name, report.frontmatter["steward"]["name"], report.body),
        Text.reminder: render_module.reminder(name, report.core),
    }
    sys.stdout.write("".join(text for which, text in texts.items() if only in (None, which)))


@app.command()
def marketplace(
    collection: Annotated[Path, typer.Argument(help="A collection of package folders.")],
    root: Annotated[
        Path | None,
        typer.Option(help="The directory the marketplace file resolves paths from. By default, the collection's parent."),
    ] = None,
) -> None:
    """Print the Claude Code marketplace entries for a collection, as a JSON list."""
    reports = _collection_reports(collection)
    if _exit_code(list(reports.values())):
        for folder, report in reports.items():
            if report.outcome != rules.VALID:
                _show(str(collection / folder), report)
        typer.echo("no entries were made, because not every package is valid", err=True)
        raise typer.Exit(_exit_code(list(reports.values())))
    root = collection.resolve().parent if root is None else root.resolve()
    try:
        from_root = collection.resolve().relative_to(root).as_posix()
    except ValueError:
        raise typer.BadParameter(f"{collection} is not inside {root}") from None
    listing = marketplace_module.entries(reports, f"./{from_root}")
    typer.echo(json.dumps(listing, indent=2, ensure_ascii=False))


@app.command()
def fixtures(
    directory: Annotated[Path, typer.Option(help="The fixtures directory.")] = FIXTURES_DIR,
) -> None:
    """Run every fixture and the coverage audits, with the network blocked."""
    fixtures_module.block_network()
    problems = fixtures_module.run(directory)
    for problem in problems:
        typer.echo(problem)
    if problems:
        typer.echo(f"{len(problems)} problem(s)")
        raise typer.Exit(1)
    typer.echo(
        "fixtures pass: every valid one renders to its expected texts, "
        "and the audits find every rule, failure and schema constraint covered"
    )


@app.command()
def selftest(
    directory: Annotated[Path, typer.Option(help="The fixtures directory.")] = FIXTURES_DIR,
) -> None:
    """Break copies of the fixtures on purpose and confirm that each break is reported."""
    fixtures_module.block_network()
    undetected = selftest_module.run(directory)
    for case in undetected:
        typer.echo(case)
    if undetected:
        raise typer.Exit(1)
    typer.echo(f"selftest: all {len(selftest_module.CASES)} deliberate breaks were reported")
