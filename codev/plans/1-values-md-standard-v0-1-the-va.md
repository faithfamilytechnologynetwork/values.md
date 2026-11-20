# Plan: values.md standard v0.1 — the VALUES.md package format

**Specification**: [codev/specs/1-values-md-standard-v0-1-the-va.md](../specs/1-values-md-standard-v0-1-the-va.md)

## Executive Summary

The spec chose a plugin-shaped folder with one new file, `VALUES.md`, and fixed the rules for
reading it, wrapping it, keeping it in force and deciding whether a package is valid. This plan
writes those rules down twice, in the order that lets each be tested as it is written:

1. first as things a program can check: the schema, the three normative prompt texts, a
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
  schema/values.schema.json
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

| Command | What it does |
|---|---|
| `check <path>` | Applies the validity rules to a file, a folder or a collection. Prints the outcome (valid, invalid with rule identifiers, or unsupported version) and exits non-zero unless valid. |
| `render <package>` | Prints the wrapper and reminder for a valid package by the rules of parts 3 and 4. |
| `fixtures` | Runs `check` on every entry in `fixtures.json` and `render` on every valid one, and compares each result with what the entry says it must be. This is the test suite. |
| `marketplace <collection>` | Prints the Claude Code marketplace entries for a collection by the mapping in part 12. |
| `consistency` | Checks that the specification's field table matches the schema, that quoted normative texts match the files in `prompts/`, and that the smallest file shown in the specification is identical to `values/plain-speaking/VALUES.md`. |

Dependencies: `typer`, `ruamel.yaml` (YAML 1.2, and it reports duplicate keys), `jsonschema`
(draft 2020-12), and the Agent Skills reference library `skills-ref`, pinned to a commit, for
V8. The Markdown rules of part 3 (ATX headings, fences, the core section) are the standard's
own and are written by hand in a few dozen lines. They are deliberately not a full Markdown
parser.

The fixtures are the tests. There are no separate unit test files: a rule that is wrong shows
up as a fixture that gives the wrong outcome, and a rule with no fixture is a gap in the
fixtures.

### Decisions this plan makes

The spec left a few things to planning. Each is settled here so that implementation does not
have to decide it.

- **The Roman Catholic example has no MCP server.** A search on 2026-11-20 found Catholic MCP
  servers, none with the standing the spec asks for: a third-party wrapper around the
  Magisterium AI service, which needs the user's own API key, and several narrow ones (the
  liturgical calendar, a single encyclical, a general Christian-texts server). The example is
  text-backed, as the spec allows.
- **Its bundled text is the 1885 Baltimore Catechism No. 2**, from Project Gutenberg ebook
  14552, which is in the public domain in the United States. The Apostles' Creed is taken from
  the same book. Project Gutenberg's own header, licence and name are removed, as its terms ask
  when a text is redistributed. The Catechism of the Catholic Church and modern Bible
  translations are cited and linked, not reproduced. Phase 3 confirms the wording against the
  source file before anything is committed.
- **`example-islam` declares `prompt: omit` for its checkpoint.** The checkpoint was trained
  and evaluated with no system prompt, and running it under a value-system prompt is untested,
  so `omit` is the only value that claims nothing unproved. The spec's recommendation was
  `optional` once issue #2 has tested the combination. That test does not exist yet. The value
  changes when it does.
- **`example-islam` has `tradition: [Islam]`** unless the architect relays that `[Islam, Sunni]`
  is right. Raised at the plan gate.
- **No licence file is added and the examples carry no `license` field** until the owner
  answers the spec's open question on the licence for everything that is not the specification
  text. `spec/README.md` states that the text is CC BY 4.0, which is decided. Raised at the
  plan gate.
- **The symbolic-link fixture for V9 is built at run time** in a temporary directory by the
  `fixtures` command, because a link committed to git does not survive every checkout.
- **Fixture files keep their exact bytes.** A `.gitattributes` in `spec/fixtures/` turns off
  line-ending conversion, since one fixture exists to test CRLF.

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
part 3 and applies V1 to V6 with the three outcomes of part 11.

#### Files to Create / Modify

- `spec/schema/values.schema.json`
- `spec/prompts/wrapper.txt`, `spec/prompts/reminder.txt`, `spec/prompts/preamble.txt`
- `spec/checker/pyproject.toml`, `spec/checker/uv.lock`
- `spec/checker/values_checker/__init__.py`, `__main__.py`, `cli.py`, `reading.py`, `rules.py`
- `spec/fixtures/.gitattributes`, `spec/fixtures/fixtures.json`
- `spec/fixtures/valid/…` and `spec/fixtures/invalid/…`, file-scope fixtures only

#### Deliverables

