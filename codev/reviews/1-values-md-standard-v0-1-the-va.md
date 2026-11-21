# Review: values.md standard v0.1 — the VALUES.md package format

## Summary

Version 0.1 of the values.md standard was written in five phases: the frontmatter schema, the
three injected texts and a checker with file fixtures; folder and collection rules, rendering
and the Claude Code marketplace mapping; four example packages in `values/`; the
specification text; and the rationale, the compatibility note and a root README. On the final
tree all four checker commands exit zero (255 fixtures, 22 deliberate breaks, the document
consistency check, and the four packages in `values/` valid). Every success criterion is
accounted for below. Several things that need a host, a second provider account or a model
session were not verified, and they are listed.

## Spec Compliance

The criteria are the spec's Success Criteria, in its order. "Run" means run again on the
final tree for this review. Results from earlier phases give the phase.

- [x] **Deliverables present under `spec/` and `values/`; nothing else changes except Codev
  files and a root licence.** `git diff --name-only origin/main...HEAD` touches only `spec/`,
  `values/`, `codev/`, `.codev/config.json`, `LICENSE` and `README.md`. The root README was
  added at the owner's request at the plan gate. (Phase 5)
- [x] **The four examples exist once, in `values/`; `spec/` holds no copy and refers by
  path.** The one copy is the smallest file at the top of the specification, which
  `consistency` compares with `values/plain-speaking/VALUES.md`. (Phases 3 and 4)
- [x] **`values/` is valid as a collection with no network access.** Run: `check values/`
  reports all four valid. In phase 3 it was also run once in a process whose socket creation
  raises, with the same result. The `check` command itself has no network guard. The guard is
  in `fixtures`, where the plan puts it. (Phase 3)
- [x] **The specification opens with the smallest valid file, at most 12 lines, and the two
  "can ignore" lists; the file is identical to `values/plain-speaking/VALUES.md`.** The file
  is 10 lines. Identity is checked by `consistency`. (Phase 4)
- [x] **The eight questions are each answered in an identifiable section.** Part 17 of
  `spec/specification.md` lists them with the part that answers each. (Phase 4)
- [x] **The security section makes the six points.** Part 13, six numbered points, compared
  one by one with the spec's list for this review. (Phase 4)
- [x] **Field table and schema agree; unknown keys allowed at the top level and refused in
  the four nested objects.** `consistency` compares the table with the schema in both
  directions, word for word. Fixture `valid/unknown-top-level-key` and the
  `additionalProperties` fixtures cover the key rules. (Phases 1 and 4)
- [x] **The schema is valid JSON Schema draft 2020-12.** Run: `Draft202012Validator.check_schema`
  accepts `values.schema.json` and `mcp.schema.json`. (Phase 1)
- [x] **Rules V1 to V10 with identifiers, scopes and three outcomes; a valid fixture and an
  invalid fixture for each rule.** Part 11. The `fixtures` audit fails if any rule has no
  invalid fixture. 255 fixtures: 56 valid, 188 invalid, 4 unsupported version, 7 collections.
  (Phases 1 and 2)
- [x] **The V3 fixture list.** Present by name: `v3-missing-name`, `v3-missing-steward`,
  `v3-name-uppercase` and four more malformed names, `v3-steward-missing-claim`,
  `v3-official-no-url`, `v3-steward-unknown-key`, `v3-every-tokens-too-small`,
  `v3-model-missing-base`, and `valid/unknown-top-level-key`. (Phase 1)
- [x] **The V5 fixture list.** `v5-no-core-section`, `v5-two-core-sections`,
  `v5-core-too-long`, `v5-core-only-in-fence`, `v5-setext-core`, and `valid/crlf`, which is
  valid only after line endings are normalised. (Phase 1)
- [x] **The V7 fixtures cover each branch.** Valid remote and local servers,
  `v7-url-and-command`, `v7-neither-url-nor-command`, `v7-http-address`, `v7-http-loopback`,
  `v7-headers` and three bad server names. The schema audit requires every constraint
  in `mcp.schema.json` to reject a fixture. (Phase 2)
- [x] **`spec-version: "0.2"` gives "unsupported version".** `unsupported/later-minor-version`
  and three others. (Phase 1)
- [x] **Every fixture, with no network, gives the labelled result.** Run: `fixtures` passes
  with socket creation blocked. (Phases 1 and 2)
- [x] **The wrapper, reminder and preamble are standalone files and every quoted copy in
  `spec/` is identical.** `spec/prompts/`. `consistency` checks every fenced block that opens
  with a tag of the injected prompt. The rationale and the compatibility note quote none of
  the three. (Phases 1, 4 and 5)
