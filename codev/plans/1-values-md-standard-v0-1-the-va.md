# Plan: values.md standard v0.1 — the VALUES.md package format

**Specification**: [codev/specs/1-values-md-standard-v0-1-the-va.md](../specs/1-values-md-standard-v0-1-the-va.md)

## Executive Summary

The spec chose a plugin-shaped folder with one new file, `VALUES.md`, and fixed the rules for
reading it, wrapping it, keeping it in force and deciding whether a package is valid. This plan
writes those rules down twice, in the order that lets each be tested as it is written:

1. first as things a program can check: two schemas, the three normative prompt texts, a
   checker and a set of fixtures;
2. then as the four example packages, which the checker validates where they live in
   `values/`;
3. then as prose: the specification text, the rationale and the compatibility note, each
   checked against the machine-readable parts so that the two cannot drift.

The checker comes first because the spec's own success criteria are mostly of the form "the
rules, applied to this input, give this result". With the checker and fixtures in place, every
later phase has something to run.

"Part N" below means part N of the spec's Desired State section. "V1" to "V10" are its
validity rules.

### Layout this plan creates

```
spec/
  README.md               what is here, how to run the checks, licence of the text
  specification.md        the standard (normative)
  rationale.md
  compatibility.md
  schema/values.schema.json     the frontmatter (rule V3)
  schema/mcp.schema.json        the shape of .mcp.json (rule V7)
  prompts/wrapper.txt  reminder.txt  preamble.txt
  fixtures/
    fixtures.json         every fixture, its scope, and the outcome it must give
    valid/<name>/...      each with expected/wrapper.txt and expected/reminder.txt
    invalid/<rule>-<what>/...
    collections/<name>/...
  checker/                a small Python project (see below)
values/
  example-islam/
  example-roman-catholic/
  example-principled-pluralism/
  plain-speaking/
```

### The checker

A Python package, `values_checker`, in `spec/checker/`, managed with `uv`, with a Typer command
line run as `uv run --project spec/checker python -m values_checker <command>`. It is the
standard testing itself. It loads nothing into a model and makes no network call.

| Command | Phase | What it does |
|---|---|---|
| `check <path>` | 1, 2 | Applies the validity rules to a file, a folder or a collection. Prints the outcome (valid, invalid with rule identifiers, or unsupported version) and exits non-zero unless valid. |
| `fixtures` | 1, 2 | Runs `check` on every entry in `fixtures.json` and compares each result with what the entry says it must be. From Phase 2 it also renders every valid fixture and compares the result with the expected files. It then runs the coverage audits described below. This is the test suite. |
| `selftest` | 1, 2, 4 | Breaks temporary copies of the fixtures and documents on purpose and confirms that `fixtures` and `consistency` report each break. It shows the other commands cannot pass with nothing to check. |
| `render <package>` | 2 | Prints the wrapper and reminder for a valid package by the rules of parts 3 and 4. |
| `marketplace <collection>` | 2 | Prints the Claude Code marketplace entries for a collection by the mapping in part 12. |
| `consistency` | 4 | Checks the documents under `spec/` against the schemas, the prompt files, the fixtures and `values/`. |

Dependencies, all from the Python package index with a committed lock file: `typer`,
`ruamel.yaml` and `jsonschema` (draft 2020-12). Typer is the project owner's standing choice
for Python command lines. The environment is installed once with `uv sync`. After that every
command runs with no network, and `fixtures` enforces it: it replaces socket creation with a
function that raises, so a rule that reached for the network would fail the run.

**YAML.** Checked on 2026-11-20 against `ruamel.yaml` 0.19.1: it refuses duplicate keys, but it
resolves aliases silently, turns `2026-01-01` into a date and applies `<<` merge keys. None of
the last three is YAML 1.2 core schema. So the checker reads the frontmatter in two steps. It
walks the parser's event stream and refuses any alias event and any event that carries an
anchor. It then builds values from the composed nodes with its own resolver for the core
schema: null, booleans, integers, floats and strings, by the regular expressions in the YAML
1.2 specification, and nothing else. A quoted scalar that contains `&` or `*` is not affected,
because the test is on events and not on the raw text.

**Markdown.** The rules of part 3 (ATX headings, fences, the core section) are the standard's
own and are written by hand. They are deliberately not a full Markdown parser.