- [ ] The schema, in JSON Schema draft 2020-12, carrying every field rule of parts 2 and 6:
      requiredness, bounds, the `steward.url` condition, the three `claim` values, the three
      `prompt` values, unknown keys allowed at the top level and refused inside `steward`,
      `persistence`, `persistence.reinject` and a `models` entry, and `metadata` with any JSON
      value. No `access` field.
- [ ] The three normative texts, word for word as in part 4, each ending in exactly one line
      feed.
- [ ] `reading.py`: encoding, line endings, frontmatter split, YAML 1.2 parse with duplicate
      keys, anchors and aliases refused, body trim, code-point counts, ATX headings outside
      fences, heading text, core resolution.
- [ ] `rules.py`: V1 to V6, and the "unsupported version" outcome for a well-formed
      `spec-version` other than `"0.1"`.
- [ ] `check` and `fixtures` commands.
- [ ] File fixtures, each listed in `fixtures.json` with its expected outcome and rule
      identifiers:
  - valid: the smallest file; a file with every optional field; a long body with a core
    section; a custom core heading matched without regard to case; a short body with a core
    section; an unknown top-level key; a CRLF file; a model entry with `prompt: omit`;
    `claim: individual` with no URL; a body containing the text `{name}`.
  - V1: wrong file name; no frontmatter; frontmatter over 8,000 characters.
  - V2: duplicate key; an anchor and alias; frontmatter that is a list.
  - V3: missing `name`; missing `steward`; malformed `name`; missing `steward.claim`;
    `official` with no `url`; unknown key inside `steward`; `every-tokens` of 500; a model
    entry without `base`; `prompt: sometimes`; unknown key inside a model entry.
  - V4: empty body; body over 7,500 characters.
  - V5: long body with no core section; two matching headings; core over 1,500 characters;
    empty core; the only `## Core` line inside a code fence in a long body; a Setext "Core"
    heading in a long body.
  - V6: `</values>`; `</VALUES >`; an opening `<value-system-reminder`.
  - unsupported version: `spec-version: "0.2"`.

#### Acceptance Criteria

- [ ] `uv run --project spec/checker python -m values_checker fixtures` exits zero, and every
      file fixture gives its labelled outcome with no network access.
- [ ] Every rule V1 to V6 has at least one invalid fixture, and every fixture named in the
      spec's success criteria for V3 and V5 exists.
- [ ] The schema validates against the draft 2020-12 meta-schema.
- [ ] The fixed text of `wrapper.txt`, with placeholders removed, is 1,504 characters, as part
      4 states. If the count differs, the text was copied wrongly.
- [ ] The CRLF fixture and its LF twin give the same body, core and counts.

#### Test Plan

- Run the `fixtures` command with the network disabled.
- Break one rule on purpose in a scratch copy of the checker (for example, stop excluding
  fences) and confirm that a fixture fails. This shows the fixtures can catch a wrong rule.
- Run `check` by hand on the smallest file and on two invalid fixtures, and read the output a
  person would see.

### Phase 2: Folder and collection validity, rendering and the marketplace mapping

**Dependencies**: Phase 1

#### Objective

Extend the checker from a file to a folder and to a collection, add rendering, and add the
mapping to a Claude Code marketplace entry, so that every mechanical rule in the standard can
be run.

#### Files to Create / Modify

- `spec/checker/values_checker/rules.py` (V7 to V10), `render.py`, `marketplace.py`, `cli.py`
- `spec/checker/pyproject.toml`, `spec/checker/uv.lock` (adds the pinned `skills-ref`)
- `spec/fixtures/fixtures.json`
- `spec/fixtures/valid/…/expected/wrapper.txt` and `reminder.txt` for every valid fixture
- `spec/fixtures/valid/…` and `invalid/…` folder fixtures, `spec/fixtures/collections/…`

#### Deliverables

- [ ] V7: the shape of `.mcp.json` from part 7.
- [ ] V8: every folder under `skills/` checked with the Agent Skills reference library.
- [ ] V9: no symbolic links.
- [ ] V10: folder name equals `name`, and names are unique in a collection.
- [ ] `render`: single-pass placeholder substitution, trimmed body and core, one final line
      feed.
- [ ] `marketplace`: the mapping table of part 12, including the fixed sentence appended to the
      description, the `author` object, tag order with repeats removed, absent fields left out,
      and `source` as the path from the marketplace root.
- [ ] Folder fixtures:
  - valid: a package with a remote server (this is the fixture the specification's worked
    example uses); a package with a local server; a package with a skill and `references/`.
  - V7: both `url` and `command`; neither; an `http` address; `headers` present; a bad server
    name; a file that is not a JSON object.
  - V8: a skill with a missing `description`; a skill whose name does not match its folder.
  - V9: a symbolic link, built at run time.
- [ ] Collection fixtures: a valid collection of two packages; one whose folder name differs
      from its `name` (V10); one with a duplicated name (V10).