- [x] **Each valid fixture has an expected wrapper and reminder and renders to them exactly.**
  Run: `fixtures`. The expected files were made from the normative texts separately from
  `render`, and two were typed by hand first. (Phase 2)
- [x] **Example bodies at most 7,500 characters and cores at most 1,500.** Run: body / core
  are 203 / 203, 1,382 / 1,382, 2,758 / 643 and 3,722 / 748. (Phase 3)
- [x] **A cold reader can render a package and say when the first reminder is due.** Two
  fresh agents did, byte for byte. The record is under "Cold-reader test" below, with its
  limits. (Phase 4)
- [x] **Worked example of the exact messages a Level 2 host sends, with the first reminder at
  the start of the user message.** Part 14, on the `remote-server` fixture. Its two quoted
  renderings carry `values-md:rendering` markers. (Phase 4)
- [x] **(tool) `example-islam` declares the Ansari MCP server, and the review records when it
  answered.** It answered `initialize` (protocol `2024-11-05`, server "Ansari" 1.0.0) and
  listed `answer_islamic_question` at 02:53 to 02:54 UTC on 2026-11-21. (Phase 3)
- [x] **The three `example-` packages carry the notice in description, body and README and
  name the values.md project as steward.** Checked by search for this review. (Phase 3)
- [x] **(tool) A temporary copy of each folder example with only `plugin.json` added passes
  `claude plugin validate` and loads with its skills and servers available; the compatibility
  note says what Claude Code does not provide.** Passed with warnings on Claude Code 2.1.330.
  "Available" means listed and connected. No model session used the skill or the tool.
  Details under "Outside-tool results". (Phases 3 and 5)
- [x] **(tool) A generated `marketplace.json` passes `claude plugin validate` and an example
  installs from it with no `plugin.json`.** Both folder examples installed. The two
  single-file packages were not tried. (Phase 3)
- [x] **(tool) Every skill inside an example passes `skills-ref validate`.** The one skill,
  `catechism-answers`, is valid under the reference validator at commit `83021e2`. (Phase 3)
- [x] **The rationale covers the four options, compares the four formats and says why option
  3, with a link and a date for every claim.** `spec/rationale.md`. Every cited page was read
  again at the source on 2026-11-21 UTC, and every cited URL returned 200. (Phase 5)
- [x] **No bundled text is under third-party copyright, and each states its source and
  status.** The only bundled texts are the Baltimore Catechism No. 2 and the Apostles' Creed
  taken from it. See "Catechism source" below, which the owner has not yet answered. (Phase 3)
- [x] **`example-principled-pluralism` is valid, cites the essay and carries the notice;
  nothing else in `spec/` mentions principled pluralism.** A search of `spec/` and the root
  README finds the words once, as the package name in the examples table of part 16. The
  other mentions are the package name in the worked marketplace file and the root README's
  list of examples. (Phases 3, 4 and 5)
- [x] **The schema accepts `prompt` values `required`, `optional` and `omit` and no other;
  part 6 states the three modes, who chooses and what the user is shown.** (Phases 1 and 4)
- [x] **`example-islam` declares the stage 2 checkpoint as in part 13.** With `prompt: omit`,
  as the owner settled at the plan gate. (Phase 3)
- [x] **(tool) The review records whether the stage 2 checkpoint loads from another
  account.** Recorded here: **not verified.** There was no provider access to try it. The
  criterion asks for exactly this report when the test cannot be run. (Phase 3)
- [x] **The checker lives in its own directory, runs with one documented command, and needs
  no network for validity and rendering.** `spec/checker/`. A fresh clone ran the root
  README's command as written. (Phases 1 and 5)
- [x] **`spec/` contains no loader or chatbot code.** The checker's imports are the standard
  library, `typer`, `ruamel.yaml` and `jsonschema`. It has no HTTP or model client. `socket`
  is imported only to block it. (Phase 5)

### Not verified

- Loading the declared checkpoint from a second account. No provider access.
- The principled-pluralism essay was read through a fetch tool that returns short quotations
  and a summary, not the full text. The package keeps to paraphrase for that reason.
- No Claude Code model session used the example skill or the Ansari tool. "Available" means
  listed by `claude plugin details` and shown connected by `claude mcp list`.
- The cold readers were not run again after the part 5 wording was tightened in phase 4, and
  they never saw the last phase 4 commit.
- Neither prompt route in the compatibility note (hooks, forced output style) was built or
  run. The install screen was not looked at. Hooks in a marketplace entry were not tried.
  Installing the two single-file packages from a marketplace was not tried. Whether Claude
  Code asks for consent before connecting a plugin's MCP server was not checked.