**Agent Skills (V8).** The checker implements the Agent Skills frontmatter rules itself, taken
from that project's reference validator at a named commit: a `SKILL.md` in each folder under
`skills/`, a `name` that meets the format's rules and equals the folder name, a `description`
within its limit, and the limits on the optional fields. This keeps V8 working offline with no
dependency fetched from a git repository. The reference validator, `skills-ref`, is then used
as an outside cross-check: in Phase 2 on every V8 fixture, where its verdict must agree with
the checker's, and in Phase 3 on the example's skill.

### Fixtures are the tests, and they are audited

Each entry in `fixtures.json` records the path, the scope (file, folder or collection), the
expected outcome, the rule identifiers expected, and for each failure a short **detail code**
that says why (`V5:two-matching-headings`, `V1:not-utf8`). For a V3 or V7 failure the detail is
the schema keyword that rejected the input (`properties/name/pattern`). A valid entry also
records the expected number of characters in the body and in the core. Detail codes belong to
this checker. They are not part of the standard, which asks only for rule identifiers.

The detail codes make three mechanical audits possible, and `fixtures` fails if any of them
fails:

1. **Every rule** V1 to V10 has at least one invalid fixture.
2. **Every failure the checker can report** is produced by at least one fixture. The checker
   keeps a list of its detail codes, and a code that no fixture triggers is an error.
3. **Every constraint in the two schemas** rejects at least one fixture. The audit walks each
   schema for its constraint keywords (`required`, `pattern`, `enum`, `const`, the length, item
   and number bounds, `additionalProperties: false`, `oneOf`, `if`/`then`) and requires that
   each one is the recorded cause of some fixture's failure. For every length or number bound
   there is also a valid fixture exactly at the bound.

`fixtures` also fails when a directory under `fixtures/` has no entry, when an entry has no
directory, when a valid fixture has no expected rendering (from Phase 2), and when a fixture
fails for a reason other than the recorded one.

There are no separate unit test files. A rule that is wrong shows up as a fixture with the
wrong outcome, a rule with no fixture shows up in audit 2 or 3, and `selftest` shows that the
audits themselves bite.

### Order of evaluation

The spec says an invalid package is reported with every rule that failed. Some rules cannot be
judged once an earlier one has failed, so the checker, and later the specification text, fix
the order. A rule that could not be evaluated is not reported at all.

1. **V1.** If it fails, no other file rule is evaluated.
2. **V2.** If it fails, the rules that need the frontmatter (the version gate, V3, V5 and V10)
   are not evaluated. V4 and V6 need only the body and still are.
3. **The version gate.** If `spec-version` is present, is a string of the form
   `digits.digits`, and is not `"0.1"`, the outcome is "unsupported version" and no further
   rule is evaluated for that package at any scope. A later version may change any of them.
   Such a package takes no part in another package's V10 check.
4. **V3.** A `spec-version` that is not a string, or not of that form, fails here. An unquoted
   `spec-version: 0.2` is a float under the core schema, so it is a V3 failure and not an
   unsupported version.
5. **V4 and V6**, on the body.
6. **V5**, unless the body is empty or `persistence.reinject.section` is present and not a
   valid value. In both cases another rule has already reported the cause.
7. **V7, V8 and V9**, each on its own, at folder scope.
8. **V10**, at collection scope, when `name` could be read as a string.

### Decided in planning

- **How a fence closes.** The spec says a fenced code block opens with three or more backticks
  or tildes and does not say how it closes. The checker and the specification text use the
  CommonMark rule: the opening line may be indented by up to three spaces, and the block closes
  at the next line that holds only the same character, at least as many times, and optional
  trailing spaces. A block that is never closed runs to the end of the body. A heading starts
  at the first column, as the spec's "a line that starts with" says.
- **The order of evaluation above.** It refines the spec's "every rule that failed".
- **A schema for `.mcp.json`.** Part 7 defines the shape in prose. Writing it as a second
  schema makes V7 as mechanical as V3 and gives a collection's checker something to reuse. The
  prose in the specification stays the definition.
- **The Roman Catholic example has no MCP server.** A search on 2026-11-20 found Catholic MCP
  servers, none with the standing the spec asks for: a third-party wrapper around the
  Magisterium AI service, which needs the user's own API key, and several narrow ones (the
  liturgical calendar, a single encyclical, a general Christian-texts server). The example is
  text-backed, as the spec allows.
