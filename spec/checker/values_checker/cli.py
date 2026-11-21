"""Command line for the values.md checker."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from values_checker import fixtures as fixtures_module
from values_checker import rules
from values_checker import selftest as selftest_module

FIXTURES_DIR = rules.SPEC_DIR / "fixtures"

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Checks a VALUES.md package against the values.md standard, version 0.1.",
)


@app.command()
def check(path: Annotated[Path, typer.Argument(help="A VALUES.md file.")]) -> None:
    """Decide whether a VALUES.md file is valid. Exits 0 only when it is."""
    if not path.is_file():
        raise typer.BadParameter(f"{path} is not a file. This version checks a single VALUES.md file.")
    report = rules.check_file(path)
    if report.outcome == rules.VALID:
        typer.echo(f"valid: {path} (body {report.body_chars:,} characters, core {report.core_chars:,})")
        return
    if report.outcome == rules.UNSUPPORTED_VERSION:
        typer.echo(
            f"unsupported version: {path} targets version {report.spec_version} of the standard. "
            f"This checker implements {rules.IMPLEMENTED_VERSION} and cannot judge it."
        )
        raise typer.Exit(3)
    typer.echo(f"invalid: {path} breaks {', '.join(report.rules)}")
    for failure in report.failures:
        typer.echo(f"  {failure.code}: {failure.message}")
    raise typer.Exit(1)


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
    typer.echo("fixtures pass, and the audits find every rule, failure and schema constraint covered")


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
