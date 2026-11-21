# Specification: Reference implementation — a side-by-side chatbot on Inkling 2 Small

<!--
SPEC vs PLAN BOUNDARY:
This spec defines WHAT and WHY. The plan defines HOW and WHEN.
Keep implementation phases, file paths, code, and "first we will… then we will…"
out of the spec — those belong in codev/plans/<id>-*.md.
-->

Issue: #2. Protocol: SPIR. The repository has three parts: `spec/` (the standard, issue #1),
`reference/` (this project) and `values/` (the collection of value systems, issue #3). This
project builds what goes under `reference/`. It changes nothing under `spec/` or `values/`.

"The standard" below means the values.md standard v0.1 as its approved spec states it
(`codev/specs/1-values-md-standard-v0-1-the-va.md`, on pull request #4 until that merges).
"Part N" means part N of that spec's Desired State section. "V1" to "V10" are its validity
rules, and "host test 31" to "host test 40" are the ten scenarios it lists under "Defined here,
exercised by a host (issue #2)".

Terms used here, beyond the standard's own (value system, package, host, steward, prompt fade,
collection, modes A, B and C):

- **Pane**: one column of the window. It holds one conversation with one model under one
  configuration.
- **Configuration**: what a pane has installed and how it runs: which value systems are active
  (none, one or several), which model answers, whether the prompt is injected, and whether the
  core is reinjected.
- **Control**: a pane configured to leave out something a conforming host does, so that the
  effect of that thing can be seen. A control is labelled as one wherever it appears.
- **Script**: a conversation written down in advance, so that the same long conversation can
  be played into every pane.
- **Record**: a file that holds everything a run sent and received, pane by pane.

## Problem Statement

The standard says what a host does with a values package: how it reads `VALUES.md`, what text
it puts in front of the model, when it repeats the core, what it does with a declared
fine-tuned model, what it asks consent for and what it shows the user. Nothing runs those
rules yet. The standard's own project checks packages and renderings and stops there, because
it ships no host. Ten of its test scenarios are handed to this project by name.

Three groups of people are affected:

- **Someone deciding whether the standard is worth adopting** cannot see what it does. A
  rendered prompt in a text file does not show that the same question gets a different,
  tradition-grounded answer once a value system is installed.
- **A host developer** has no working host to read or to compare their own against.
- **The standard's authors** do not know whether the wrapper wording holds on a real model,
  whether reinjection does anything about prompt fade, or whether a fine-tuned model can stand
  in for the prompt. These are open risks in the standard's spec, and each is assigned to this
  project to test.

Prompt fade is the hardest of these to show. It appears only in a long conversation, and it
can only be seen by comparison: the same conversation, with and without the thing that is
meant to prevent it.

## Current State

- `reference/` does not exist. There is no host for the standard anywhere.
- The standard is specified and partly built on pull request #4: the schema, the three
  normative prompt texts, the fixtures, a checker, and the four example packages in `values/`.
  The specification text, the rationale and the compatibility note are still to come.
- The checker decides validity and renders the wrapper and reminder. By design it is not a
  loader and talks to no model.
- A package installed in Claude Code as a plugin gets its skills and MCP servers and not its
  prompt. Claude Code does not read `VALUES.md`. The standard describes the adapter that
  would supply the prompt and leaves building it to this project.

What was checked for this spec, and what is only reported:

| Subject | Finding | Status |
|---|---|---|
| Tinker's OpenAI-compatible endpoint | Base address `https://tinker.thinkingmachines.dev/services/tinker-prod/oai/api/v1`, with a bearer key. The chat completions call takes `system`, `user`, `assistant` and `tool` messages, `tools` and `tool_choice`, and streaming. Replies carry `usage` token counts. A reasoning model returns its reasoning in `reasoning_content`, apart from `content`, and the documentation says to send each earlier assistant turn back with it. The limit on generated tokens is `max_completion_tokens`. The documentation is silent on a system message in the middle of a conversation and on how streamed tool calls are assembled. | Documentation read on 2026-11-20. Not called from here: this project had no provider access when the spec was written. |
| Inkling 2 Small on Tinker | The documentation lists `thinkingmachines/Inkling-2-Small` (64K) and `thinkingmachines/Inkling-2-Small:peft:262144` (256K) as separate model IDs. One page says serverless inference is in beta for other models only. The owner reports that the base model and a checkpoint both answered on this endpoint with a system prompt. | Model list read through a summary. The owner's report is from 2026-11-20. To be confirmed by a call. |
| Addressing a checkpoint | The documentation gives two forms for `model`: the checkpoint path alone, which runs on the base model it was trained on, and `<base model ID>;<checkpoint path>`, where the base model must be the one the checkpoint was trained on, at the context length wanted. | Documentation read on 2026-11-20. The owner reports the first form working. The second is untested. |
| The declared checkpoint | `example-islam` declares one model: provider `tinker`, base `thinkingmachines/Inkling-2-Small`, a 65,536-token window, `prompt: omit`. It was trained with no system prompt. Loading it from an account other than the one that trained it is untested. A copy of an earlier training stage exists at 256K. The declared one has no 256K copy. | From the package and the issue. |
| Ansari | The MCP server at `https://mcp.ansari.chat/mcp` answered `initialize` (protocol `2024-11-05`, server "Ansari" 1.0.0) and listed one tool, `answer_islamic_question`, taking a `question` string, at 03:11 UTC on 2026-11-21. It needs no key, answers in plain JSON and issues no session identifier. | Checked by calling the server. |
| The example packages | `example-islam` has a remote tool and a declared model. `example-roman-catholic` has no tool and no model: its depth is a skill and bundled texts, the largest about 88,000 characters. `example-principled-pluralism` and `plain-speaking` are `VALUES.md` alone. | Read on pull request #4. |
| Claude Code hooks | `SessionStart` and `UserPromptSubmit` hooks can add context, as plain output or as `hookSpecificOutput.additionalContext`. `SessionStart` fires on start-up, resume, clear, compaction and fork. Each such string is capped at 10,000 characters, measured separately for each hook. Text over the cap is replaced by a file path and a preview, so the model would not have it. A hook receives the path of the transcript and no running token count. Hooks can be declared in settings, in a plugin manifest, or inline in a marketplace entry for a plugin folder that has no manifest. | Documentation read on 2026-11-20. Part through a summary. To be confirmed by running it. |

## Desired State

A person clones the repository, supplies a Tinker key, runs one command and opens a page on
their own machine. The page shows the value systems in `values/` and a window of panes. They
type a question once. Each pane answers it from a different value system, or from the same
value system run a different way, and each pane shows what is installed, who vouches for it and
what the model was actually sent.

The rest of this section states what is built. The reasoning and the alternatives are under
Solution Approaches.

### 1. What is delivered

Under `reference/`, and nowhere else:

1. **The chatbot**: a host for the standard that runs on the user's own machine and is used
   through a browser page.
2. **Scripts**: a format for a conversation written in advance, at least one long script that
   ships with the project, and a way to play a script without the browser.
3. **The Claude Code prompt adapter**: what makes Claude Code inject a package's prompt and
   reminder.
4. **A README** that says what is here, how to run it, what it needs and what level of the
   standard it claims.

And in the project's review document: the findings in part 12.

### 2. The host

- It claims **Level 2** of the standard: it reads `VALUES.md`, injects the wrapper, addresses
  prompt fade, discloses what is installed, and connects the remote MCP servers a package
  declares. It does not expose `skills/` or `references/`, and it starts no local MCP server.
- It talks to one provider, Tinker, through the OpenAI-compatible endpoint. Its own model is
  `thinkingmachines/Inkling-2-Small`. The model name is a setting, so that the same host can
  be run on another base model without a change to its code.
- It adds no instructions of its own to the conversation. A pane with nothing installed has no
  system prompt, and a pane with a value system has exactly the text the standard puts there.
  What differs between two panes is then only what the standard does.
- It implements nothing the standard does not define. Where the host needs a rule the standard
  lacks, the gap is written down as a finding (part 12) and the simplest behaviour is chosen
  and stated.

### 3. The link to the collection

- The host reads value systems from one directory, the collection. By default this is
  `values/` at the root of the repository the host is run from. The directory is a setting.
- It reads the directory each time the list of value systems is asked for and each time a
  pane is set up. It keeps no copy of any package, in the repository or on disk. A folder
  added to the collection appears in the list at the next refresh of the page, with no
  restart.
- A conversation that is already running keeps the text it started with. A package edited on
  disk takes effect in the next conversation.
- Every folder in the collection is checked against V1 to V10 before it is offered. A valid
  package can be activated. An invalid one is listed as refused, with the identifiers of the
  rules it breaks, and cannot be activated. One that targets a later version of the standard
  is listed as one this host cannot judge. Nothing is repaired or truncated.
- The schema and the three normative prompt texts are read from `spec/` where they live. The
  project keeps no copy of them.

### 4. The window

- The window holds two to four panes, side by side. There is one message box. A message is
  sent to every pane at once, and each pane keeps its own conversation.
- Panes work at the same time. A pane that is slow or fails does not hold up the others. A
  failure is shown in the pane it happened in, in plain words, and that pane stops.
- Two arrangements are offered ready-made:

  | Arrangement | Panes |
  |---|---|
  | **Value systems** (the default) | `example-islam`, `example-roman-catholic` and `example-principled-pluralism`, each on the host's own model with the prompt and reinjection (mode A). |
  | **Prompt fade**, for one value system the user picks | (1) Base model: nothing installed. (2) Prompt only: the wrapper is injected and the core is never reinjected. (3) Prompt with reinjection: mode A. (4) Fine-tuned model: a model the package declares, in the mode its `prompt` value allows. |

- The user can also set each pane by hand: any valid package in the collection, several
  packages together, or none, and any way of running that part 6 allows.
- Panes 1 and 2 of the prompt fade arrangement are controls. A conforming host always
  reinjects, and a package cannot turn reinjection off. Pane 2 leaves it out on purpose, at
  the user's choice, to show what reinjection changes. Each is labelled as a control, and the
  README says that a control is not conforming behaviour.
- The fourth pane is offered only for a package that declares a model matching the host's
  (part 6). For any other package the arrangement has three panes and says why.

### 5. What a pane puts in front of the model

Exactly what parts 3, 4, 5 and 10 of the standard say:

- **The wrapper** goes in the system prompt, once, rendered from the normative text with the
  package's name, steward name and body.
- **Reinjection.** The host counts the tokens added to the conversation since the value
  system's text was last placed: the user's messages, the model's replies and reasoning, tool
  calls and tool results. The count starts at zero when the wrapper is placed and returns to
  zero after each reminder. When it has reached the package's interval, the reminder is placed
  at the start of the next user message, then a blank line, then the user's own text. A value
  system gets at most one reminder at a boundary, however large its count.
- **Counting.** The host has no tokenizer for the model, so it uses the standard's estimate
  of one token for every four characters. This makes the placing of reminders the same on every
  run of the same text, and testable without a model.
- **Several value systems in one pane.** The preamble comes first, then one wrapper per
  package in the order the user activated them. Each package has its own count and its own
  interval, and each one that is due gets its reminder, in activation order. A second package
  with a name already active in that pane is refused.
- Every reminder stays in the conversation. The host drops none.
- The pane shows the user's message as they typed it, and marks each turn where a reminder was
  attached. It shows each package's running count against its interval. The user can open a
  view of exactly what the model was sent for that pane: the system prompt and every message,
  reminders included.

### 6. Declared models

The host follows part 6 of the standard.

- **Matching.** A package's `models` entry matches when its `provider` is `tinker` and its
  `base` is exactly the name of the host's own model. Nothing else matches, and entries that
  do not match are ignored.
- **Addressing.** The host addresses a declared model from the entry's `base` and `adapter`
  alone. It needs nothing that is not in the package.
- **Modes.** The host offers mode A always, mode B for an entry whose `prompt` is `required`
  or `optional`, and mode C for an entry whose `prompt` is `optional` or `omit`. It does not
  offer mode C for `required` or for an entry with no `prompt` value, and does not offer mode
  B for `omit`. In mode B it does not reinject. Mode C is offered only when that package is
  the only one active in the pane.
- **Who chooses.** The user. The host never moves a pane to a declared model, and never drops
  the prompt, without the user having chosen that for that pane. Choosing the prompt fade
  arrangement is such a choice, and the arrangement says what its fourth pane will run before
  it starts.
- **Mode C.** Before a pane starts in mode C, the host says what that gives up: none of the
  wrapper's rules and none of the body's instructions are in context, and how the model
  behaves rests on its weights. Tools the package declares stay connected.
- **A model that fails to load.** The pane says which model failed, and goes on in mode A:
  the host's own model, with the prompt and reinjection. It does not go on in mode C without
  the model and does not try another entry.
- **The context window.** A pane's window is the entry's `context-window` for a declared
  model and a setting for the host's own model. The host tracks the size of each conversation
  from the token counts the provider reports. When the next message would not fit, the pane
  stops and says so. It does not drop or shorten earlier turns to make room.

### 7. Tools

- When a package with an `.mcp.json` is activated, the host connects each remote server it
  declares and offers that server's tools to the model. What a tool returns goes back to the
  model as a tool result and nowhere else. It is never added to the system prompt.
- **Consent.** Before the host first connects to a server, it asks the user, naming the
  package and the server and showing the address, and saying that the user's questions will be
  sent there. Consent is given for one package and one server. It is held in memory and is
  asked for again after the host restarts. If the user declines, the package is still
  activated, without that server's tools, and the pane shows that the tool is not connected.
- **Local servers.** The host starts none, as the standard allows. A package that declares
  one is still activated, and the pane shows that the server was not started.
- A server that cannot be reached is shown in the pane as not connected. The conversation goes
  on without its tools.
- The pane shows each tool call and what came back.
- There is a fixed limit on the number of tool calls in one turn. A turn that reaches it stops
  with a message saying so.
- Tools stay connected in every mode, mode C included. A pane with nothing installed has no
  tools.

### 8. What the user is shown

Before a value system is activated, in the place where it is chosen:

- its name, description, steward, kind of claim and steward address, and its version;
- where it came from: the folder it was read from;
- the tools it declares, by server name and address, and the models it declares, each with
  its provider, base, adapter, `prompt` value and description.

For as long as it is active, at the head of its pane:

- its name, steward, kind of claim and source;
- which model is answering, and when that is a declared model, that it is a fine-tuned model
  and which one;
- whether the prompt is injected and whether the core is reinjected;
- the word "control" on a pane that is one.

This holds in every mode. In mode C it is the only thing that tells the user what is
installed, so the pane also says that the prompt is not injected.

The page shows everything that comes from a package, a model or a tool as text. None of it is
run or treated as markup by the browser.

### 9. Scripts and the long conversation

Prompt fade shows only in a long conversation, and nobody can type one by hand several times
over. So the conversation can be written down and played.

- A script is a list of turns in order. A turn is a user message. A turn may carry a reply
  written in advance, which is then used in every pane in place of calling the model. A turn
  may be marked as a probe: a question whose answers are the ones worth comparing.
- A reply written in advance lets a long stretch of conversation be the same in every pane and
  costs no model call. Such a reply is always shown as written in advance and not as that
  pane's own answer. It counts toward the reinjection interval like any other text, so
  reminders fall where they would have fallen in a live conversation.
- The window can play a script into its panes. A script can also be played from the command
  line with no browser, against the same arrangements.
- One long script ships with the project. It is long enough to pass the reinjection interval
  at least five times, fits the 65,536-token window with room for the replies, and has probes
  before the first interval and near the end. Any text in it that the project did not write is
  in the public domain and says where it came from.

### 10. Records

- Any run, typed or scripted, can be saved as a record: for each pane, its configuration, the
  model addressed, and every message sent and received in order, with reminders, tool calls,
  tool results, the token counts the provider reported and the times.
- A record holds no key and no request headers.
- Records are what the findings in part 12 are drawn from. The project keeps the records
  behind its findings where a reader can check them.

### 11. The Claude Code prompt adapter

The adapter gives Claude Code the one thing a plugin does not: the prompt.

- For a package the user has chosen to install, it supplies the rendered wrapper when a
  session starts, and again whenever Claude Code rebuilds the context: after a resume, a
  clear, a compaction or a fork.
- It supplies the reminder with the user's next prompt once the conversation has grown by the
  package's interval since that package's text was last placed. Claude Code gives a hook no
  token count, so the adapter works the count out from the session's transcript, at one token
  for every four characters.
- It uses the same reading, validity and rendering rules as the chatbot. A package that is
  not valid is refused with an error naming the rule, and nothing is injected.
- It refuses, with an error, to emit a text longer than Claude Code's 10,000-character cap. It
  does not truncate.
- With several packages it emits one output for each package and the preamble as an output of
  its own.
- It can print the hook configuration for a given list of packages, ready to put into Claude
  Code's settings, a plugin manifest or a marketplace entry. Nothing is installed without
  the user doing so. Putting that configuration in place is the explicit installation the
  standard requires.
- The README says what Claude Code still does not do with the adapter in place, including
  what its install screen shows about the steward.

### 12. What this project finds out

The standard hands these to this project. Each is tried against the real model or the real
tool, and the result goes in the review with the date and the record behind it. Each is
either answered or reported as not verified, with the reason. None is ticked on trust.

1. Whether Inkling 2 Small on Tinker takes a system prompt and calls tools through this
   endpoint, and its exact model name.
2. How the declared checkpoint is addressed, and whether `base` and `adapter` are enough.
3. Whether the declared checkpoint loads from an account other than the one that trained it.
4. Whether the wrapper wording holds on the real model. There is at least one probe for each
   of the wrapper's seven rules.
5. How the declared checkpoint behaves with the value-system prompt on top of it. The package
   declares `prompt: omit`, so a conforming host will not run that combination. The test is
   run against a temporary copy of the package, outside the collection, with the value changed
   to `optional`. The result is a recommendation to keep `omit` or change to `optional`.
6. What the prompt fade arrangement shows on the long script: how the four panes answer the
   same probes early and late.
7. Anything the host needed that the standard does not define, and anything in the standard
   that could not be implemented as written.

Probe answers are judged by reading them, and the review says so. This is a demonstration
with its evidence attached. It is not a benchmark, and it makes no claim beyond the
conversations it ran.

Findings about the standard or the examples are reported to the architect and listed in the
review. This project does not change `spec/` or `values/` to act on them.

### 13. Running it

- One documented command starts the host. The key is read from the environment and stays in
  the host process. It is never sent to the browser, written to a record or printed.
- Without a key the host does not start, and says what is missing.
- The host listens on the local machine only. It has no accounts and no sign-in, because it
  is not a hosted service.
- The project's tests run with no network and no key, against a stand-in for the model and a
  stand-in for a tool server. Checks that need the real provider or the real tool are
  separate, and are run and reported with their dates.

## Success Criteria

Criteria marked (live) need the real provider or tool. If one cannot be run, it is reported
as not verified in the review and to the architect.

Scope and layout

- [ ] Everything this project adds is under `reference/`, apart from Codev artifacts. Nothing
      under `spec/` or `values/` is changed, and `reference/` holds no copy of a package, the
      schema or a normative prompt text.
- [ ] One documented command starts the host, and the README states the level claimed, what
      is needed to run it, and which panes are controls.

The collection

- [ ] The list of value systems is read from the collection directory. A valid package folder
      added to that directory while the host is running appears in the list at the next
      refresh, with no restart and no other change.
- [ ] An invalid package in the collection is listed as refused with its rule identifiers and
      cannot be activated. A package targeting a later `spec-version` is listed as one the
      host cannot judge.
- [ ] For every valid fixture in `spec/fixtures/`, the system prompt the host would send
      equals the fixture's expected wrapper, and the reminder it would attach equals the
      expected reminder. For every invalid fixture, the host refuses the package.

The prompt and reinjection

- [ ] A pane with one value system sends a system prompt that is exactly the rendered
      wrapper. A pane with nothing installed sends no system prompt.
- [ ] Host test 31: with the default interval, the first reminder is attached to the first
      user message after 5,000 counted tokens, as the reminder text, a blank line and the
      user's text. One very large tool result produces one reminder, not several.
- [ ] A package's own `every-tokens` and `section` values are honoured.
- [ ] Host test 36: with two value systems in a pane, the preamble comes first, each package
      has its wrapper in activation order and its own count, and each core is reinjected
      when due. A second package with the same name is refused.
- [ ] The pane marks the turns that carried a reminder, and the view of what the model was
      sent shows the full text of each one.

Declared models

- [ ] Host test 33: with the host's model set to a name that matches no entry, the package's
      `models` are ignored and the pane runs in mode A.
- [ ] Host test 32: with an entry whose `prompt` is `required` or `optional`, the user can
      choose mode B. The wrapper is injected, no reminder is attached, and the pane shows
      that a fine-tuned model is in use and names it.
- [ ] Host test 38: with `prompt: omit`, or `optional` and the user choosing to drop the
      prompt, nothing from the package is sent to the model. The pane still shows the name,
      steward, kind of claim and source, and shows that the prompt is not injected. The host
      said what mode C gives up before the pane started.
- [ ] Host test 39: with `prompt: required`, or with the field absent, mode C is not offered.
- [ ] Host test 40: with two value systems active in a pane, mode C is not offered for
      either.
- [ ] Host test 34: when a declared model fails to load, the pane names the model that
      failed and continues in mode A.
- [ ] No pane runs a declared model, or runs without the prompt, unless the user chose that
      for that pane.
- [ ] A pane whose next message would not fit its context window stops and says so.

Tools

- [ ] Host test 37: the host does not connect to a declared server before the user has
      consented for that package and that server, and the request for consent shows the
      address. Declining leaves the package active without that tool, and the pane says so.
- [ ] A package that declares a local server is activated with that server not started, and
      the pane says so.
- [ ] Host test 35: a package with `skills/` and `references/` is activated with both
      ignored, its prompt complete and any remote tool working.
- [ ] A tool result reaches the model only as a tool result. Tool calls and results are
      visible in the pane.
- [ ] (live) In a pane with `example-islam` on the host's model, a question asking for a
      ruling or a verse leads to a call to `answer_islamic_question`, and the answer is built
      on what came back.

Disclosure

- [ ] Before activation the user is shown the name, description, steward, kind of claim,
      version, source, declared tools and declared models. While a value system is active its
      pane shows the name, steward, kind of claim, source, the model in use, whether the
      prompt is injected and whether the core is reinjected.
- [ ] Text from a package, a model or a tool that contains markup is displayed as text.

The window, scripts and records

- [ ] One typed message is sent to every pane. A failure in one pane is shown there and the
      other panes complete.
- [ ] The value systems arrangement opens with the three example packages named by the owner.
      The prompt fade arrangement opens with the four panes of part 4 for a package that
      declares a matching model, and with three, and the reason, for one that does not.
- [ ] Playing a script sends the same user turns to every pane. A reply written in advance is
      used in every pane, is shown as written in advance, and counts toward the interval.
- [ ] The long script that ships with the project passes the default interval at least five
      times and fits a 65,536-token window with its replies.
- [ ] A script can be played from the command line, and a run can be saved as a record that
      holds each pane's configuration and every message sent and received. No record or log
      contains the key.
- [ ] (live) The prompt fade arrangement completes the long script for `example-islam` in
      all four panes, and the record is kept.

The Claude Code adapter

- [ ] For each valid fixture the adapter's session-start output carries exactly the expected
      wrapper, and its reminder output carries exactly the expected reminder once a transcript
      has grown by the interval, and nothing before that.
- [ ] It refuses an invalid package with the rule named, and refuses a rendered text over
      10,000 characters, without truncating either.
- [ ] It prints a hook configuration for one package and for several, with one output per
      package and the preamble on its own.
- [ ] (live) In a Claude Code session with `example-islam` installed as a plugin and the
      adapter's hooks in place, the model, asked what value system is installed, names it and
      its steward.

Findings

- [ ] The review answers each of the seven items of part 12, or reports it as not verified
      with the reason, and gives the date and the record for each one that was run.
- [ ] The review recommends `omit` or `optional` for the `example-islam` model entry, with
      the evidence, or says the test could not be run.
- [ ] Every finding about the standard or the examples has been sent to the architect.

Tests

- [ ] The project's tests pass with the network blocked and no key set.

## Constraints

Decided by the owner on 2026-11-20, copied from the issue. These are fixed.

- The model is Inkling 2 Small.
- The window is side by side, one pane per value system.
- The value systems shown are Islam (with Ansari as its tool), Roman Catholic and principled
  pluralism, each an example package from #1.
- Prompt fade is handled by (a) a declared fine-tuned model or (b) reinjecting the core of the
  prompt about every 5,000 tokens. The owner has a Tinker checkpoint for the Islam package;
  details are in the first comment.
- The chatbot keeps a live link to the collection of value systems in this repository (#3): it
  loads them from that directory and does not keep copies of its own.

From the issue's statement of what the chatbot should do. Also fixed.

- Load a values package exactly as the standard in `spec/` defines it, with no private
  extensions. If the implementation needs something the standard lacks, that is a finding for
  the standard.
- Inject the standard's system prompt, call the package's declared tools, and apply its
  persistence policy.
- Use a declared fine-tuned model when the package has one for the running base model.
- Make prompt fade visible: the panes should be able to show base model, prompt only, prompt
  with reinjection, and fine-tuned model on the same long conversation.

From the architect's starting notes on the issue (2026-11-21). Also fixed.

- The standard is read from pull request #4's branch until it merges, and from `main` after.
  Its files are not copied into `reference/`.
- This project builds the loader and everything a host does at run time, and the Claude Code
  prompt adapter.
- It tests a value-system prompt on top of the fine-tuned checkpoint, and the wrapper wording
  on a real model. A weak wrapper is a finding for the standard, not something to patch
  locally.
- Ansari is reached through its hosted MCP server, as `example-islam` declares it.

Out of scope, from the issue:

- Changes to the standard itself.
- Hosting or public deployment.

Further constraints:

- The repository is going public. Nothing in `reference/`, the Codev artifacts or the pull
  request says where a credential is kept or names an account.
- Out of scope: the collection's browser, its submission check and its marketplace file
  (issue #3), Level 3 of the standard, local MCP servers, accounts and sign-in, storing
  conversations beyond a saved record, training or publishing a model, and translations of
  the normative texts.

## Assumptions

- Pull request #4 merges, or its branch is otherwise made available to this project's branch,
  before the implementation needs `spec/` and `values/` in the working tree. If it has not
  when implementation starts, the architect decides how this branch gets them.
- The standard's remaining parts (the specification text and the compatibility note) will
  agree with its approved spec. Where the specification text, once written, differs from what
  is assumed here, the difference goes to the architect.
- A Tinker key is available for the live checks. Without one the project can still be built
  and tested against stand-ins, and every (live) criterion is reported as not verified.
- Inkling 2 Small calls tools through the OpenAI-compatible endpoint well enough for the
  Islam pane to reach Ansari. This is the first thing checked. If it does not, the architect
  is told at once, because the owner's decision that Ansari is the Islam example's tool rests
  on it.
- The declared checkpoint can be loaded with the key the project is given.
- The Ansari server stays available without a key.
- The estimate of one token for every four characters is close enough for English text that
  reminders fall near every 5,000 tokens. The interval is approximate by the owner's own
  wording.
- Claude Code's hook behaviour is as its documentation says. The adapter is checked against a
  real session before its criterion is ticked.
- One person uses the host at a time, on their own machine. That person is both the user and
  the operator in the standard's sense.

## Solution Approaches

### The form of the chatbot

The owner fixed the window as side by side. What remains open is what kind of program shows
it.

### Approach 1: A local web application (recommended)

A small server on the user's machine holds the key, the conversations and the tool
connections, and serves one page with the panes. The server is written in Python and the
page needs no build step.

- For: a browser gives side-by-side columns, long scrolling text and a consent dialog with no
  special effort. Python is what the standard's checker is written in, so the host can use the
  checker's reading and validity rules directly, and one toolchain serves the repository. The
  key stays on the server side.
- Against: two parts to keep in step, a server and a page.
- Risk: low.

### Approach 2: A JavaScript application, server and page

- For: one language on both sides.
- Against: the reading and validity rules would have to be written a second time in another
  language and kept in step with the checker, or the checker called as a separate program.
  It adds a second toolchain to a repository that has one.
- Risk: medium. Two implementations of the same rules can drift.

### Approach 3: A terminal application

Panes drawn side by side in a terminal.

- For: no browser and no server.
- Against: four columns of long prose are hard to read at terminal widths, and a view of
  exactly what the model was sent is awkward. It is a poor thing to show someone who is
  deciding whether to adopt the standard.
- Risk: low to build, high that it does not serve the purpose.

### Approach 4: A notebook or a ready-made chat interface kit

- For: the least code for a first screen.
- Against: these kits own the layout and the conversation state. Several conversations fed
  from one message box, with reminders, consent and a per-pane disclosure header, means
  working against the kit.
- Risk: medium.

Approach 1 is recommended.

### Decisions inside that approach

Each of these was open. The first alternative listed is the one adopted in Desired State.

**Where the reading and validity rules come from.**

- Adopted: the host uses the standard's checker as a library for reading a file, deciding
  validity and rendering the texts, and writes itself only what happens at run time. A host
  at install and a collection's check then give the same verdict by construction, which is
  the reason the standard has one definition of validity.
- Rejected: a second, independent loader inside `reference/`. It would show that the rules can
  be implemented from the text alone, and it would double the code and let two readings
  drift. The standard's own project already tests "implementable from the text" another way.

**How tokens are counted for reinjection.**

- Adopted: one token for every four characters, the standard's rule for a host with no
  tokenizer. It is the same on every run, the same in the chatbot and the adapter, and can be
  tested with no model.
- Rejected: the provider's reported token counts. They are exact, but they arrive only after
  a call, they include overhead the provider adds, and a reply written in advance has none.
  The reported counts are still used for the one thing that needs them, the context window.
- Rejected: loading the model's tokenizer. It adds a dependency and a download for an
  interval the owner describes as approximate.

**Where the long conversation comes from.**

- Adopted: a script, in which a turn may carry a reply written in advance. The same long
  stretch is then identical in every pane, a run costs a handful of model calls and takes
  minutes, and the result can be repeated.
- Rejected: typing it live. Nobody can type tens of thousands of tokens four times over.
- Rejected: a script of user turns only, with every reply generated. Each pane's history
  would then differ, so two panes would be compared on different conversations, and one run
  would be several hundred thousand tokens of generation.

**Which level of the standard the host claims.**

- Adopted: Level 2. It is what the issue asks for (the prompt, the declared tools, the
  persistence policy), it is the level the standard's worked example and host test 35 assume,
  and it is what a plain chat loop can do.
- Rejected for now: Level 3. The Roman Catholic example's depth is in a skill and bundled
  texts, so at Level 2 that pane answers from its prompt and says it cannot open its
  catechism. Level 3 would mean giving the model a way to read package files on demand and
  managing an 88,000-character text inside a 64K window. It is open question 3.

**How a model's prompt-on-top behaviour is tested when the package says `omit`.**

- Adopted: against a temporary copy of the package with the value changed. The host stays
  conforming and the collection is untouched.
- Rejected: a switch in the host that overrides a package's `prompt` value. It would be a
  private extension, and a way to do what the standard says a host does not do.

**How the controls are offered.**

- Adopted: as pane configurations the user chooses, labelled as controls. The issue asks for
  a "prompt only" pane, and without it nothing shows what reinjection adds.
- Rejected: leaving them out for the sake of conformance. The comparison is the point of the
  arrangement.

**How the Claude Code adapter is attached.**

- Adopted: the adapter is a command that takes the package's location, and it prints the hook
  configuration for the user to put in place. The same command then serves a package
  installed as a plugin, a marketplace entry and plain settings, and package folders stay as
  the standard defines them.
- Rejected: adding hook files to each package in `values/`. That changes the collection and
  copies the adapter into every package.
- Rejected: a forced output style carrying the wrapped prompt. It cannot reinject, and it
  replaces Claude Code's own instructions unless told otherwise.

## Open Questions

**Critical** (blocks progress)

None for writing the plan. One practical matter blocks the live checks: this project had no
Tinker access when the spec was written, and the owner has been asked for it. Live
verification is the plan's first step. Access through the account that trained the checkpoint
would not settle finding 3 of part 12, which needs a second account. Unless one is provided,
that finding is reported as not verified.

**Important** (shapes the design; each has a recommended answer above, and the owner decides)

1. **The length of the prompt fade demonstration.** The declared checkpoint has a
   65,536-token window and no larger copy. Recommended: keep the demonstration under 64K for
   now. Because the host's model is a setting and matching is by exact `base`, a 256K entry
   added to the package later would be picked up by running the host on the 256K base model,
   with no change to the host. The alternatives are to re-save the checkpoint at 256K, or to
   declare the earlier-stage 256K copy as well. Both are changes to `values/example-islam`
   and belong to the owner.
2. **What "live link" means.** Recommended: the host reads a directory on the machine it runs
   on, each time the list is asked for, by default the repository's own `values/`. Fetching
   from GitHub belongs with hosting, which is out of scope. A deployment can point the setting
   at a checkout it keeps up to date.
3. **Level 2 or Level 3.** At Level 2 the Roman Catholic pane answers from its prompt and
   says it cannot open its catechism, because that package keeps its depth in a skill and
   bundled texts. Recommended: Level 2 in this project, as the standard's own host test
   expects, with Level 3 as later work if the owner wants that pane to quote its sources.
4. **Replies written in advance.** The long script uses them so that the long stretch is the
   same in every pane and a run is quick and cheap. They are always shown as written in
   advance. Recommended: yes. The alternative is a fully generated conversation, which is
   slower, costs far more and compares panes on different histories.

**Nice-to-know** (does not block)

5. Whether replies can be shown as they are generated when the model is also calling tools.
   The provider's documentation does not say how streamed tool calls are assembled. The plan
   settles it after the first live call. Showing each reply when it is complete is
   acceptable.
6. Whether the model's reasoning is shown in the pane. Recommended: hidden by default and
   available in the view of what the model was sent.
7. Whether Claude Code keeps the order of several hook outputs, so that the preamble comes
   before the wrappers. Checked with a real session and reported.

## Test Scenarios

Without a network, against a stand-in model and a stand-in tool server:

1. **Fixtures.** Every valid fixture gives the expected wrapper as the system prompt and the
   expected reminder. Every invalid fixture is refused. The unsupported-version fixture is
   reported as one the host cannot judge.
2. **The collection.** The four example packages are listed. A folder added while the host is
   running appears at the next listing. A broken package beside valid ones is refused and the
   others still load.
3. **Nothing installed.** No system prompt, no tools, no reminder.
4. **Reminder timing.** Messages totalling just under the interval attach no reminder. The
   next user message after the interval is passed carries one, in the standard's form. The
   count then starts again.
5. **One large tool result.** A result many times the interval produces one reminder.
6. **Custom interval and section.** A package with its own `every-tokens` and `section` is
   reinjected at that interval with that section.
7. **A body that is its own core.** For `example-principled-pluralism` the reminder carries
   the whole body.
8. **Prompt only.** The control attaches no reminder however long the conversation, and is
   labelled a control.
9. **Two value systems.** Preamble, two wrappers in order, separate counts, each reminder
   when due. The same name twice is refused.
10. **Model matching.** An entry whose `base` equals the host's model is offered. With the
    host's model set to any other name, including the same model at another context length,
    it is not.
11. **Mode B.** With `prompt: optional` and the model chosen with the prompt, the wrapper is
    sent to the declared model and no reminder is attached.
12. **Mode C.** With `prompt: omit`, nothing from the package is sent, the tools are still
    offered, and the pane carries the disclosure and the statement that the prompt is not
    injected.
13. **Modes not offered.** Mode C is not offered for `required` or an absent `prompt`. Mode B
    is not offered for `omit`. Mode C is not offered with two value systems active.
14. **Model fails to load.** The stand-in refuses the declared model. The pane names it and
    continues in mode A with the wrapper and reinjection.
15. **Consent.** No connection is made before consent. The request shows the address. After
    declining, the package is active with no tool and the pane says so. After consenting, the
    tool is offered. Consent for one package's server does not cover another's.
16. **Local server.** Not started, and shown as such.
17. **Server unreachable.** Shown as not connected, and the conversation continues.
18. **Tool round trip.** The model's call reaches the stand-in server, the result returns as
    a tool result, and both are shown in the pane. A turn that reaches the limit on tool
    calls stops with a message.
19. **Level 3 package on this host.** `example-roman-catholic` activates, its skill and texts
    are not offered, and its prompt is complete.
20. **Context window.** A conversation at its window stops with a message. Nothing earlier is
    dropped.
21. **One pane fails.** The stand-in fails for one pane. That pane shows the error and the
    others finish.
22. **Markup.** A package body, a model reply and a tool result that contain markup are shown
    as text.
23. **Script.** User turns go to every pane. A reply written in advance appears in every pane,
    marked as such, and counts toward the interval. Probes are marked in the record.
24. **Record.** A saved record holds each pane's configuration and messages, and contains no
    key.
25. **No key.** The host refuses to start and says what is missing.
26. **Adapter, session start.** The output carries the expected wrapper for a fixture, and
    does so again for each kind of session start.
27. **Adapter, reminder.** With a transcript shorter than the interval there is no output.
    Past the interval the output carries the expected reminder, and not again until the
    interval passes once more.
28. **Adapter, refusals.** An invalid package and an over-long rendering are each refused
    with an error.
29. **Adapter, configuration.** The printed configuration for one package and for two is
    well formed, with the preamble separate.

With the real provider and tool (live):

30. **The endpoint.** Inkling 2 Small answers with a system prompt, and calls a tool.
31. **Ansari.** The Islam pane calls `answer_islamic_question` for a ruling and reports what
    came back.
32. **The checkpoint.** The declared model loads from `base` and `adapter`, in mode C.
33. **Three value systems.** One question, three panes, three answers each from its own
    value system.
34. **Prompt fade.** The long script runs in all four panes for `example-islam`.
35. **The wrapper's rules.** One probe or more for each of the seven.
36. **Prompt on top of the checkpoint.** The temporary copy, in mode B.
37. **Claude Code.** A session with the adapter in place names the installed value system
    when asked.

Non-functional:

38. **No copies.** `reference/` contains no package, schema or normative text.
39. **Honesty of the display.** A control is never shown without its label, and a reply
    written in advance is never shown as a pane's own.

## Risks and Mitigation

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Inkling 2 Small does not call tools reliably through this endpoint. | Medium | High | It is the first live check. If it fails, the architect is told at once. The host still shows the tool as connected and unused, and the wrapper tells the model to say when it cannot reach a source. |
| No provider access during the project. | Medium | High | The host is built and tested against stand-ins. Every live criterion is reported as not verified, and the architect is told which. |
| The declared checkpoint does not load with the key the project is given. | Low | Medium | The fine-tuned pane reports the failure and falls back to mode A, as the standard says. The result is itself the answer to finding 3, and goes to the architect. |
| Prompt fade does not show within 64K, so the four panes look alike. | Medium | Medium | The project's job is to make the comparison possible and report what it shows. A result of "no visible fade at this length" is recorded as a finding, with open question 1 as the way to go further. |
| The wrapper wording proves weak on this model. | Medium | Medium | That is a finding for the standard, reported with the record. The wording is not patched here. |
| A reply written in advance is taken for a real answer. | Low | Medium | It is marked wherever it is shown and in the record, and probes are always answered by the model. |
| A control pane is taken for conforming behaviour. | Low | Medium | Controls are labelled in the pane and described in the README. |
| The key leaks into a record, a log or the page. | Low | High | The key stays in the server process. A test checks that no record contains it. |
| A tool result or a package body tries to instruct the model or the page. | Medium | Medium | Tool results go only where tool results go. Everything from a package, model or tool is displayed as text. The standard already treats this content as untrusted. |
| Pull request #4 changes after this spec is approved. | Medium | Medium | The host takes the rules from the checker and the texts from `spec/` and holds no copy, so most changes arrive without work here. A change to a run-time rule goes through the architect. |
| Claude Code's hook behaviour differs from its documentation, or changes. | Medium | Low | The adapter is checked against a real session, and the README records the version it was checked with. |
| The estimate of four characters to a token is far off for this model. | Low | Low | The provider's reported counts are in every record, so the review can say how far off it was. A large gap is a finding. |
| The project grows: a host, a script player and an adapter in one piece of work. | Medium | Medium | The plan orders the work so that the chatbot is complete before the adapter starts. If something must be left out, the architect decides what. |

## References

- Issue #2 (this work), with the checkpoint details in its first comment and the architect's
  starting notes in its second. Issue #1 (the standard) and issue #3 (the collection).
- The standard's approved spec: `codev/specs/1-values-md-standard-v0-1-the-va.md`, on pull
  request #4. Parts 3 to 11, and host tests 31 to 40.
- The standard's files on pull request #4: `spec/schema/`, `spec/prompts/`, `spec/fixtures/`,
  `spec/checker/`, and the example packages in `values/`.
- Tinker, OpenAI-compatible inference: https://tinker-docs.thinkingmachines.ai/inference/openai/overview/
  and https://tinker-docs.thinkingmachines.ai/inference/openai/chat-completions/ (read on
  2026-11-20).
- Tinker checkpoints: https://tinker-docs.thinkingmachines.ai/tinker/howto/checkpoints/ (read
  on 2026-11-20).
- Ansari MCP server: https://github.com/ansari-project/ansari-mcp, hosted at
  `https://mcp.ansari.chat/mcp` (called on 2026-11-21 UTC).
- Model Context Protocol: https://modelcontextprotocol.io/
- Claude Code hooks: https://code.claude.com/docs/en/hooks.md. Plugin manifest reference:
  https://code.claude.com/docs/en/plugins-reference.md. Marketplaces:
  https://code.claude.com/docs/en/plugin-marketplaces.md (read on 2026-11-20).