- **Its bundled text is the 1885 Baltimore Catechism No. 2**, from Project Gutenberg ebook
  14552, which is marked public domain in the United States. The Apostles' Creed is taken from
  the same book. Project Gutenberg's own header, licence and name are removed, as its terms ask
  when a text is redistributed. The Catechism of the Catholic Church and modern Bible
  translations are cited and linked, not reproduced. Phase 3 confirms the edition and the
  wording against the source file before anything is committed.
- **The symbolic-link fixture for V9 is built at run time** in a temporary directory, because a
  link committed to git does not survive every checkout. It still has an entry in
  `fixtures.json`, marked as built at run time, so the manifest lists every fixture.
- **Fixture files keep their exact bytes.** A `.gitattributes` in `spec/fixtures/` turns off
  line-ending conversion, since several fixtures exist to test line endings and encoding.
- **Porch's checks are pointed at the checker.** The protocol's default build and test checks
  run `npm`, which this repository does not use. Phase 1 adds a `porch.checks` entry to
  `.codev/config.json`: build is `uv sync` for the checker, and tests is the checker's own
  commands. The entry grows as phases add commands.
- **If a measured figure disagrees with the spec**, the wording is not edited to hit the
  number. The spec gives 1,504 characters for the wrapper's fixed text and 9,432 for the worst
  case. If the committed file measures differently, the text is first compared with part 4. If
  it matches, the figures are wrong, and that is reported to the architect as an erratum.

### For the owner at the plan gate

Three points are the owner's to settle. The plan states what it will do if no answer comes, so
that work is not blocked.