- Whether the 10,000-character hook cap counts code points or UTF-16 units is not documented
  and was not tested. The standard counts code points.
- Whether context added by a hook survives a resume, a fork or a compaction is not documented
  and was not tested.
- Whether claude.ai or the Skills API rejects unknown skill frontmatter keys. The rationale
  makes no claim about either.

### Outside-tool results

All on 2026-11-21 UTC (2026-11-20 local), on temporary copies outside the repository.

- **Ansari MCP server.** See the criterion above. Each line under "The basics" in the Islam
  example, and its advice to take a personal ruling to a scholar, was put to the tool in
  three questions and confirmed. That is one source, not a scholar's review.
- **`skills-ref` at `83021e2`.** The example's skill is valid. On every skill folder in the
  fixtures the reference validator and the checker agree, with three cases that cannot be
  compared: the unsupported-version fixture and the linked fixture, where the checker by
  design does not judge the skill, and a directory named `SKILL.md`, where the reference
  stops with an error and no verdict. In phase 2 this cross-check could not be run. It was
  run in phase 3.
- **Claude Code 2.1.330** (the spec was written against 2.1.329). Copies of `example-islam`
  and `example-roman-catholic` with a name-only `plugin.json`: "Validation passed with
  warnings" (no version, description or author), with no warning about `VALUES.md` or
  `references/`. Loaded with `--plugin-dir`, `claude plugin details` lists the skill
  `catechism-answers` for one and the server `ansari` for the other, and `claude mcp list`
  shows `plugin:example-islam:ansari` connected. The worked marketplace file beside a copy of
  `values/` passes with one warning (no marketplace description), and both folder examples
  installed from a marketplace with no `plugin.json`, into a throwaway configuration
  directory. A copy of the fixture `invalid/v2-duplicate-key` with a `plugin.json` added also
  passes, and the output never mentions `VALUES.md`.
- **Sources read again with `curl`:** the Claude Code hooks, plugin manifest, marketplace and
  output-styles references, agents.md, the Agent Skills specification and client guide, the
  `skills-ref` validator, the Belief Protocol README and LICENSE, and the MCP home page.

### Cold-reader test

Two fresh agents were each given only `spec/specification.md`, the three files in
`spec/prompts/` and one package, and were told not to read the fixtures or the checker and
not to run the checker. Each wrote its own small program from the text.

| Package | Wrapper and reminder | Body / core | First reminder |
|---|---|---|---|
| `values/example-islam` (a `## Core` section) | Byte-identical to `render` | 2,758 / 643 | Start of the first user message added after the count reaches 5,000 tokens, as a block before the user's text |
| `values/example-principled-pluralism` (no core section, host with no tokenizer) | Byte-identical to `render` | 1,382 / 1,382 | First user message after a running total of 20,000 characters |

Neither went wrong. Both listed the same doubts about part 5, and the text was tightened
before the commit. The agents were not run again afterwards.

### Errata against the approved spec

Sent to the architect. The spec file was left as approved.

- **Reminder cost table.** The rationale has about 420 tokens and 8,400 where the spec's
  Solution Approaches has 415 and 8,300. The rationale counts the reminder's 149 fixed
  characters and a 13-character name at four characters to a token. Percentages do not change.
- **Belief Protocol.** Each belief carries `layer`, `grip` and `warrant` and records a
  `source`. The spec's "format at a glance" says `layer`, `grip` and `source`.

The spec's two measured figures for the wrapper held: 1,504 characters of fixed text and
9,432 for the worst case.

### Catechism source

The bundled catechism comes from Project Gutenberg ebook 14552. It is listed as public domain
in the United States and carries the 1885 approval, but its text follows a printing of 1977.
The transcription says answer 257 was rewritten for that printing, and a comparison of all
421 answers with the two sibling volumes (ebooks 14553 and 14554) showed answers 254 and 258
also differ in substance. The bundled copy keeps the thirty-seven lessons, has 421 questions
with the answers to 418 of them, marks the three left out, and leaves out the prayers and
hymns. Project Gutenberg is named nowhere in `values/`, because its terms ask that its name
and its licence go together or not at all. The package says the copy is a public-domain
transcription of a 1977 printing. This finding was sent to the architect in phase 3 and has
not been answered. If the owner wants the text removed or taken from another source, that
is a change to make before or after merge.

### Commits no reviewer saw

Each was made after the last review round of its phase.

