# Architecture

This repository holds the values.md standard, the collection of value systems written to it,
and the program that checks both. It holds no assistant, no loader and no model client.

## Repository layout

- `spec/` is the standard: three documents (`specification.md` is normative; `rationale.md`
  and `compatibility.md` are not), two JSON Schemas in `schema/`, the three texts a host
  injects in `prompts/`, the fixtures in `fixtures/`, and the checker in `checker/`.
  `spec/README.md` is the index and the command reference.
- `values/` is the collection: one folder per value system, each with `VALUES.md` at its root.
- `codev/` holds the development records. `.codev/config.json` holds the porch checks.
- A reference implementation is planned under `reference/` and is a separate project. Nothing
  in `spec/` or `values/` depends on it.

## Single sources of truth

Each normative thing lives in one place, and every other mention is a checked copy or a path.

- The wrapper, the reminder and the multiple-system preamble are the files in `spec/prompts/`.
  A document under `spec/` that quotes one in a fenced block must match the file byte for byte.
- The frontmatter is defined by `spec/schema/values.schema.json`. The field table in
  `specification.md` must agree with it in both directions, word for word.
- The shape of `.mcp.json` is defined in prose in the specification, and
  `spec/schema/mcp.schema.json` is its mechanical form.
- A package lives once, in `values/`. `spec/` refers to packages by path. The one copy is the
  smallest valid file at the top of `specification.md`, which is compared with
  `values/plain-speaking/VALUES.md`.

## The checker

`spec/checker/` is a Python package, `values_checker`, managed with `uv` and run as
`uv run --project spec/checker python -m values_checker <command>`. Commands: `check`,
`render`, `marketplace`, `fixtures`, `consistency`, `selftest`.

- `reading.py` implements the reading rules: line endings, frontmatter delimiters, YAML, ATX
  headings, fences, the core section. `rules.py` applies V1 to V10 at file, folder and
  collection scope in a fixed order of evaluation. `skills.py` is rule V8.
- The YAML library is used as a parser only. The checker walks its events, refuses anchors,
  aliases and explicit tags, and builds values with its own YAML 1.2 core-schema resolver.
- Markdown handling is written by hand from the standard's own rules. It is deliberately not
  a Markdown parser.
- Nothing is read through a symbolic link. V9 reports the link, and a rule that would need the
  link's content is not judged.
- Exit codes are the checker's and not the standard's: 0 valid, 1 invalid, 3 unsupported
  version. An unexpected exception surfaces as a traceback and a non-zero exit, on purpose.

## Fixtures and audits

The fixtures are the test suite. There are no unit test files.

- `spec/fixtures/fixtures.json` lists every fixture with its scope, expected outcome, rule
  identifiers and a detail code for each failure. Each valid fixture has an `expected/`
  directory with the wrapper and reminder it must render to.
- `fixtures` fails unless three audits pass: every rule has an invalid fixture, every failure
  the checker can report is caused by some fixture, and every constraint in the two schemas
  is the recorded cause of some fixture's failure, with a valid fixture at every bound.
- `fixtures` blocks socket creation while it runs.
- Fixtures that need a symbolic link are built at run time in a temporary directory and are
  still listed in the manifest.
- `spec/fixtures/.gitattributes` turns off line-ending conversion. Several fixtures exist to
  test exact bytes.
- The expected renderings were made from the normative texts independently of `render`.

## Document consistency

`consistency` reads the Markdown files under `spec/`, outside `fixtures/` and `checker/`, and
checks them against the machine-readable parts through HTML-comment markers
(`values-md:field-table`, `values-md:rule-table`, `values-md:smallest-file`,
`values-md:rendering <path>`). `spec/README.md` documents the markers.

- A fenced block is compared with a file in `prompts/` only when the block opens with one of
  the injected prompt's tags.
- A schema keyword or pattern the field table has no words for is reported as a problem.
- Two copies are outside its reach and are maintained by hand: the worked `marketplace.json`
  in `compatibility.md` and the smallest file in the root `README.md`.

`selftest` breaks temporary copies of the fixtures and the documents, one way at a time, and
requires `fixtures` and `consistency` to report each break.

## The collection in values/

A folder directly inside `values/` is a package, and its name equals the package's `name`.
The collection must be valid under `check values/` with no network. The `marketplace` command
produces Claude Code marketplace entries from the collection by the mapping in the
specification.

- The three packages whose names begin `example-` are illustrations. Each says so in its
  description, body and README, and names the values.md project as steward.
- `plain-speaking` must stay identical to the smallest file shown in the specification, so it
  carries no optional fields.
- A bundled text states its own source and the basis of its public-domain or licence status.

## Checks porch runs

`.codev/config.json` points porch's build check at `uv sync` for the checker and its tests
check at four commands in sequence: `fixtures`, `selftest`, `consistency`, `check values/`.
The repository has no `npm` scripts.

## Licences

`specification.md`, `rationale.md` and `compatibility.md` are CC BY 4.0. Everything else is
MIT under the root `LICENSE`, except a public-domain text bundled inside a package.

## Verified-Wrong Assumptions

- Claude Code does not read `VALUES.md`. A package with a `plugin.json` added loads its tools
  and skills there and not its prompt, and a package the checker calls invalid still passes
  `claude plugin validate`.
- Text a Claude Code hook adds is placed in the conversation inside a system reminder. It is
  not in the system prompt.
- A marketplace entry can stand in for a plugin manifest, so a package folder can be listed
  with no `plugin.json` inside it.
- The YAML library resolves aliases silently, turns date-like scalars into dates and applies
  merge keys. None of that is YAML 1.2 core schema, which is why the checker has its own
  resolver.
- The Agent Skills reference validator refuses any frontmatter field outside its fixed set,
  accepts skill names in any script, and refuses flow-style YAML that its specification does
  not forbid. Rule V8 copies the first two and not the third.