1. **The `prompt` value for `example-islam`** (the spec's open question 3). The checkpoint was
   trained and evaluated with no system prompt, and running it under a value-system prompt is
   untested. `omit` claims nothing unproved, but it means the only example that declares a
   model cannot be used to try "fine-tuned model with the prompt". `optional` allows that, and
   claims it works. Recommended: `omit` now, changed to `optional` when the reference
   implementation has tested the combination.
2. **The `tradition` value for `example-islam`**: `[Islam]` or `[Islam, Sunni]`. The checkpoint
   is described as Sunni and the Ansari service is not limited to one school. Recommended:
   `[Islam]`.
3. **The licence for everything that is not the specification text.** Until it is answered, no
   licence file is added and the examples carry no `license` field. `spec/README.md` states
   that the text is CC BY 4.0, which is decided.

## Phases (Machine Readable)

<!-- REQUIRED: porch parses this JSON to track phase progress. Keep it in sync when you add or remove phases; at least two phases. -->

```json
{
  "phases": [
    {"id": "phase_1", "title": "File-level validity: schema, normative prompt texts, checker and file fixtures"},
    {"id": "phase_2", "title": "Folder and collection validity, rendering and the marketplace mapping"},
    {"id": "phase_3", "title": "The four example packages in values/"},
    {"id": "phase_4", "title": "The specification text"},
    {"id": "phase_5", "title": "Rationale and compatibility note"}
  ]
}
```

## Phase Breakdown

### Phase 1: File-level validity: schema, normative prompt texts, checker and file fixtures

**Dependencies**: None

#### Objective

Make the rules for a single `VALUES.md` file executable: a schema for the frontmatter, the
three normative texts as files, and a checker that reads a file by the eight reading rules of
part 3 and applies V1 to V6 with the three outcomes of part 11. This phase checks validity
only. Rendering arrives in Phase 2.

#### Files to Create / Modify

- `spec/schema/values.schema.json`
- `spec/prompts/wrapper.txt`, `spec/prompts/reminder.txt`, `spec/prompts/preamble.txt`
- `spec/checker/pyproject.toml`, `spec/checker/uv.lock`
- `spec/checker/values_checker/__init__.py`, `__main__.py`, `cli.py`, `reading.py`, `rules.py`,
  `fixtures.py`, `selftest.py`
- `spec/fixtures/.gitattributes`, `spec/fixtures/fixtures.json`
- `spec/fixtures/valid/…` and `spec/fixtures/invalid/…`, file-scope fixtures only
- `.codev/config.json` (the `porch.checks` entry)

#### Deliverables

- [ ] The schema, in JSON Schema draft 2020-12, carrying every field rule of parts 2 and 6:
      requiredness, bounds, the `steward.url` condition, the three `claim` values, the three
      `prompt` values, unknown keys allowed at the top level and refused inside `steward`,
      `persistence`, `persistence.reinject` and a `models` entry, and `metadata` with any JSON
      value. No `access` field.
- [ ] The three normative texts, word for word as in part 4, each ending in exactly one line
      feed.
- [ ] `reading.py`: encoding, byte-order mark, line endings, frontmatter split, the two-step
      YAML read described above, body trim, code-point counts, ATX headings outside fences,
      heading text, core resolution.
- [ ] `rules.py`: V1 to V6, the version gate, and the order of evaluation.
- [ ] `check`, `fixtures` (validity and the three audits) and `selftest` commands.
- [ ] File fixtures, each in `fixtures.json` with its outcome, rules and detail codes. The
      lists below are the cases that must exist. Audits 2 and 3 add any that are missing.

  **Valid**
  - the smallest file; a file with every optional field; `spec-version: "0.1"` given;
  - a long body with a core section; a custom core heading matched without regard to case; a
    short body with a core section; a short body with none;
  - `## Core ##`, where the closing run of `#` is removed and the heading matches;
  - a `# Title` after the core section, which ends the core, and a `### Detail` inside the
    core, which does not;
  - a `## Core` line inside a backtick fence, a tilde fence, a fence of four markers closed by
    four, and a fence that is never closed, each in a body that has a real core section
    elsewhere;
  - a file with a leading byte-order mark;
  - a CRLF file and a lone-CR file, each built so that it is valid only if line endings are
    normalised first: the body is within 7,500 characters only when the carriage returns are
    gone, and the core heading matches only without a trailing one;
  - a body of exactly 7,500 characters and a core of exactly 1,500, both made largely of
    characters outside the Basic Multilingual Plane, so that counting bytes or UTF-16 units
    would put them over;
  - an unknown top-level key; `metadata` holding nested lists and objects; `metadata` holding
    `2026-01-01`, which stays a string;
  - `claim: individual` with no URL; a model entry with `prompt: omit`; a body containing the
    text `{name}`; a quoted frontmatter string containing `&` and `*`.

  **V1**: wrong file name; bytes that are not UTF-8; no frontmatter; no closing delimiter; a
  delimiter line of `--- ` with a trailing space; frontmatter over 8,000 characters.

  **V2**: duplicate key; an anchor and alias; an anchor with no alias; frontmatter that is a
  list; frontmatter that is not parseable YAML.

  **V3**: at least one fixture for every constraint in the schema (audit 3). That covers a
  missing `name`, `description` or `steward`; a malformed or over-long `name`; a multi-line or
  over-long `description`; a `steward.name` with a forbidden character; a missing or unknown
  `claim`; `organization` and `official` with no `url`; a `url` that is not `https`; an unknown
  key inside `steward`, `persistence`, `persistence.reinject` and a model entry; a `version`
  that is not Semantic Versioning, and an unquoted `version: 1.0`; a malformed language tag;
  every list over its item limit; `every-tokens` of 999 and of 1,000,001; `persistence` as a
  string; a model entry without `provider`, `base` or `adapter`; `prompt: sometimes`; a
  `context-window` out of range; `spec-version: 0.2` unquoted; `spec-version: "v1"`.

  **V4**: empty body; a body of only whitespace; a body of 7,501 characters.

  **V5**: long body with no core section; two matching headings; a core of 1,501 characters; a
  core section with no text; the only `## Core` line inside a fence in a long body; a Setext
  "Core" heading in a long body; `## **Core**` as the only candidate in a long body, which
  does not match because inline formatting is kept; `##Core` with no space.

  **V6**: `</values>`; `</VALUES >`; `< / value-system>`; an opening `<value-system-reminder`.

  **Unsupported version**: `spec-version: "0.2"`; `spec-version: "0.2"` with `name` missing,
  which is still "unsupported version" by the order of evaluation.

#### Acceptance Criteria

- [ ] `uv run --project spec/checker python -m values_checker fixtures` exits zero with socket
      creation blocked: every file fixture gives its recorded outcome, rules and detail codes,
      and the three audits pass for V1 to V6 and the frontmatter schema.
- [ ] `selftest` exits zero. Each of these breaks, made on a temporary copy, makes `fixtures`
      fail: an entry removed from the manifest; an entry added with no directory; an expected
      outcome flipped; a recorded detail code changed; every fixture for one rule removed; one
      schema constraint left with no fixture; the fence rule switched off in the reading code.
- [ ] The schema validates against the draft 2020-12 meta-schema.
- [ ] The fixed text of `wrapper.txt`, with placeholders removed, is 1,504 characters. If not,
      the erratum rule above applies.
- [ ] Porch's build and test checks run the checker and pass.

#### Test Plan

- Run `fixtures` and `selftest`.
- Run `check` by hand on the smallest file and on two invalid fixtures, and read the output a
  person would see.
- Confirm in a Python session, before writing `reading.py`, the library behaviour the plan
  relies on: the event types for anchors and aliases, and the error raised for a duplicate
  key.

### Phase 2: Folder and collection validity, rendering and the marketplace mapping

**Dependencies**: Phase 1

#### Objective

Extend the checker from a file to a folder and to a collection, add rendering, and add the
mapping to a Claude Code marketplace entry, so that every mechanical rule in the standard can
be run.

#### Files to Create / Modify

- `spec/schema/mcp.schema.json`
- `spec/checker/values_checker/rules.py` (V7 to V10), `skills.py`, `render.py`,
  `marketplace.py`, `fixtures.py`, `selftest.py`, `cli.py`
- `spec/fixtures/fixtures.json`
- `spec/fixtures/valid/…/expected/wrapper.txt` and `reminder.txt` for every valid fixture
- `spec/fixtures/valid/…` and `invalid/…` folder fixtures, `spec/fixtures/collections/…`

#### Deliverables

- [ ] `mcp.schema.json` and V7: the shape of `.mcp.json` from part 7.
- [ ] V8, implemented in `skills.py` from the Agent Skills rules, with the commit of the
      reference validator it was taken from named in the file.
- [ ] V9: no symbolic links.
- [ ] V10: folder name equals `name`, and names are unique in a collection.
- [ ] `render`: single-pass placeholder substitution, trimmed body and core, one final line
      feed.
- [ ] `marketplace`: the mapping table of part 12, including the fixed sentence appended to the
      description, the `author` object, tag order with repeats removed, absent fields left out,
      and `source` as the path from the marketplace root.
- [ ] Folder fixtures:
  - **Valid**: a package with a remote server (the fixture the specification's worked example
    uses); one with `type: sse`; one with a local server that has `args` and `env`; one whose
    server object and whose top level carry unknown keys, which are ignored; a package with a
    skill and `references/`.
  - **V7**: at least one fixture for every constraint in `mcp.schema.json` (audit 3). That
    covers a file that is not JSON; a file that is not an object; no `mcpServers`;
    `mcpServers` as a list; a bad server name; both `url` and `command`; neither; an `http`
    address; an `http` loopback address; a `url` that is a number; an unknown `type`; an empty
    `command`; a `command` that is a list; `args` as a string; `args` holding a number; `env`
    as a list; `env` with a number as a value; `headers` present.
  - **V8**: no `SKILL.md`; a missing `description`; a name that does not match its folder; a
    name with a capital letter; a `description` over its limit.
  - **V9**: a symbolic link to a file and one to a directory, both built at run time.
- [ ] Collection fixtures: a valid collection of two packages; one whose folder name differs
      from its `name` (V10); one with a duplicated name (V10); one holding an
      unsupported-version package beside a valid one.
- [ ] An expected wrapper and reminder for every valid fixture, including those from Phase 1,
      and an expected marketplace entry for the valid collection.
- [ ] A fixture with the longest name, steward name and body, whose rendered wrapper must be
      9,432 characters.

#### Acceptance Criteria

- [ ] `fixtures` exits zero with socket creation blocked, and the three audits pass for all of
      V1 to V10 and both schemas.
- [ ] Every valid fixture renders to exactly its expected wrapper and reminder.
- [ ] The marketplace entries for the valid collection equal the expected ones.
- [ ] `check` on the collection fixtures reports V10 for the right package.
- [ ] `skills-ref validate`, run from the named commit, gives the same verdict as the checker on
      every V8 fixture and on the valid skill fixture. (tool) If it cannot be run, this is
      reported as not verified. V8 itself does not depend on it.
- [ ] `selftest` also covers: an expected wrapper changed by one character; a valid fixture
      with its expected files removed.

#### Test Plan

- Run `fixtures` and `selftest`.
- Write the expected renderings for two fixtures by hand from part 4 before `render` exists,
  then compare. This keeps the expectations from being a copy of the program's own output.
- Check the size-budget fixture's length independently with a one-line count.
- Run `skills-ref` on the V8 fixtures and record the result.

### Phase 3: The four example packages in values/

**Dependencies**: Phase 2

#### Objective

Write the four example packages where they live, as the first entries of the collection, and
show that each is valid there by the standard's rules alone.

#### Files to Create / Modify

- `values/plain-speaking/VALUES.md`
- `values/example-principled-pluralism/VALUES.md`, `README.md`
- `values/example-islam/VALUES.md`, `.mcp.json`, `README.md`
- `values/example-roman-catholic/VALUES.md`, `README.md`,
  `references/apostles-creed.md`, `references/sources.md`,
  `skills/catechism-answers/SKILL.md`,
  `skills/catechism-answers/references/baltimore-catechism-no-2.md`
- `.codev/config.json` (the test check gains `check values/`)

#### Deliverables

- [ ] `plain-speaking`: the file from the top of the spec, unchanged.
- [ ] `example-principled-pluralism`: a short body that states the value system's own position
      as the essay gives it, cites the essay, and carries the "illustrative, not endorsed by
      its author" notice.
- [ ] `example-islam`: a body that keeps to high-consensus basics and sends rulings, verses and
      hadith to Ansari; `.mcp.json` declaring `https://mcp.ansari.chat/mcp`; the model entry
      from part 13 with a `description` and the `prompt` value settled at the plan gate;
      `languages: [en]`.
- [ ] `example-roman-catholic`: a body that keeps to high-consensus basics; a self-contained
      skill that answers basic questions from the bundled catechism and points to the current
      Catechism online; the Apostles' Creed and a list of sources in `references/`. Every
      bundled text states its source and the basis for its public-domain status.
- [ ] The three `example-` packages name the values.md project as steward with the claim
      `organization`, and carry their notice in the description, the body and the README.
- [ ] No copy of any package under `spec/`.

#### Acceptance Criteria

- [ ] `check values/` reports every package valid, with socket creation blocked.
- [ ] Every body is at most 7,500 characters and every core at most 1,500. (`check` enforces
      this. The numbers are also recorded for the review.)
- [ ] (tool) The Ansari server answers `initialize` and lists `answer_islamic_question`, and
      the date is recorded.
- [ ] (tool) The skill passes `skills-ref validate`.
- [ ] (tool) A temporary copy of each folder example, with only `.claude-plugin/plugin.json`
      added, passes `claude plugin validate` and loads in Claude Code with its skill or MCP
      server available.
- [ ] (tool) A marketplace file generated for `values/` passes `claude plugin validate`, and
      one example installs from it in Claude Code with no `plugin.json` in its folder.
- [ ] Each statement an example makes about a tradition or about the essay is traced to a
      source, and the list is kept for the review.

#### Test Plan

- Run `check values/` and `render` on each package, and read each rendered wrapper in full as
  a model would receive it.
- Probe the Ansari server with `initialize` and `tools/list`.
- For the Islam body, put each factual statement to Ansari and compare. For the Catholic body,
  compare each statement with the bundled catechism. For the pluralism body, compare each
  statement with the essay.
- Run the Claude Code checks on temporary copies outside the repository, so that nothing is
  added to `values/`.
- A check marked (tool) that cannot be run, for whatever reason, is reported as not verified.
  This applies in particular to loading the Islam example's checkpoint from a second account,
  which needs provider access this project does not have.

### Phase 4: The specification text

**Dependencies**: Phases 1, 2 and 3

#### Objective

Write the standard as a document a host developer or a package author can implement from, and
tie it to the machine-readable parts so that the two stay the same.

#### Files to Create / Modify

- `spec/specification.md`
- `spec/README.md`
- `spec/checker/values_checker/consistency.py`, `selftest.py`, `cli.py`
- `.codev/config.json` (the test check gains `consistency`)

#### Deliverables

- [ ] `specification.md`, in RFC 2119 language, covering parts 1 to 12:
  - an opening that shows the smallest valid file in full and the two lists of what a
    first-time author and a Level 1 host can ignore;
  - package shape; frontmatter with the field table; reading rules, body, prompt and core,
    with the fence rule; the three normative texts quoted; prompt fade and reinjection;
    fine-tuned models with the `prompt` field, the three modes, who chooses and what the user
    is shown; tools, the shape of `.mcp.json`, consent, and conformance levels; discovery and
    installation; provenance; more than one value system; validity with rules V1 to V10,
    scopes, outcomes and the order of evaluation; collections, listings and the marketplace
    mapping;
  - a security section making the six points of part 8;
  - a worked example of the exact messages a Level 2 host sends for the remote-server fixture,
    including the first reminder at the default placement;
  - the conformance tests for hosts that the spec lists as "defined here, exercised by a
    host", stated as numbered requirements;
  - an **Examples** section that lists the four packages by path (`values/<name>`), says in a
    line what each one shows, and copies none of them. This is the only place principled
    pluralism is named.
- [ ] Each of the issue's eight questions answered in a section a reader can find, with a short
      table at the end pointing to each, as in part 17 of the spec. Question 7 points to the
      Examples section.
- [ ] `spec/README.md`: what each file is, the commands that run every check, and the licence
      of the text.
- [ ] The `consistency` command. The documents carry markers in HTML comments, and the command
      checks, across every Markdown file under `spec/`:
  - the field table (marked, exactly once, in `specification.md`) against the schema, in both
    directions: every field, its requiredness and its limits;
  - every fenced block that opens with one of the three normative tags: it is either identical
    to its file in `prompts/`, or it is marked as a rendering of a named fixture and identical
    to that fixture's expected file;
  - the smallest file shown (marked, exactly once) against `values/plain-speaking/VALUES.md`;
  - the rule table against the rules the checker implements, by identifier.

  A marker that is missing or appears twice is an error, and so is a table with no rows.

#### Acceptance Criteria

- [ ] `consistency` exits zero.
- [ ] `selftest` also covers `consistency`: one character changed in a quoted wrapper; a row
      dropped from the field table; a limit changed in the table; a marker removed; a marker
      duplicated. Each must make `consistency` fail.
- [ ] The messages in the worked example equal what `render` produces for that fixture. (This
      follows from `consistency`, and is also read by eye.)
- [ ] An agent given only `spec/` and one package from `values/` produces the correct rendered
      wrapper and reminder and says when the first reminder is due.
- [ ] The smallest valid file shown is no more than 12 lines.
- [ ] `fixtures` and `check values/` still exit zero.

#### Test Plan

- Run `consistency`, `selftest`, `fixtures` and `check values/`.
- The cold-reader test: start an agent with no context but `spec/` and one package, ask for
  the rendered wrapper, the rendered reminder and the point at which the first reminder
  falls, and compare with `render` and with the worked example. Where it goes wrong, fix the
  text, not the agent, and run it again with a fresh agent.
- Read the specification against the table in part 17 of the spec and tick each of the eight
  questions.

### Phase 5: Rationale and compatibility note

**Dependencies**: Phases 3 and 4

#### Objective

Record why the format has this shape, and say exactly what each kind of existing host gets
from a package.

#### Files to Create / Modify

- `spec/rationale.md`
- `spec/compatibility.md`
- `spec/README.md` (index entries)

#### Deliverables

- [ ] `rationale.md`: the four options with their trade-offs and why option 3; a comparison
      with AGENTS.md, Agent Skills, Claude Code plugins and Belief Protocol; the reasoning
      behind the main decisions inside option 3, including core-only reinjection with its cost
      figures and the `prompt` field. Every claim about another format has a link and the date
      it was checked. The wrapper's rules are explained on their own merits.
- [ ] `compatibility.md`: what Claude Code gets from a package with `plugin.json` added, and
      what it does not; the two ways to supply the prompt (hooks, a forced output style); the
      hook size cap with the budget arithmetic and the refuse-on-overflow rule; the marketplace
      mapping with a worked `marketplace.json` for `values/`, and the plain statement that the
      install screen shows the steward's claim only through the description; what a host that
      only reads skills gets; what a host that only reads AGENTS.md gets.
- [ ] The facts the spec marked as read through a summary only, re-read at the source before
      they are stated: the hook output cap, what hooks receive, and anything else the two
      documents rely on.

#### Acceptance Criteria

- [ ] Every statement the compatibility note makes about Claude Code is one that Phase 3
      observed or that is quoted from the linked documentation, and it says which.
- [ ] The worked `marketplace.json` equals what the `marketplace` command prints for `values/`.
- [ ] A link check finds every cited URL reachable, or the document notes the one that is not.
- [ ] Principled pluralism appears in neither document except in a list of the examples.
- [ ] `consistency` (which reads these two documents as well), `selftest`, `fixtures` and
      `check values/` still exit zero.

#### Test Plan

- Re-fetch each cited page and compare it with the claim made.
- Compare the worked marketplace file with the command's output.
- Search all of `spec/` for the words "principled pluralism" and confirm where they appear.
- Go through the spec's Success Criteria one by one and record, for each, the command or
  observation that shows it is met, or that it could not be verified.

## How the spec's success criteria map to phases

| Criterion (short form) | Phase |
|---|---|
| Deliverables present under `spec/` and `values/`, nothing else changed | 5 |
| Examples exist once, in `values/`, and are valid there; `spec/` refers to them by path | 3, 4 |
| Specification opens with the smallest file and the two lists | 4 |
| Eight questions answered | 4 |
| Security section | 4 |
| Field table and schema agree; unknown-key rules | 1 (schema), 4 (agreement) |
| Schema is valid draft 2020-12 | 1 |
| Rules V1 to V10, scopes, outcomes, fixtures for each | 1 and 2 |
| V3, V5, V7 fixture lists; unsupported-version fixture | 1 and 2 |
| Rules applied to every fixture offline give the labelled result | 1 and 2 |
| Normative texts as files, every quoted copy in `spec/` identical | 1 (files), 4 and 5 (identity) |
| Valid fixtures render exactly | 2 |
| Body and core limits for the examples | 3 |
| Cold-reader test | 4 |
| Worked example for a Level 2 host | 4 |
| Ansari server declared and answering | 3 |
| Notices on the three `example-` packages | 3 |
| Claude Code plugin and marketplace checks | 3 |
| Skills pass `skills-ref validate` | 2 (fixtures), 3 (the example) |
| Rationale content, links and dates | 5 |
| No bundled text under third-party copyright | 3 |
| Principled pluralism is an ordinary example | 3, 4 and 5 |
| `prompt` values in the schema; modes in the specification | 1 and 4 |
| `example-islam` declares the stage 2 checkpoint | 3 |
| Second-account load test recorded or reported not verified | 3 |
| Checker in its own directory, offline | 1 |
| No loader or chatbot code | 5 (final check) |

## Risks and Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| The checker and the specification text describe different rules. | Medium | High | The checker is written first from the approved spec. The specification is then checked against the schemas, the prompt files, the rule list and the fixtures by `consistency`, and `selftest` shows that check can fail. |
| The fixtures pass while leaving a rule untested. | Medium | High | The three audits: every rule, every failure the checker can report, and every schema constraint must be the cause of some fixture's failure. |
| Expected renderings are just the program's own output, so they prove nothing. | Medium | Medium | Two are written by hand from part 4 before `render` exists. The cold-reader test in Phase 4 is a second, independent implementation. |
| The YAML library does not behave as the plan assumes. | Low | Medium | The three behaviours the plan relies on were checked on 2026-11-20 and are named above. The core-schema resolver is the checker's own, and fixtures cover dates, merge keys, anchors and unquoted numbers. |
| The checker's own Agent Skills rules drift from that standard. | Low | Medium | They are taken from the reference validator at a named commit, and `skills-ref` is run on the V8 fixtures as a cross-check. |
| Claude Code does not ignore `VALUES.md` or `references/` at a plugin root, or does not take a wrapped `.mcp.json`. | Low | High | Tested in Phase 3. A failure goes to the architect at once, because it touches the owner's decision that a package installs in Claude Code unchanged. |
| An example misstates a tradition or the essay. | Medium | High | Bodies are short and keep to high-consensus basics. Each statement is traced to a source in Phase 3, and the notices say plainly that nobody with authority has endorsed the text. |
| The public-domain status of a bundled text is less clear than it looks. | Low | Medium | Only the 1885 Baltimore Catechism is bundled, from a Project Gutenberg edition marked public domain in the United States. Anything else is cited and linked. |
| Phase 4 is the largest phase and overruns. | Medium | Low | It stays one commit because the text and the command that checks it belong together. If it must be cut, the host conformance requirements move to a follow-up commit in the same phase, and the architect is told. |
| The Ansari server is down when Phase 3 runs. | Low | Low | Validity does not depend on it. The probe is retried, and if it still fails the criterion is reported as not verified. |
| The examples' licence is still undecided when Phase 3 commits. | Medium | Low | The examples carry no `license` field and no licence file is added until the owner answers. The review says so. |

## Documentation Updates

- `spec/README.md` is new and is the index for everything under `spec/`.
- Each `example-` package has its own `README.md`.
- `.codev/config.json` gains a `porch.checks` entry, so porch's build and test checks run the
  checker.
- `codev/resources/arch.md` and `codev/resources/lessons-learned.md` are still placeholders.
  They are filled in during the review phase, once there is an architecture and there are
  lessons to record.
- No README is added at the root of the repository. The spec limits this project to `spec/`
  and `values/`. The repository is public and has none, which is worth the architect's
  attention separately.