| Commit | Phase | What it changed |
|---|---|---|
| `cd0a992` | 2 | A directory named `VALUES.md` or `SKILL.md` gives an invalid result, not a crash. Porch advanced the phase at its three-round ceiling with this fix unreviewed. |
| `9544811` | 3 | The round 1 comments on the example packages. |
| `4d15b33` | 4 | Part 10 states that an `omit` model is not used while a second value system is active; `consistency` reports an unknown schema keyword in a sentence. |
| `ecc2776` | 5 | Two wording edits in the compatibility note. |

## Deviations from Plan

### Phase 1

- A multi-line `description` is valid. The plan's fixture list said otherwise, but the spec's
  field table sets no one-line rule.
- The unsupported-version fixtures have their own `unsupported/` directory, since they are
  not invalid.
- The approved spec was silent on seven reading details, and the checker had to choose:
  whitespace for trimming is space, tab and line feed; case is compared for A to Z only; the
  frontmatter limit counts the text between the two `---` lines; the frontmatter may not hold
  a second document, an explicit tag, a non-string key or a non-finite number; a language tag
  is checked for well-formedness only; a steward `url` holds no whitespace and `trained-on`
  is a Semantic Versioning string; a backtick fence's opening line holds no other backtick.
  The architect confirmed these as built. Each is pinned by a fixture and stated in the
  specification.

### Phase 2

- The `skills-ref` cross-check on the V8 fixtures was not permitted to run in this phase. It
  was run in phase 3.
- Eight further silent points were settled the same way, among them: a server is remote when
  `url` is present and local when `command` is present; an empty `mcpServers` is valid; V7 to
  V9 are judged even when a file rule failed; when two packages share a name, both break V10.
- Added beyond the plan's wording, from review: nothing is read through a symbolic link, and
  a package folder that is itself a link breaks V9 at collection scope.
- Known limit, left alone: a `.mcp.json` nested many thousands of levels deep ends the run
  with an error and no verdict. The exit code is not zero. The standard sets no depth limit.

### Phase 3

- The catechism's source is a later printing than the plan assumed. See "Catechism source".
- `example-principled-pluralism` has no core section. Its body is under 1,500 characters, so
  the whole body is reinjected.
- The steward is named "The values.md project", with the article, because the wrapper opens
  a sentence with the name.

### Phase 4

- A small change to phase 1 code: `reading.fences` returns each fenced block's first and last
  line, because `consistency` needs the blocks themselves.
- Wording the approved spec left open was settled in the simplest deterministic way: a
  reminder is due when the count is equal to or greater than the interval; a host with no
  tokenizer counts four characters to a token; a model declared `omit` is not run with the
  prompt; the host conformance requirements are H1 to H10, one for each of the spec's
  scenarios 31 to 40.
- The cold readers were not run again after the part 5 edits.

### Phase 5

- The worked marketplace file in the compatibility note has no `consistency` marker, and the
  root README's copy of the smallest file has no automated check. Each was compared by script
  once and found identical. The note says its copy is not checked automatically. The plan
  asks for a comparison, and the architect's standing instruction was to add no check beyond
  the spec and plan.
- No source for prompt fade was found that could be checked, so the rationale presents the
  5,000-token interval as a design parameter and cites nothing.
- The reinjection cost table uses measured sizes. See "Errata".

## Consultation Feedback

The Gemini lane produced a review once, for the spec. In every later round its command line
(`agy`) exited with code 3 and porch recorded a non-blocking skip. Those rounds had two
reviewers, not three.

### Specify Phase (Round 1)

Two reviews carry a "repository moved" warning. The move was the builder's own commit, made
while the reviews ran.

#### Gemini (APPROVE)
- **Concern**: code points and line endings, the core excluding its heading line, trimming,
  a case-insensitive reserved-text check, independent counters per package, absent optional
  fields left out of a marketplace entry → **Addressed**: all taken with the other reviews.

#### Codex (REQUEST_CHANGES)
- **Concern**: core extraction is not deterministic → **Addressed**: part 3 fixes eight
  reading rules.
- **Concern**: V7 does not define a valid `.mcp.json` → **Addressed**: part 7 defines the
  shape.
- **Concern**: symbolic links, paths leaving the package, consent, untrusted content →
  **Addressed**: rule V9, a consent rule and a required security section.
- **Concern**: "one reminder at a boundary" conflicts with several due cores →
  **Addressed**: one reminder per package per boundary, in activation order.
- **Concern**: schema bounds and the marketplace mapping are under-specified →
  **Addressed**: bounds for every field and a stated mapping.

#### Claude (REQUEST_CHANGES)
- **Concern**: reinjecting the core narrows the owner's decision without asking →
  **Addressed**: raised as a critical question, and the owner confirmed core-only reinjection.
- **Concern**: the reserved text is undefined and is not a security boundary →
  **Addressed**: an exact pattern, described as hygiene.
