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

## 2026-11-20 — specify, after the owner's answers

The owner answered the first round of open questions in a comment on issue #1. The gate is
still pending. The spec was revised to match:

- The reading of decision 3 is confirmed, and the draft wrapper wording is the starting text.
- Principled pluralism is now an ordinary example package, `example-principled-pluralism`,
  `VALUES.md` alone. The separate "where it fits" part is gone, and so is the plan to credit it
  as the source of the wrapper's structure. The wrapper's rules stand on their own merits.
- A checker for the fixtures and renderings lives in its own directory under `spec/`.
- Core-only reinjection stands. The cost table moved from Open Questions into Solution
  Approaches as the recorded reasoning.
- Fine-tuned models: the fixed rule "replaces reinjection only" is replaced by a `prompt` field
  on each model entry (`required`, `optional`, `omit`; default `required`). The package
  declares what a model supports, and the user or operator chooses within that. What the user
  is shown about what is installed holds in every mode, and when a model runs without the
  prompt the host's own display carries it. This design is the one critical open question
  left.
- The Islam example declares the stage 2 checkpoint. Its base model ID is still to be
  confirmed, so the entry in the spec leaves it unfilled.
- The spec, this thread and the pull request are written for public readers.

A pull request with the spec is open so that it can be shared before the gate is decided.

## 2026-11-20 — the collection moves into this repository

The owner decided that the collection of value systems is a directory in this repository,
`values/` at the root, and not a separate repository. The spec was updated:

- The repository has three parts: `spec/`, `reference/` and `values/`.
- The four example packages live once, in `values/`. `spec/` keeps no copy and refers to them
  by path. They must be loadable from there by the standard's rules alone, because the
  reference implementation reads `values/` directly.
- Expected renderings now belong to the purpose-made fixtures in `spec/`, not to the examples,
  so that nothing in `spec/` duplicates a package's text. The one exception is the smallest
  valid file shown at the top of the specification, which the checker compares with
  `values/plain-speaking/VALUES.md`.
- The marketplace mapping's `source` is now the path from the marketplace file's root, which
  for a marketplace at the repository root is `./values/<name>`.
- The stage 2 checkpoint's base model ID is still unconfirmed and still unfilled.

## 2026-11-20 — the standard covers public models only

The owner's final word on models: the standard refers only to public models. A package may
declare only a model that anyone with access to the provider can load. The `access` field that
earlier drafts added to each model entry is dropped, along with everything that depended on
it. A model entry has three required fields: `provider`, `base` and `adapter`. When a declared
model fails to load, the host tells the user and goes back to its own model with the prompt
and reinjection. The project's stage 2 checkpoint was being published at that point. Earlier entries in this log that mention `access` describe those drafts.

## 2026-11-20 — stage 2 checkpoint confirmed

The architect relayed confirmation that the stage 2 checkpoint is published on Tinker with no
expiry. Base `thinkingmachines/Inkling-2-Small`, LoRA rank 32, the standard 65,536-token
window, and no larger-window copy. The model entry for the Islam example in the spec is now
complete: `provider`, `base`, `adapter` and `context-window`. Its `prompt` value is still an
open question, because the checkpoint was trained with no system prompt and has not been tried
with one. Loading the checkpoint from a second account has not been tested. The spec records
that as an assumption and a risk, and asks the review to record a test or say plainly that it
was not done.

## 2026-11-20 — the prompt field is decided

The owner confirmed the `prompt` field design for fine-tuned models, and that with several
value systems active all of them are injected. Both are recorded in the spec's Constraints.
The spec now has no critical open question. The ones left have a recommended answer each and
do not change what is delivered. The spec-approval gate is still pending.
