# Rebuttal: specify, iteration 1

Reviews: Gemini (no review: the lane was skipped, its CLI exited with code 3), Codex
(REQUEST_CHANGES), Claude (REQUEST_CHANGES). Every point below was taken unless it says
otherwise. All changes are in `codev/specs/2-reference-implementation-inkli.md`.

## Codex

1. **Mode B and several packages.** Taken. Part 6 now says mode B skips reinjection only for
   the package that declares the model, and any other package in the pane is reinjected as
   usual. A success criterion and test scenario 9 cover it.
2. **Context-window enforcement.** Taken. Part 6 now says how the size is known before a
   request: the host's own count, at one token for every four characters, over everything it
   is about to send (system prompt, messages, reasoning, tool calls and results, replies
   written in advance), plus the reply limit. The default window for the host's model is
   65,536 and the reply limit is 8,192, both settings. A refusal from the provider as too long
   is shown and the pane stops. Reported counts are shown and recorded, and are not what the
   host decides by. The "Rejected" note under token counting was corrected to match.
3. **Local web security.** Taken. Part 13 now requires the host to answer only requests
   addressed to the local machine, and to accept a request that sends a message or changes
   anything only from its own page. Part 7 says the host does not follow a redirect from a
   consented address. Criteria and scenarios added.
4. **Adapter state.** Taken. Part 11 now states the model: the adapter keeps no state and
   finds its last placement in the transcript, as the most recent wrapper or reminder it
   emitted for that package. A session start of any kind places the wrapper again and the
   count runs from there. That rests on Claude Code writing hook-supplied text into the
   transcript, which is checked first against a real session; part 11 says what the adapter
   keeps instead if it does not hold. Scenarios cover all five kinds of session start.
5. **MCP and tool-loop bounds.** Taken in part. Added: a limit of eight tool calls a turn, a
   120-second limit on a tool call and a 300-second limit on a model request, all settings;
   several calls in one reply run in order and each counts; both `http` and `sse` servers are
   supported; the host offers a server no capabilities, so server-issued requests are
   declined. Not taken: spelling out session identifiers and JSON versus SSE replies. The
   spec now says the host uses an existing MCP client library and writes no transport of its
   own, and those belong to that library.
6. **Privacy of records.** Taken. Part 10 now says a record names a package by its folder in
   the collection, holds no machine path or user name, and that only records of scripted
   runs made for the findings are committed, each read through first. A test checks the
   contents.
7. **Open questions already adopted.** Taken. The Important questions now open with a
   statement that Desired State is written on the recommended answers so that the spec states
   one design, and is revised before the plan if the owner decides otherwise.
8. **Numbers for the limits.** Taken, with point 5.

## Claude

1. **Probe answers diverge the panes.** Taken. Part 9 now says a probe is answered by the
   model, shown and recorded, and left out of what the pane carries forward, so every pane
   continues from the same conversation. It also says what happens to a reminder due at a
   probe. This is the reviewer's second option in a simpler form: no written reply is needed
   for a probe. The reasoning, including that an early in-tradition answer would otherwise
   prop up a later one, is under Solution Approaches.
2. **Records against the no-copies rule.** Taken. Part 10 names where the records are kept
   and says why they are not copies in the rule's sense: the host reads nothing from them.
   The first success criterion and the no-copies scenario are scoped to match.
3. **The adapter's last placement.** Taken. See Codex 4. Added as open question 8 and as a
   live criterion.
4. **Consent from the command line.** Taken. Part 7: consent is given in the command by
   naming the package and server, the address is printed first, and a server not named is not
   connected.
5. **Context-window tracking for replies written in advance.** Taken. See Codex 2.

Smaller points:

- Generation settings: taken. The same in every pane, and held in the record.
- A number for the tool-call limit: taken.
- `context_tokens` on resume or fork: taken. The Current State row now agrees with the
  standard's spec.
- The fine-tuned pane differs by tools as well as weights: taken, in part 12 item 6.
- Whether a pane's configuration is fixed: taken. It is fixed once the first message is sent,
  and changing any pane starts a new conversation in every pane.
- The pull request #4 dependency: taken. It is named under Critical, as a practical matter
  for the architect.
- Rate limits: taken, as a risk row. The host does not retry on its own.
- `Origin` and `Host`: taken. See Codex 3.