- **Concern**: the unknown-key rule contradicts a scenario → **Addressed**: allowed at the
  top level, refused in nested objects.
- **Concern**: a third of the scenarios cannot run without code → **Addressed**: scenarios
  split into those checked here and those a host exercises, and the owner allowed a checker
  under `spec/`.
- **Concern**: the security section is not a deliverable, "never executes anything" is
  contradicted by local servers, and the mapping drops the steward's claim → **Addressed**.
- **Concern**: no fallback for Catholic texts, and too little room under the hook cap →
  **Addressed**: a named fallback, and the body limit lowered from 8,000 to 7,500 characters.
- **Concern**: thirteen smaller points (three outcomes, `metadata` type, model matching,
  loopback addresses, scopes, duplicate names, and others) → **Addressed**: all changed.

### Plan Phase (Round 1)

#### Gemini
- `CONSULT_ERROR`: lane skipped, no review.

#### Codex (REQUEST_CHANGES)
- **Concern**: the V3, reading-rule and V7 fixture lists omit many cases → **Addressed**:
  three mechanical audits, a second schema, and the named cases.
- **Concern**: no order of diagnostics or outcome precedence → **Addressed**: a fixed order
  of evaluation, accepted by the owner at the plan gate.
- **Concern**: phase 1 claims rendering that arrives in phase 2 → **Addressed**.
- **Concern**: the harness could pass with nothing to check → **Addressed**: `selftest`.

#### Claude (COMMENT)
- **Concern**: `skills-ref` as a hard dependency for V8 → **Addressed**: the checker
  implements the rules itself, with `skills-ref` as a cross-check.
- **Concern**: the CRLF fixture is vacuous; `spec-version` precedence; no mechanism for
  anchors and aliases; fixture gaps; several smaller points → **Addressed**.
- **Concern**: `prompt: omit` settles an owner-facing question → **Addressed**: put to the
  owner, who chose `omit`.
- **Concern**: Typer is optional and `argparse` would cut a dependency → **Rebutted**: Typer
  is the owner's standing choice for Python command lines.

### Phase 1 (Round 1)

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (REQUEST_CHANGES)
- **Concern**: the language pattern is not BCP 47 → **Addressed** in part: it is now the
  RFC 5646 grammar. **Rebutted** for a repeated variant, which is well formed and needs the
  registry to refuse.
- **Concern**: any text after `https://` passes as a URL → **Addressed**.
- **Concern**: "without regard to case" covers A to Z only, and "whitespace" is narrowed →
  **Rebutted**: the architect settled both as built.

#### Claude (APPROVE)
- **Concern**: reading decisions beyond the plan need relaying → **Addressed**: relayed, and
  stated in the specification in phase 4.
- **Concern**: whether `reinject` is required; a recursive reader crashes on deep nesting;
  `type` is not audited; a literal byte-order mark; the pattern guard rewrites only a final
  `$` → **Addressed**. The new `type` audit found a real defect at once.
- **Concern**: a multi-line `description` is valid against the plan's list → **Rebutted**:
  the spec sets no one-line rule.

### Phase 1 (Round 2)

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (REQUEST_CHANGES)
- **Concern**: the reserved-text check ignores case by Unicode rules → **Addressed**: ASCII
  only, pinned by a fixture.
- **Concern**: every explicit YAML tag is refused, core-schema tags included →
  **Rebutted**: confirmed by the architect, and stated in the specification.

#### Claude (APPROVE)
- **Concern**: `## Core#` is untested → **Addressed**: fixture added.
- **Concern**: `trained-on` as a Semantic Versioning string is a narrowing → **Rebutted**: it
  is a package version, which is defined as one.
- **Concern**: three smaller notes → **Addressed** or carried to phase 4.

### Phase 1 (Round 3)

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (APPROVE)
- No concerns raised.

#### Claude (APPROVE)
- **Concern**: the section name's limits are restated in code; the pattern guard covers `$`
  only; the constraint audit does not walk `oneOf` → **Addressed** in phase 2.
- **Concern**: schema failures are deduplicated by constraint path, so the printed output can
  name only the first offending field → **N/A**: deliberate, needed for the audit.

### Phase 2 (Round 1)

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (REQUEST_CHANGES)
- **Concern**: a package folder that is a symbolic link is accepted in a collection →
  **Addressed**.
- **Concern**: `--root` equal to the collection gives `././name` → **Addressed**.
- **Concern**: the `skills-ref` cross-check was not verified → **Addressed** in phase 3,
  when the command could be run.

#### Claude (APPROVE)
- **Concern**: non-ASCII skill names pass with no fixture; the preamble is never rendered →
  **Addressed**.

