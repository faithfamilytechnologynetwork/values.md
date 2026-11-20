# Rebuttal: specify, iteration 1

Verdicts: Gemini approve, Codex request changes, Claude request changes.

Every point was accepted. No reviewer disputed the design. The findings were gaps in precision,
and the spec was revised in commit `6dfe6fd`. Part numbers below refer to the Desired State
section of `codev/specs/1-values-md-standard-v0-1-the-va.md`.

Both request-changes reviews carry a "repository moved" warning. The move was my own commit
`ec0b8cb`, made while the reviews ran (confirmed in the reflog). It added the "format at a
glance" block and open question 4. The reviewers read the commit before it, `30b9fb5`. Nothing
else changed the branch.

## Codex

| Point | Response |
|---|---|
| Core extraction is not deterministic: heading inclusion, heading forms, fences, whitespace, body boundaries, character counting, YAML version, duplicate keys, the exact prohibited tags. | Changed. Part 3 now fixes eight reading rules: UTF-8 with CRLF turned into LF, frontmatter delimiters, YAML 1.2 core schema with no duplicate keys, anchors or aliases, the body trimmed, characters as code points, ATX headings only and never inside a fence, how heading text is taken, and the core as the text after the heading line. The reserved text is defined as an exact pattern, matched without regard to case, covering opening and closing tags. |
| V7 does not define valid `.mcp.json` server objects. | Changed. Part 7 defines the shape: a server is remote (`url` beginning `https://`, optional `type`) or local (`command`, optional `args` and `env`), never both and never neither. Server names are bounded. `headers` is not allowed in v0.1. Other keys are ignored. A success criterion requires a fixture for each branch. |
| Security boundaries: symlinks, paths escaping the package, consent before network or command, untrusted tool and reference content. | Changed. Part 1 forbids symbolic links and reading outside the folder, and new rule V9 checks the first. Part 7 requires consent per package and per server before a first connection and before starting a local command, and says tool output, skills and reference texts are untrusted. The specification text must carry a security section (part 8, deliverable 1, and a success criterion). |
| Multiple systems: "at most one reminder at a boundary" conflicts with reinjecting every due core. | Changed. Part 10: each package has its own count and interval, every due package gets its reminder in activation order, and the limit is one reminder per package per boundary. A fine-tuned model lets the host skip reinjection for the package that declares it and no other. Two packages with one name are never active together. |
| Schema and marketplace mapping under-specified: SemVer, bounds, `context-window`, omission rules, `author` shape, tag order, frontmatter size. | Changed. Part 2 gives bounds for every list and string field and names Semantic Versioning 2.0.0. Part 6 bounds the model fields. Frontmatter is at most 8,000 characters. Part 12 states the `author` shape, the tag order with duplicates removed, and that an absent optional field is left out. |

## Claude

| Point | Response |
|---|---|
| 1. Decision 5 is narrowed (core, not prompt) without asking. | Changed, and already raised by the architect. It is critical open question 4, with a cost table and three choices. |
| 2. V6's forbidden set is undefined, and it is not a security boundary. | Changed. Part 3 defines the pattern exactly, including opening tags and whitespace, and says in terms that it is hygiene and not a security boundary. |
| 3. V2 contradicts the unknown-key scenario unless the schema permits unknown keys. | Changed. Part 2: unknown keys are allowed at the top level and refused inside `steward`, `persistence`, `persistence.reinject` and a `models` entry. A success criterion checks both. |
| 4. Body and core extraction needs normalization rules. | Changed. See the first Codex row. The case of a short body that has a core section is now stated: the section is the core. |
| 5. A third of the scenarios cannot run in a code-free deliverable, and it is unclear whether a checking script is in scope. | Changed. Test Scenarios is split into "checked in this project" and "defined here, exercised by a host (issue #2)". New part 17 explains the split. Whether a small self-test may live in `spec/` is now critical open question 3, with a recommendation, because the plan depends on it. Tool availability is recorded as an assumption, and a criterion that cannot be run is reported as not verified. |
| 6. The promised security section is not a deliverable. "Never executes anything" is contradicted by local MCP commands. The marketplace mapping drops the claim. | Changed. The security section is in deliverable 1 and the success criteria. Part 1 now says installing runs nothing and that a local server command is the one thing a host may execute, under a must-have-consent rule in part 7. The mapping puts the claim into the entry's description through a fixed sentence, and the compatibility note must say that this is weaker than what part 9 asks of a host. The `author` shape is stated. |
| 7. No fallback for redistributable Catholic texts. The hook cap leaves about 400 characters of headroom and overflows for two packages. | Changed. Part 13 names the candidate texts and the fallback, which is to cite and link a text whose status cannot be shown. The body limit drops from 8,000 to 7,500 characters, so a worst-case rendered wrapper is 9,432 characters, and part 4 shows the arithmetic. Part 15 says the adapter emits one hook output per package and refuses on overflow. |
| 8a. "Invalid" and "unsupported version" are conflated. | Changed. Part 11 gives three outcomes. A well-formed later `spec-version` gives "unsupported version", which is not a rule failure. |
| 8b. `metadata` is string to string, yet it is the only extension space. | Changed. `metadata` takes any JSON value. Raised as important open question 16, since it differs from Agent Skills. |
| 8c. The model matching rule is undefined. | Changed. Part 6: same provider and an exact match on the `base` string. |
| 8d. Loopback `http` addresses. | Changed. Part 7: an `http://` address is invalid, loopback included. A local server is declared by its command. |
| 8e. Validation scopes are not stated. | Changed. Part 11 gives file, folder and collection scopes and the scope of each rule. |
| 8f. Duplicate names among active packages. | Changed. Part 10: the host refuses the second. |
| 8g. `tradition` is free-case and will not group. | Changed. Part 2: compared without regard to case, and any controlled vocabulary belongs to the collection. |
| 8h. Deliverable 1 covers parts 1 to 12 but the criterion asks for part 16 as well. | Changed. The rationale carries part 16, and the criterion says so. |
| 8i. "The issue's eight questions" are not enumerated. | Changed. New part 18 lists them with the part that answers each. |
| 8j. The no-changes-outside-`spec/` criterion conflicts with a possible root licence file. | Changed. The criterion allows a root licence file if the owner asks for one. |
| 8k. The `plugin.json` criterion cannot apply to the single-file example. | Changed. It is scoped to folder examples. |
| 8l. Part 13 states the checkpoint and the minimal example as decided while open questions ask permission. | Changed. Both are phrased conditionally and point at their open questions. |
| 8m. The reinjection placement branch makes the worked example irreproducible. | Changed. Part 5 has one default placement, at the start of the next user message, with the mid-conversation system message as an option. The worked example uses the default. |

## Gemini

Approved. Its suggestions were taken with the others: code points and line endings, the core
excluding its heading line, trimming around `{body}` and `{core}`, a case-insensitive reserved
text check that also covers opening tags, independent counters per package, and leaving absent
optional fields out of a marketplace entry.

## One point where I went further than asked

Claude suggested stating an overhead budget for the hook cap. I also lowered the body limit to
7,500 characters, because at 8,000 the worst case came to 9,932 and one sentence added to the
wrapper would have broken it. The limit is an important open question for the owner either way.
