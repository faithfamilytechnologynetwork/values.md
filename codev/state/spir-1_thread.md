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