- [ ] An expected wrapper and reminder for every valid fixture, and an expected marketplace
      entry for the valid collection.
- [ ] A fixture with the longest name, steward name and body, whose rendered wrapper must be
      9,432 characters.

#### Acceptance Criteria

- [ ] The `fixtures` command exits zero with every rule V1 to V10 covered by at least one
      invalid fixture, and every V7 branch named in the spec's success criteria present.
- [ ] Every valid fixture renders to exactly its expected wrapper and reminder.
- [ ] The marketplace entries for the valid collection equal the expected ones.
- [ ] `check` on the collection fixtures reports V10 for the right package.

#### Test Plan

- Run the `fixtures` command with the network disabled.
- Write the expected renderings for two fixtures by hand from part 4 before running `render`,
  then compare. This keeps the expectations from being a copy of the program's own output.
- Check the size-budget fixture's length independently with a one-line count.

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

#### Deliverables

- [ ] `plain-speaking`: the file from the top of the spec, unchanged.
- [ ] `example-principled-pluralism`: a short body that states the value system's own position
      as the essay gives it, cites the essay, and carries the "illustrative, not endorsed by
      its author" notice.
- [ ] `example-islam`: a body that keeps to high-consensus basics and sends rulings, verses and
      hadith to Ansari; `.mcp.json` declaring `https://mcp.ansari.chat/mcp`; the model entry
      from part 13 with `prompt: omit` and a `description`; `languages: [en]`.
- [ ] `example-roman-catholic`: a body that keeps to high-consensus basics; a self-contained
      skill that answers basic questions from the bundled catechism and points to the current
      Catechism online; the Apostles' Creed and a list of sources in `references/`. Every
      bundled text states its source and the basis for its public-domain status.
- [ ] The three `example-` packages name the values.md project as steward with the claim
      `organization`, and carry their notice in the description, the body and the README.
- [ ] No copy of any package under `spec/`.

#### Acceptance Criteria

- [ ] `check values/` reports every package valid, with no network access.
- [ ] Every body is at most 7,500 characters and every core at most 1,500. (`check` enforces
      this. The numbers are also recorded in the review.)
- [ ] The Ansari server answers `initialize` and lists `answer_islamic_question`, and the date
      is recorded.
- [ ] The skill passes `skills-ref validate`.
- [ ] A temporary copy of each folder example, with only `.claude-plugin/plugin.json` added,
      passes `claude plugin validate` and loads in Claude Code with its skill or MCP server
      available.
- [ ] A marketplace file generated for `values/` passes `claude plugin validate`, and one
      example installs from it in Claude Code with no `plugin.json` in its folder.
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
- A check that cannot be run, for whatever reason, is reported as not verified. This applies
  in particular to loading the Islam example's checkpoint from a second account, which needs
  provider access this project does not have.

### Phase 4: The specification text

**Dependencies**: Phases 1, 2 and 3

#### Objective

Write the standard as a document a host developer or a package author can implement from, and
tie it to the machine-readable parts so that the two stay the same.

#### Files to Create / Modify

- `spec/specification.md`
- `spec/README.md`
- `spec/checker/values_checker/consistency.py`, `cli.py`

#### Deliverables

- [ ] `specification.md`, in RFC 2119 language, covering parts 1 to 12:
  - an opening that shows the smallest valid file in full and the two lists of what a
    first-time author and a Level 1 host can ignore;
  - package shape; frontmatter with the field table; reading rules, body, prompt and core; the
    three normative texts quoted; prompt fade and reinjection; fine-tuned models with the
    `prompt` field, the three modes, who chooses and what the user is shown; tools, the shape
    of `.mcp.json`, consent, and conformance levels; discovery and installation; provenance;
    more than one value system; validity with rules V1 to V10, scopes and outcomes;
    collections, listings and the marketplace mapping;
  - a security section making the six points of part 8;
  - a worked example of the exact messages a Level 2 host sends for the remote-server fixture,
    including the first reminder at the default placement;
  - the conformance tests for hosts that the spec lists as "defined here, exercised by a
    host", stated as numbered requirements.
- [ ] Each of the issue's eight questions answered in a section a reader can find, with a short
      table at the end pointing to each.
- [ ] `spec/README.md`: what each file is, the command that runs every check, and the licence
      of the text.
- [ ] The `consistency` command.
- [ ] No mention of principled pluralism outside the list of examples.

#### Acceptance Criteria

- [ ] `consistency` exits zero: every field in the specification's table is in the schema with
      the same requiredness and limits and the reverse; every quoted normative text equals its
      file; the smallest file shown equals `values/plain-speaking/VALUES.md`.
- [ ] The messages in the worked example equal what `render` produces for that fixture.
- [ ] An agent given only `spec/` and one package from `values/` produces the correct rendered
      wrapper and reminder and says when the first reminder is due.
