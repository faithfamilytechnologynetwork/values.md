# spir-2 thread — reference implementation (issue #2)

## 2026-11-20 — specify: first draft

Read the approved spec for the standard and its files on `builder/spir-1` (pull request #4),
issues #1 to #3, and the architect's starting notes on #2. `spec/` and `values/` are not on
`main` yet, so this branch does not have them.

Checked from here:

- Ansari MCP server answered `initialize` (protocol `2024-11-05`, server "Ansari" 1.0.0) and
  `tools/list` (one tool, `answer_islamic_question`) at 03:11 UTC on 2026-11-21. Plain JSON
  replies, no session identifier.
- Tinker and Claude Code hook documentation, read on 2026-11-20. Notes that matter later:
  the generated-token limit is `max_completion_tokens`; reasoning comes back in
  `reasoning_content` and is to be sent back with earlier assistant turns; replies carry
  `usage`; the hook cap of 10,000 characters is per string, and text over it is replaced by
  a file path and a preview, not cut.

Not checked: anything on Tinker. There is no provider access in this worktree. Asked the
architect how a key is supplied and whether it is a second account.

Choices made in the draft, to be confirmed at the spec gate:

- A local web application: a Python server and a page with no build step.
- The host uses the standard's checker as a library for reading, validity and rendering,
  and writes only the run-time behaviour itself.
- Level 2. The Roman Catholic example keeps its depth in a skill and bundled texts, so its
  pane answers from the prompt and says it cannot open its catechism. Raised as an open
  question.
- Reinjection is counted at one token for every four characters. The provider's reported
  counts are used only for the context window.
- The long conversation is a script in which a turn may carry a reply written in advance.
- "Base model" and "prompt only" panes are controls and are labelled as such, because a
  conforming host always reinjects.
- Prompt on top of the `omit` checkpoint is tested against a temporary copy of the package,
  not through a switch in the host.
- The Claude Code adapter is a command given the package's location that also prints its
  hook configuration.

Architect's reply on provider access (2026-11-21): the owner is being asked. The only access
known belongs to the account that trained the checkpoints, so it would not settle the
second-account check. Carry on: spec on the reported facts, live verification as the plan's
first step.