### Phase 2 (Round 2)

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (REQUEST_CHANGES)
- **Concern**: a directory named `.mcp.json` is treated as absent → **Addressed**.

#### Claude (APPROVE)
- **Concern**: mixed path handling in `marketplace`; V7 and V8 read through a symbolic link;
  lowercase `skill.md` accepted without a word → **Addressed**.
- **Concern**: the `---` split in a skill's frontmatter has no fixture → **Rebutted**: it is
  an accident of the reference validator, documented in a comment and not made part of this
  standard's tests.

### Phase 2 (Round 3)

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (REQUEST_CHANGES) and Claude (REQUEST_CHANGES)
- **Concern**: a directory named `VALUES.md`, and one named `SKILL.md`, crash the checker →
  **Addressed** in `cd0a992`. Porch advanced the phase at its three-round ceiling, so no
  reviewer saw this fix.
- **Concern** (Claude): a file named `skills`; a collection entry that links to a file →
  **Addressed**: stated and pinned.
- **Concern** (Claude): wrong-type suppression and server names → **Rebutted**: a bad name is
  reported at a different path, so both are reported.

### Phase 3 (Round 1)

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (COMMENT)
- **Concern**: "421 questions and answers" with three answers left out; the pluralism README
  says "`VALUES.md` and nothing else" → **Addressed** in `9544811`.

#### Claude (COMMENT)
- **Concern**: no record of the Claude Code and `skills-ref` checks → **Addressed**: recorded
  in this review under "Outside-tool results".
- **Concern**: the pluralism body is 22 characters from invalid → **Addressed**: now 1,382.
- **Concern**: no statement-by-statement trace to the essay → **Addressed**: a table in the
  package's README, and one phrase the essay does not support was removed.
- **Concern**: Project Gutenberg's name kept without its licence → **Addressed**: the name is
  removed from `values/`.
- **Concern**: mixed dates; the Catholic core lacks the "if you cannot open them" clause →
  **Addressed**.
- **Concern**: `check` has no network guard → **Rebutted**: the plan puts the guard in
  `fixtures`, and `check values/` was run once with sockets blocked.

### Phase 4 (Round 1)

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (REQUEST_CHANGES)
- **Concern**: `spec/README.md` puts itself under CC BY 4.0 → **Addressed**.

#### Claude (APPROVE)
- **Concern**: the cold-reader test is not recorded → **Addressed**: recorded above.
- **Concern**: a Level 1 host "can ignore `models`" against the duty to show them; whose
  reminder counts; a Level 1 host handed a folder with a linked `VALUES.md` → **Addressed**.

### Phase 4 (Round 2)

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (REQUEST_CHANGES)
- **Concern**: a Level 1 host must show tools it never reads → **Addressed**: every host
  shows the declared models, and a host that reads `.mcp.json` also shows the servers.

#### Claude (APPROVE)
- **Concern**: `consistency` checks a normative text only when a fenced block begins with its
  tag → **N/A**: the phase 5 documents quote none of the three texts.
- **Concern**: a renamed `specification.md` surfaces as a `KeyError` in `selftest` →
  **Rebutted**: `consistency` reports the missing marker by name in the same test run.

### Phase 4 (Round 3)

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (APPROVE)
- No concerns raised.

#### Claude (APPROVE)
- **Concern**: an `omit` model with two value systems active is derivable but unstated;
  `consistency` raises a traceback on an unknown schema keyword → **Addressed** in `4d15b33`,
  after the round.
- **Concern**: prose definitions of the forms are not checked against their regular
  expressions → **Rebutted**: the text says the schema settles any detail the words leave
  open.

### Phase 5 (Round 1)

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (REQUEST_CHANGES)
- **Concern**: a `SessionStart` hook that emits the wrapper on every firing can inject it
  twice → **Addressed**: a table by `source`, and a plain statement of what is undocumented
  and untried.

#### Claude (APPROVE)
- **Concern**: three "does not" statements carry no source marker; the licence sentence does
  not except bundled public-domain texts → **Addressed**.
- **Concern**: the worked marketplace file is hand-copied and unchecked → **Addressed** in
  the lighter form: the note says so. No marker was added.
- **Concern**: the root README's copy of the smallest file has no automated check →
  **Rebutted**: outside `spec/`, and a check the plan does not ask for. Compared by script.
- **Concern**: version drift, 2.1.329 against 2.1.330 → **N/A**: the tool updated between
  the two, and the note gives the version and date of what it observed.

### Phase 5 (Round 2)

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (APPROVE)
- No concerns raised.