- [ ] The smallest valid file shown is no more than 12 lines.
- [ ] `fixtures` and `check values/` still exit zero.

#### Test Plan

- Run `consistency`, `fixtures` and `check values/`.
- The cold-reader test: start an agent with no context but `spec/` and one package, ask for
  the rendered wrapper, the rendered reminder and the point at which the first reminder
  falls, and compare with `render` and with the worked example. Where it goes wrong, fix the
  text, not the agent, and run it again with a fresh agent.
- Read the specification against the spec's part 18 table and tick each of the eight
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
- [ ] `consistency`, `fixtures` and `check values/` still exit zero.

#### Test Plan

- Re-fetch each cited page and compare it with the claim made.
- Compare the worked marketplace file with the command's output.
- Search both documents, and all of `spec/`, for the words "principled pluralism" and confirm
  where they appear.
- Go through the spec's Success Criteria one by one and record, for each, the command or
  observation that shows it is met, or that it could not be verified.

## How the spec's success criteria map to phases

| Criterion (short form) | Phase |
|---|---|
| Deliverables present under `spec/` and `values/`, nothing else changed | 5 |
| Examples exist once, in `values/`, and are valid there | 3 |
| Specification opens with the smallest file and the two lists | 4 |
| Eight questions answered | 4 |
| Security section | 4 |
| Field table and schema agree; unknown-key rules | 1 (schema), 4 (agreement) |
| Schema is valid draft 2020-12 | 1 |
| Rules V1 to V10, scopes, outcomes, fixtures for each | 1 and 2 |
| V3, V5, V7 fixture lists; unsupported-version fixture | 1 and 2 |
| Rules applied to every fixture offline give the labelled result | 1 and 2 |
| Normative texts as files, quoted copies identical | 1 (files), 4 (identity) |
| Valid fixtures render exactly | 2 |
| Body and core limits for the examples | 3 |
| Cold-reader test | 4 |
| Worked example for a Level 2 host | 4 |
| Ansari server declared and answering | 3 |
| Notices on the three `example-` packages | 3 |
| Claude Code plugin and marketplace checks | 3 |
| Skills pass `skills-ref validate` | 3 |
| Rationale content, links and dates | 5 |
| No bundled text under third-party copyright | 3 |
| Principled pluralism is an ordinary example | 3, 4 and 5 |
| `prompt` values in the schema; modes in the specification | 1 and 4 |
| `example-islam` declares the stage 2 checkpoint | 3 |
| Second-account load test recorded or reported not verified | 3 |
| Checker in its own directory, one command, offline | 1 |
| No loader or chatbot code | 5 (final check) |

## Risks and Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| The checker and the specification text describe different rules. | Medium | High | The checker is written first from the approved spec. The specification is then checked against the schema and the prompt files by the `consistency` command, and against rendering by the worked example. |
| Expected renderings are just the program's own output, so they prove nothing. | Medium | Medium | Two are written by hand from part 4 before `render` runs. The cold-reader test in Phase 4 is a second, independent implementation. |
| Claude Code does not ignore `VALUES.md` or `references/` at a plugin root, or does not take a wrapped `.mcp.json`. | Low | High | Tested in Phase 3. A failure goes to the architect at once, because it touches the owner's decision that a package installs in Claude Code unchanged. |
| An example misstates a tradition or the essay. | Medium | High | Bodies are short and keep to high-consensus basics. Each statement is traced to a source in Phase 3, and the notices say plainly that nobody with authority has endorsed the text. |
| The public-domain status of a bundled text is less clear than it looks. | Low | Medium | Only the 1885 Baltimore Catechism is bundled, from a Project Gutenberg edition marked public domain in the United States. Anything else is cited and linked. |
| `skills-ref`, pinned from a git repository, cannot be fetched when the checker is installed. | Low | Medium | The commit is pinned and the lock file is committed. If it cannot be installed, V8 is reported as not verified and the architect is told. |
| Porch's build and test checks assume a different kind of project. | Medium | Low | The checker has one command that runs everything. If a porch check needs pointing at it, that is done through `porch.checks` in the Codev configuration, not by changing porch state. |
| The Ansari server is down when Phase 3 runs. | Low | Low | Validity does not depend on it. The probe is retried, and if it still fails the criterion is reported as not verified. |
| The examples' licence is still undecided when Phase 3 commits. | Medium | Low | The examples carry no `license` field and no licence file is added until the owner answers. The review says so. |

## Documentation Updates

- `spec/README.md` is new and is the index for everything under `spec/`.
- Each `example-` package has its own `README.md`.
- `codev/resources/arch.md` and `codev/resources/lessons-learned.md` are still placeholders.
  They are filled in during the review phase, once there is an architecture and there are
  lessons to record.
- No README is added at the root of the repository. The spec limits this project to `spec/`
  and `values/`. The repository is public and has none, which is worth the architect's
  attention separately.
