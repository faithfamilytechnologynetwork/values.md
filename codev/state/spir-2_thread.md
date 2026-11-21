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

## 2026-11-20 — specify: reviewed, at the spec-approval gate

Codex and Claude both asked for changes; the Gemini lane produced no review (its CLI exited
with code 3). All points taken except one detail (MCP session identifiers and reply formats
are left to the client library). The main changes:

- A probe in a script is answered by the model, shown and recorded, and not carried forward,
  so every pane continues from the same conversation.
- The context window is checked before a request with the host's own count (four characters
  to a token) plus the reply limit. Reported counts are shown and recorded only.
- Numbers: 8 tool calls a turn, 120 seconds for a tool call, 300 seconds for a model request,
  8,192 tokens for a reply, 65,536 for the host's window. All settings.
- The host checks `Host` and `Origin`, and does not follow a redirect from a consented
  address.
- The adapter keeps no state: it finds its last placement in the transcript. This rests on
  Claude Code writing hook text into the transcript, to be checked first.
- Consent on a command-line run is given in the command, by package and server.
- Records name packages by collection folder and hold no machine path or user name. Only
  scripted runs made for the findings are committed.

Four questions are open for the owner at the gate, each with a recommendation: demo length
under 64K, the live link as a local directory, Level 2 (the Roman Catholic pane then cannot
open its catechism), and replies written in advance in the long script. Two practical
matters for the architect: provider access, and getting `spec/` and `values/` onto this
branch before implementation.

## 2026-11-21 — spec revised at the gate: the adapter is not a conforming host

The architect relayed a finding from project 1's compatibility note (`spec/compatibility.md`,
"Where this departs from the specification"). A Claude Code hook's text goes into the
conversation inside a system reminder, not into the system prompt, so a hook adapter cannot
meet the standard's rules on placement, exactness and placing the wrapper once. Whether the
standard should allow that placement is with the owner.

Part 11 was rewritten to say what the adapter does and where it departs, in the note's own
six points, and that it does not make Claude Code a conforming host. Session starts now
follow the note's table: emit at start-up, clear and compaction; at a resume or a fork only
if the conversation does not already hold the wrapper. The cap is measured in UTF-16 code
units, the stricter reading, since Claude Code does not say what it counts. The live checks
now include the things the note marks as not tried.

Also read `spec/specification.md` on the same branch, now that all five phases of project 1
are built. Two things taken from it: the system prompt, tool definitions and a package's own
reminder are not counted toward its interval; and the reminder is a content block of its own
where the API has content blocks, otherwise one string. Which form the Tinker endpoint takes
for this model is for the first live check. The requirements are numbered H1 to H10 there.

The spec is still at the spec-approval gate.

## 2026-11-21 — spec not approved; rewritten for a public service

The owner did not approve the spec. He wants the chatbot runnable on the internet, with no
local operation required. Hosting and public deployment are now in scope, and the issue body
says so. The spec was rewritten around a service at a public address. It is back at the
spec-approval gate.

What changed:

- **Who pays.** The service holds the operator's key. Visitors bring nothing. Spending is
  limited in money, worked out from the provider's reported token counts and its published
  prices: by default $0.50 a day for one visitor and $5.00 a day for all visitors, checked
  before every model request. The daily totals survive a restart. The provider offers no
  spending cap of its own that could be found, so the operator's guide recommends an account
  paid for in advance.
- **Abuse.** Limits on message length, turns per visitor, model requests at once, and calls a
  day to any one tool server. An off switch for live chat. No package, script, key or request
  of a visitor's own making is accepted.
- **Privacy.** Conversations live in the service's memory for the visit and are written
  nowhere. Logs hold counts and no text. A visitor can save their own record to their own
  machine.
- **Consent.** Per visitor, per visit, per package and server, in the browser.
- **The link to the collection.** The service is deployed again whenever `main` changes and
  reads `values/` from the commit it was built from. Fetching from GitHub while running was
  rejected: the packages and the standard would come from different commits.
- **Recordings.** The committed records behind the findings can be opened on the service,
  marked as recordings. They need no model, so the page still shows something when a limit is
  reached or live chat is off.
- **No second catalogue.** The service lists what is needed to pick panes, plus what the
  standard requires a host to show before activation, and links to the collection's browser
  (issue #3) for the rest.
- **Where it runs.** One small instance that stays up. Railway is recommended, at about $5 to
  $20 a month. Four other platforms are compared. The owner decides, and the first public
  deployment waits for his say-so.
- **The adapter** (part 11) now allows for the expected change to the standard that lets an
  outside adapter place the wrapper at the start of the conversation if it says so. The other
  five departures stand.

Live checks, 2026-11-21 05:20 UTC, all against the real endpoint: Inkling 2 Small follows a
system prompt, calls a tool and answers from the result, takes a user message as two text
blocks and a system message mid-conversation, and reports cached tokens. The declared
checkpoint loads from `base` and `adapter` alone, returns no reasoning, and follows a system
prompt. A checkpoint path that does not exist gives HTTP 404, which is the load-failure
signal the host needs. Two consequences in the spec: the reminder is a content block of its
own, as the standard prefers, and a declared model is addressed as `base;adapter`. One
surprise: the endpoint refuses a request sent under a programming library's default client
name (HTTP 403), so the host sends a named client. Loading the checkpoint from a second
account is still not verified.

The owner's four earlier recommendations: demo under 64K, Level 2 and replies written in
advance are unchanged. The live link changed as above.

For the owner at the gate, each with a recommendation in the spec's Open Questions: where it
runs; the limit figures; whether the host should offer web search now that the Roman
Catholic example is to take its detail from it (recommended: no, in this project); declared
models on the public service; no moderation of the host's own; and confirming with the
Ansari project that a public demonstration may call its server.

The revised spec has not been through a second review round. Porch is holding at the gate
and has not asked for one.