#### Claude (APPROVE)
- **Concern**: one bullet lacks a source marker; "exactly" overstates the marketplace copy →
  **Addressed** in `ecc2776`, after the round.
- **Concern**: two figures in the rationale supersede the spec's → **N/A**: reported as
  errata, above.

### Review Phase (Round 1)

No code changed in response to this round. One reviewer's diff file was empty, so it reviewed
the files on disk.

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (REQUEST_CHANGES)
- **Concern**: a `.mcp.json` nested deeply enough makes the checker end with an error and no
  outcome, though the document may be valid → **Rebutted**, and put to the owner. The limit
  is real: 5,000 levels parse and 100,000 do not. It is stated in `spec/README.md` and in
  this review. The run exits non-zero, so a submission check fails closed. Calling such a
  file invalid would be a wrong verdict, and a depth limit would be a new rule of the
  standard, which the architect's standing instruction rules out without the owner's say. It
  is listed under Follow-up Items as a decision.
- **Concern**: many commits are `chore(porch): ...` and not in the `[Spec 1][Phase: ...]`
  form → **Rebutted**: those are porch's own state commits. Every commit the builder made
  carries the required form. Rewording them means rewriting a pushed branch, which is not the
  builder's to do. Squashing at merge is the owner's choice.

#### Claude (APPROVE)
- **Concern**: `LICENSE` holds only the MIT text while the documents say three files are
  CC BY 4.0 → **N/A** for the builder, and put to the owner. The owner settled at the plan
  gate that the root `LICENSE` carries the MIT text and that the two READMEs say which
  licence covers what. That is what was built. Whether `LICENSE` should also name the
  exceptions is listed under Follow-up Items.
- **Concern**: the thread file and the review records are untracked and not ignored →
  **N/A**: kept off the branch at the owner's request. Whether to add them back or ignore
  them is already a question for the owner before merge.
- **Concern**: the catechism comparison covers the answers, and other editorial changes in a
  1977 printing cannot be ruled out; keep it on the merge checklist → **Addressed**: it is
  the first item for the owner under Follow-up Items and is named in the pull request.
- **Concern**: `check` is the one command that does not block the network → **Rebutted**, as
  in phase 3: the plan puts the guard in `fixtures`, and the checker has no network client.
  Listed as an optional small item.
- **Concern**: `render.substitute` raises a bare `KeyError` for an unknown placeholder →
  **N/A**: offered as take-or-leave, and left. The three prompt files are fixed by the
  standard.
- The reviewer read the four unreviewed commits and found nothing that needed another round.

### Review Phase (Round 2)

Both rebuttals from round 1 were given to the reviewers. No code changed in this round.

#### Gemini
- `CONSULT_ERROR`: lane skipped.

#### Codex (APPROVE)
- No concerns raised.

#### Claude (APPROVE)
- The reviewer checked both disputed points against the tree and agreed with each rebuttal.
- **Concern**: a third way to handle a deeply nested `.mcp.json`: catch the reader's
  recursion error and print a plain "could not judge" message with a non-zero exit, in place
  of a traceback. It adds no rule and keeps today's outcome → **N/A** in this pull request:
  offered as optional and not blocking, and making it now would add code no reviewer has
  seen. It is listed under Follow-up Items as the third option for the owner.
- **Concern**: the untracked records, the catechism and the `LICENSE` wording stay on the
  merge checklist → **N/A**: all three are already listed for the owner.

## Lessons Learned

### What Went Well

- Building the checker and fixtures first gave every later phase something to run, and
  turned each silent point in the spec into a fixture that needed an outcome.
- The three audits and `selftest` caught real gaps: the `type` audit found a schema defect on
  its first run.
- The cold-reader test produced byte-identical renderings from the text alone, which is the
  strongest evidence that the specification can be implemented without the checker.
- Reading the cited pages again at the source changed the documents: the behaviour over the
  hook cap, where a hook's text is placed, and one of Belief Protocol's attribute names.

### Challenges Encountered

- **The approved spec was silent on more than twenty reading and evaluation details.** Each
  was settled the simplest deterministic way, pinned by a fixture, confirmed by the architect
  where it mattered, and written into the specification in phase 4.
- **Phase 2 took three rounds and ran out.** Each round found one more input the checker read
  wrongly or crashed on (a linked folder, a directory where a file belongs). Porch advanced
  at its ceiling with the last fix unreviewed.
- **The catechism was not the edition its title page gives.** Comparing every answer with two
  sibling volumes found three that differ in substance. They are left out and marked.
- **Reviewers could not see the evidence.** The thread file is untracked at the owner's
  request, and the reviewers had no shell. Records were copied into each round's response
  and are in this document.

