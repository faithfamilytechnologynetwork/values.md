# spir-1 thread — values.md standard v0.1 (issue #1)

## 2026-11-20 — specify

- No spec existed, so I wrote one from the issue. The owner's eight decisions are copied into
  Constraints as fixed.
- Checked the issue's research notes against the sources. Differences worth knowing:
  - Ansari has a live hosted MCP server (`https://mcp.ansari.chat/mcp`, one tool,
    `answer_islamic_question`, no key). I called `initialize` and `tools/list` and both
    answered. Its repo has been quiet since 2025-09 and has no licence file. The Islam example
    declares it in `.mcp.json` and does not bundle the skill.
  - A Claude Code plugin manifest is optional, and a marketplace entry acts as the manifest
    when a folder has no `plugin.json`. So a package folder can be listed in a marketplace
    as it is.
  - Claude Code does not read `VALUES.md`. With only `plugin.json` added it gets the tools and
    skills, not the prompt. The prompt needs a hook adapter, which is code and belongs to #2.
    Raised as a critical open question.
  - The hooks 10,000-character cap and "no token counts" were read through a page summary
    only. Re-check before the compatibility note cites them.
  - "claude.ai rejects unknown skill frontmatter keys" was not verified. It does not affect the
    design.
- Main design calls, all with alternatives in the spec: whole body is the prompt and a named
  section is the reinjected core; limits in characters (body 8,000, core 1,500); a fine-tuned
  model replaces reinjection only, never the prompt; three host conformance levels with MCP as
  the tool floor; no ambient discovery; value systems are never merged.
- Architect instruction at 19:30Z: the registry (issue #3) needs things from the standard.
  Added: `steward.claim` (individual / organization / official), `tradition`, `languages`,
  `tags`, numbered validity rules V1 to V9 decided from files alone with fixtures, a
  collection definition (folder name equals `name`, unique), and a field-for-field mapping to a
  `marketplace.json` entry. Copied the instruction into Constraints as item 9.
- Checkpoint details from the comment on #2 are folded in: `models` entries gained a required
  `access` (public / restricted) plus optional `context-window` and `description`. The spec
  points at the issue comment for the `tinker://` paths and does not print them. Whether the
  public example may print them is a question for the owner.
- Principled pluralism: placed as guidance in the wrapper, credited in the rationale, nothing
  published under the name. Whether even citing it by name needs agreement first is a critical
  open question.

## 2026-11-20 — specify, after the 3-way review (iteration 1)

- Architect notes folded in before the reviews landed: the smallest valid `VALUES.md` is shown
  in full at the top with the two "can ignore" lists (the owner's test is "lighter than Belief
  Protocol"), and core-only reinjection is now critical open question 4 with a cost table,
  because the owner's words were "reinjects the prompt".
- Verdicts: Gemini approve, Codex request changes, Claude request changes. No reviewer
  disputed the design. All findings were precision gaps, and all were accepted:
  - Reading rules for the file are now fixed (line endings, YAML 1.2 with no duplicate keys,
    code points, ATX headings only, fences, heading line excluded from the core, trimming).
  - Reserved text is defined exactly and described as hygiene, not a security boundary.
  - Unknown keys: allowed at the top level, refused inside nested objects. `metadata` takes any
    JSON value.
  - `.mcp.json` shape is defined (remote or local, never both, no `headers`, https only), with
    a consent rule for both kinds and a "tool output is untrusted" rule.
  - Validity now has three outcomes (valid, invalid, unsupported version), three scopes and
    ten rules. V9 is new: no symbolic links.
  - Body limit dropped from 8,000 to 7,500 characters so that a worst-case rendered wrapper is
    9,432 characters, under the reported 10,000-character hook cap with room to spare.
  - The marketplace mapping now carries the steward's claim in the description, since an entry
    has no field for it.
  - Test scenarios are split into "checked in this project" and "defined here, exercised by a
    host (issue #2)".
- New critical open question 3: may a small self-test live in `spec/` to apply the validity and
  rendering rules to the fixtures? The plan depends on the answer.
- Mistake to avoid: I committed while the reviews were running, so two reviews carry a
  "repository moved" warning. The move was my own commit ec0b8cb (checked in the reflog). Do
  not commit while consultations are in flight.
- `skills-ref` is not installed in this environment. Claude Code 2.1.329 is.