### What Would Be Done Differently

- Test every "file expected" path with a directory, and the reverse, in the first build of a
  phase, not after a reviewer finds each one.
- Put outside-tool results in a tracked file from the start, so a reviewer can read them.
- Never commit while consultations are running. It happened once, in the specify phase.
- Read a source in full before planning around it. The essay and the catechism edition were
  both known less well than the plan assumed.

### Methodology Improvements

- A skipped review lane is recorded as a COMMENT verdict and nothing more. The Gemini lane
  was skipped in every round from the plan onward, so the "3-way" review was two-way for the
  whole implementation. Porch could say so loudly, or stop until the lane is fixed.
- When porch force-advances at the round ceiling with reviewers still asking for changes, the
  last fix is never reviewed. A final check of that one commit would close the gap. The same
  holds for comments taken after an approving round.
- Reviewers without a shell cannot run the tests they are asked to judge. Giving a reviewer
  the output of porch's own test check would save a note in almost every round.
- The review phase's default `e2e_tests` check runs `npm` in a repository that has none and
  passes by printing "skipped". It could read the project's configured checks.
- A second `porch next` acknowledges a task and its instructions are gone. Printing the task
  again on request would help.

## Architecture Updates

The four governance files were starters. They now hold real content.

- Routed: cold — `codev/resources/arch.md` — written from scratch: repository layout, single
  sources of truth, the checker, fixtures and audits, document consistency, the collection,
  the checks porch runs, licences, and verified-wrong assumptions about Claude Code, the YAML
  library and the Agent Skills validator.
- Routed: hot — `codev/resources/arch-critical.md` — ten one-line facts (single sources for
  the injected texts, the schema and field table, and the packages; fixtures as the test
  suite with exact bytes; no network or model code in the checker; no reading through links;
  the four test commands; public-facing writing; licences) and a map of all nine sections of
  `arch.md`. The file is at its cap of ten facts, so nothing was demoted.

## Lessons Learned Updates

- Routed: cold — `codev/resources/lessons-learned.md` — written from scratch in five
  sections: writing a standard, tests that can fail, outside tools and sources, working with
  reviewers, and public repository hygiene.
- Routed: hot — `codev/resources/lessons-critical.md` — the three seeded lessons are kept and
  six are added: settle an open edge case the simplest deterministic way and pin it; every
  check needs a deliberate break; read cited pages at the source and mark each claim; record
  "not verified" and do not work around a denial; do not commit during consultations and list
  unreviewed commits; put evidence where reviewers can read it. Nine of ten slots are used.

## Flaky Tests

No flaky tests encountered. The Gemini review lane was skipped in every round after the spec.
That is a reviewer that did not run, not a test.

## Follow-up Items

For the owner or architect to decide:

- The catechism finding: keep the 1977-printing text with three answers left out, replace
  the source, or drop the bundled text.
- The steward name "The values.md project".
- Whether the two errata are applied to the approved spec file.
- Whether the review records and the builder's thread file, kept off the branch at the
  owner's request, are added back before merge. If they stay off, an ignore rule would keep
  them from being committed by accident.
- Whether the root `LICENSE`, which holds the MIT text alone, should also name the three
  CC BY 4.0 documents and the bundled public-domain texts. A reviewer of the pull request
  asked for this before merge.
- What to do about a `.mcp.json` nested many thousands of levels deep, which today gets an
  error and no verdict. Three options came out of the pull request review: set a depth limit
  in the standard; make the checker read any depth; or keep the outcome and replace the
  traceback with a plain "could not judge" message, which is about three lines and adds no
  rule.

For the reference implementation (issue #2):

- Build and run the hook adapter. Test all five `SessionStart` sources, whether hook-added
  context survives resume, fork and compaction, and whether the cap counts code points or
  UTF-16 units.
- Check whether Claude Code asks for consent before connecting a plugin's MCP server, and
  look at the install screen.
- Use the example skill and the Ansari tool in a model session.
- Try the stage 2 checkpoint with a prompt on top. `example-islam` changes from
  `prompt: omit` to `optional` once that works.
- Load the checkpoint from a second account.

Smaller items:

- Fix the Gemini review lane (`agy` needs installing or signing in).
- Read the principled-pluralism essay in full and compare it with the package.
- Install the two single-file packages from a marketplace, and try hooks in a marketplace
  entry.
- Add the network guard to the `check` command, which two review rounds asked for. It is one
  line, and the plan did not ask for it.
- If `values/` changes, regenerate the worked marketplace file in `spec/compatibility.md`.
  An automatic check for it, and for the root README's copy of the smallest file, is not in
  place.
