# Specification: Reference implementation — a public side-by-side chatbot on Inkling 2 Small

<!--
SPEC vs PLAN BOUNDARY:
This spec defines WHAT and WHY. The plan defines HOW and WHEN.
Keep implementation phases, file paths, code, and "first we will… then we will…"
out of the spec — those belong in codev/plans/<id>-*.md.
-->

Issue: #2. Protocol: SPIR. The repository has three parts: `spec/` (the standard, issue #1),
`reference/` (this project) and `values/` (the collection of value systems, issue #3). This
project builds what goes under `reference/` and puts it on the internet. It changes nothing
under `spec/` or `values/`.

The first draft of this spec described a chatbot that a person ran on their own machine. The
owner did not approve it. His words, on 2026-11-21: "I want it to be runnable so people can
experiment with it on the internet no local operation required." This revision is for a
service at a public address.

"The standard" below means the values.md standard v0.1 as its approved spec and its
specification text state it (`codev/specs/1-values-md-standard-v0-1-the-va.md` and
`spec/specification.md`, on pull request #4 until that merges). "Part N" means part N of that
spec's Desired State section. "V1" to "V10" are its validity rules. "Host test 31" to "host
test 40" are the ten scenarios it lists under "Defined here, exercised by a host (issue #2)",
which the specification text states as requirements H1 to H10, in the same order.

Terms used here, beyond the standard's own (value system, package, host, steward, prompt fade,
collection, modes A, B and C):

- **The service**: the chatbot running at a public address.
- **Visitor**: a person who opens the service in a browser. In the standard's terms the
  visitor is the user.
- **Operator**: whoever runs the service and pays for it. For the public service this is the
  values.md project. In the standard's terms this is the operator.
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
- **Recording**: a record the project made and published, opened in the window to be read.

## Problem Statement

The standard says what a host does with a values package: how it reads `VALUES.md`, what text
it puts in front of the model, when it repeats the core, what it does with a declared
fine-tuned model, what it asks consent for and what it shows the user. Nothing runs those
rules yet. The standard's own project checks packages and renderings and stops there, because
it ships no host. Ten of its test scenarios are handed to this project by name.

Three groups of people are affected:

- **Someone deciding whether the standard is worth adopting** cannot see what it does. A
  rendered prompt in a text file does not show that the same question gets a different,
  tradition-grounded answer once a value system is installed. Most of these people will not
  clone a repository, obtain a model key and run a server to find out. They will follow a
  link.
- **A host developer** has no working host to read or to compare their own against.
- **The standard's authors** do not know whether the wrapper wording holds on a real model,
  whether reinjection does anything about prompt fade, or whether a fine-tuned model can stand
  in for the prompt. These are open risks in the standard's spec, and each is assigned to this
  project to test.

Prompt fade is the hardest of these to show. It appears only in a long conversation, and it
can only be seen by comparison: the same conversation, with and without the thing that is
meant to prevent it.

A public service brings problems a program on one's own machine does not have. The model
costs money for every token and the visitor is not the one paying. One of the example
packages sends questions to a tool that somebody else runs. Anyone, or any program, can call
a public address. And people will type things about their faith and their lives into it.

## Current State

- `reference/` does not exist. There is no host for the standard anywhere, and nothing a
  person can open to try it.
- The standard is specified and built on pull request #4, which has not merged: the
  specification text, the rationale, the compatibility note, the schema, the three normative
  prompt texts, the fixtures, a checker, and the four example packages in `values/`. Two
  changes to it are expected before it merges (see Assumptions).
- The checker decides validity and renders the wrapper and reminder. By design it is not a
  loader and talks to no model.
- A package installed in Claude Code as a plugin gets its skills and MCP servers and not its
  prompt. The standard's compatibility note describes an adapter that would supply the prompt
  through hooks, and leaves building it to this project. The note also finds that a hook
  cannot place the text where the standard requires (part 11).
- Issue #3, a public browser for the collection, is starting. It and this service are both
  public pages over the same `values/` directory.

What was checked for this spec, and what is only reported:

| Subject | Finding | Status |
|---|---|---|
| Inkling 2 Small on Tinker | `thinkingmachines/Inkling-2-Small` answers on the OpenAI-compatible endpoint at `https://tinker.thinkingmachines.dev/services/tinker-prod/oai/api/v1`. It followed a system prompt. Offered a tool, it called it, with `finish_reason` `tool_calls`, and built its answer on the tool result sent back. It took a user message made of two text blocks, and a system message in the middle of a conversation. Its reasoning comes back in `reasoning_content`, apart from `content`. Replies carry `usage` with prompt, completion and cached token counts, and the second call of a turn was partly served from the prompt cache. Replies took one to three seconds. The endpoint refused a request sent with a programming library's default client name (HTTP 403) and accepted the same request under a named client. | Checked by calling it, 2026-11-21 05:20 UTC. |
| The declared checkpoint | `example-islam` declares one model: provider `tinker`, base `thinkingmachines/Inkling-2-Small`, a 65,536-token window, `prompt: omit`. It loaded when addressed by its path alone (about 13 seconds the first time) and as `<base>;<path>` (3 seconds). It returns no reasoning. It followed a system prompt and accepted tool definitions. A path that does not exist gives HTTP 404, "Weights not found". The check used the account that trained it. Loading it from another account is still untested. | Checked by calling it, 2026-11-21 05:20 UTC. |
| What the model costs | Published prices for Inkling 2 Small, per million tokens: $0.30 for input, $0.03 for input served from the prompt cache, $1.00 for output. A fine-tuned checkpoint is priced the same. No fee by the hour. No spending cap or limit on a key was found in the documentation. An account can be paid for in advance with credits. | Pricing page dated 2026-10-19, read on 2026-11-21. |
| Tinker for a public service | The documentation says the endpoint "is designed for testing your models, and you can also use it for production traffic". The terms allow use "in connection with your products or services", and allow the provider to throttle or suspend access without notice. No rate limit is published. Two pages disagree on whether Inkling 2 Small is among the models served in the beta of serverless inference. | Read on 2026-11-21. The owner's account, and his call. |
| Ansari | The MCP server at `https://mcp.ansari.chat/mcp` answered `initialize` (protocol `2024-11-05`, server "Ansari" 1.0.0) and listed one tool, `answer_islamic_question`, taking a `question` string. It needs no key, answers in plain JSON and issues no session identifier. | Checked by calling the server, 2026-11-21 03:11 UTC. |
| The example packages | `example-islam` has a remote tool and a declared model. `example-roman-catholic` has no tool and no model. Today its depth is a skill and bundled texts. It is about to change on pull request #4 to carry no bundled catechism and to take its detail from web search. `example-principled-pluralism` and `plain-speaking` are `VALUES.md` alone. | Read on pull request #4. The change is reported by the architect and not yet on the branch. |
| Claude Code hooks | `SessionStart` and `UserPromptSubmit` hooks can add context. `SessionStart` fires on start-up, resume, clear, compaction and fork. Claude Code puts a hook's text into the conversation inside a system reminder, at the point where the hook fired, and not into the system prompt. Each such string is capped at 10,000 characters, measured separately for each hook. Text over the cap is replaced by a file path and a preview of its first 2,000 characters. A hook receives the path of the transcript and no running token count, except that `SessionStart` on resume or fork receives `context_tokens`. The documentation says text a hook supplies is saved in the transcript. | Documentation read on 2026-11-20. To be confirmed by running it. |
| Where a small service can run | Five platforms were compared from their own pricing pages (see Solution Approaches). One small instance that stays up costs between about $4 and $31 a month depending on the platform. | Read on 2026-11-21. Some figures could not be read and are marked there. |

## Desired State

A person follows a link. The page that opens shows a window of panes, each with a value
system from the collection installed, and one box to type in. They type a question once. Each
pane answers it from a different value system, or from the same value system run a different
way, and each pane shows what is installed, who vouches for it and what the model was actually
sent. They install nothing, bring no key and create no account.

The operator pays for the model, so the service limits what one visitor and all visitors
together can spend in a day. It keeps no conversation after the visit, and it sends a question
to a package's tool only after that visitor has agreed.

The rest of this section states what is built. The reasoning and the alternatives are under
Solution Approaches.

### 1. What is delivered

Under `reference/`, and nowhere else:

1. **The chatbot**: a host for the standard, used through a browser page, built to run as a
   public service.
2. **What it takes to run the service**: the description of the service that a hosting
   platform builds and runs, the settings and their defaults, and an operator's guide: how to
   deploy it, set its key and limits, watch what it spends, and switch it off.
3. **Scripts**: a format for a conversation written in advance, at least one long script that
   ships with the project, and a way to play a script without the browser.
4. **Recordings**: the records of the runs behind the project's findings, which the service
   can show.
5. **The Claude Code prompt adapter**: what gets a package's prompt and reminder into a
   Claude Code session, as far as Claude Code's hooks allow.
6. **A README** that says what is here, the public address, what level of the standard the
   host claims, and how to run it on one's own machine.

Outside `reference/`: whatever the hosting platform or the repository needs at a fixed place
for the service to be deployed when `main` changes.

In the project's review document: the findings in part 12.

And the service itself, running at a public address (part 14).

### 2. The host

- It claims **Level 2** of the standard: it reads `VALUES.md`, injects the wrapper, addresses
  prompt fade, discloses what is installed, and connects the remote MCP servers a package
  declares. It does not expose `skills/` or `references/`, and it starts no local MCP server.
- It talks to one provider, Tinker, through the OpenAI-compatible endpoint. Its own model is
  `thinkingmachines/Inkling-2-Small`. The model name is a setting, so that the same host can
  be run on another base model without a change to its code.
- It adds no instructions of its own to the conversation, and gives the model no tools of its
  own. A pane with nothing installed has no system prompt and no tools, and a pane with a
  value system has exactly the text and the tools the standard puts there. What differs
  between two panes is then only what the standard does.
- Every pane uses the same generation settings. The limit on a reply is 8,192 tokens, which
  covers the model's reasoning and its answer. Any other setting is left at the provider's
  default unless it is set for all panes at once. A model request that has not finished in
  300 seconds has failed. These figures are settings, and these are their defaults.
- It implements nothing the standard does not define. Where the host needs a rule the standard
  lacks, the gap is written down as a finding (part 12) and the simplest behaviour is chosen
  and stated.
- **Who is who.** The standard leaves some choices to "the user or operator". Here the
  operator decides what the service offers at all: which collection, which model, whether
  declared models may be used, and the limits. Within that, the visitor chooses what each
  pane runs and gives or withholds consent. The host makes neither kind of choice on its own.

### 3. The link to the collection

- The host reads value systems from one directory, the collection. It reads the directory
  each time the list of value systems is asked for and each time a pane is set up. It keeps no
  copy of any package anywhere.
- The service is built from the repository. Its collection is the `values/` directory of the
  commit it was built from, and the schema and normative prompt texts it uses are the `spec/`
  of that same commit. The standard and the packages a visitor sees therefore always belong
  together.
- **How a merged value system reaches the service.** A change to `main` deploys the service
  again, by itself, with nobody doing anything. A value system merged into `values/` is in the
  service when that deployment finishes, which is a matter of minutes. The page shows which
  commit it is serving, as a link to that commit.
- A deployment ends the conversations in progress (part 13). A visitor whose conversation
  ends this way is told that the service was updated.
- Every folder in the collection is checked against V1 to V10 before it is offered. A valid
  package can be activated. An invalid one is listed as refused, with the identifiers of the
  rules it breaks, and cannot be activated. One that targets a later version of the standard
  is listed as one this host cannot judge. Nothing is repaired or truncated.
- A visitor can activate only packages from the collection. The service takes no package from
  a visitor: not as a file, not as pasted text, not as an address.
- **This is not a second catalogue.** The service lists what a visitor needs in order to
  choose panes, and what the standard requires a host to show before a value system is
  activated (part 8). For anything more about a package, each entry links to that package's
  page in the collection's browser (issue #3). The address of the browser is a setting, and
  the links appear once it is set.

### 4. The window

- The window holds two to four panes, side by side. There is one message box. A message is
  sent to every pane at once, and each pane keeps its own conversation.
- Panes work at the same time. A pane that is slow or fails does not hold up the others. A
  failure is shown in the pane it happened in, in plain words, and that pane stops.
- Two arrangements are offered ready-made:

  | Arrangement | Panes |
  |---|---|
  | **Value systems** (what a visitor sees first) | `example-islam`, `example-roman-catholic` and `example-principled-pluralism`, each on the host's own model with the prompt and reinjection (mode A). |
  | **Prompt fade**, for one value system the visitor picks | (1) Base model: nothing installed. (2) Prompt only: the wrapper is injected and the core is never reinjected. (3) Prompt with reinjection: mode A. (4) Fine-tuned model: a model the package declares, in the mode its `prompt` value allows. |

- The visitor can also set each pane by hand: any valid package in the collection, several
  packages together, or none, and any way of running that part 6 allows.
- A pane's configuration is fixed once the first message of a conversation has been sent.
  Changing any pane starts a new conversation in every pane, so that the panes are always
  being compared on the same messages.
- Panes 1 and 2 of the prompt fade arrangement are controls. A conforming host always
  reinjects, and a package cannot turn reinjection off. Pane 2 leaves it out on purpose, at
  the visitor's choice, to show what reinjection changes. Each is labelled as a control, and
  the page and the README say that a control is not conforming behaviour.
- The fourth pane is offered only for a package that declares a model matching the host's
  (part 6), and only while the operator allows declared models. Otherwise the arrangement has
  three panes and says why.
- The page works on a narrow screen. Panes that do not fit side by side are reached one at a
  time, and the message box still sends to all of them.

### 5. What a pane puts in front of the model

Exactly what parts 3, 4, 5 and 10 of the standard say:

- **The wrapper** goes in the system prompt, once, rendered from the normative text with the
  package's name, steward name and body.
- **Reinjection.** The host counts the tokens added to the conversation since the value
  system's text was last placed: the user's messages, the model's replies and reasoning, tool
  calls and tool results. The count starts at zero when the wrapper is placed and returns to
  zero after each reminder. The system prompt, the definitions of tools and a value system's
  own reminder are not counted. When the count has reached the package's interval, the
  reminder is placed at the start of the next user message, before the user's own text and
  apart from it. A value system gets at most one reminder at a boundary, however large its
  count.
- **The form of the reminder.** The standard says that where the API has content blocks, the
  reminder is a block of its own and the first block of the message. This endpoint takes a
  list of text blocks for this model, so that is the form the host uses.
- **Counting.** The host has no tokenizer for the model, so it uses the standard's estimate
  of one token for every four characters. This makes the placing of reminders the same on every
  run of the same text, and testable without a model.
- **Several value systems in one pane.** The preamble comes first, then one wrapper per
  package in the order the visitor activated them. Each package has its own count and its own
  interval, and each one that is due gets its reminder, in activation order. A second package
  with a name already active in that pane is refused.
- Every reminder stays in the conversation. The host drops none.
- The pane shows the visitor's message as they typed it, and marks each turn where a reminder
  was attached. It shows each package's running count against its interval. The visitor can
  open a view of exactly what the model was sent for that pane: the system prompt and every
  message, reminders included.

### 6. Declared models

The host follows part 6 of the standard.

- **Matching.** A package's `models` entry matches when its `provider` is `tinker` and its
  `base` is exactly the name of the host's own model. Nothing else matches, and entries that
  do not match are ignored.
- **Addressing.** The host addresses a declared model as the entry's `base`, a semicolon and
  its `adapter`. It needs nothing that is not in the package.
- **Modes.** The host offers mode A always, mode B for an entry whose `prompt` is `required`
  or `optional`, and mode C for an entry whose `prompt` is `optional` or `omit`. It does not
  offer mode C for `required` or for an entry with no `prompt` value, and does not offer mode
  B for `omit`. In mode B it does not reinject the package that declares the model. Any other
  package active in the same pane is reinjected as usual. Mode C is offered only when that
  package is the only one active in the pane.
- **Who chooses.** The operator decides whether declared models may be used on the service at
  all. Within that, the visitor chooses. The host never moves a pane to a declared model, and
  never drops the prompt, without the visitor having chosen that for that pane. Choosing the
  prompt fade arrangement is such a choice, and the arrangement says what its fourth pane
  will run before it starts.
- **Mode C.** Before a pane starts in mode C, the host says what that gives up: none of the
  wrapper's rules and none of the body's instructions are in context, and how the model
  behaves rests on its weights. Tools the package declares stay connected.
- **A model that fails to load.** The pane says which model failed, and goes on in mode A:
  the host's own model, with the prompt and reinjection. It does not go on in mode C without
  the model and does not try another entry.
- **The context window.** A pane's window is the entry's `context-window` for a declared
  model and a setting for the host's own model, 65,536 by default. Before each request the
  host works out the size of everything it is about to send, at one token for every four
  characters: the system prompt, every message, reasoning, tool calls and results, and
  replies written in advance (part 9). If that size plus the limit on a reply is more than the
  window, the pane stops and says so. It does not drop or shorten earlier turns to make room.
  If the provider refuses a request as too long all the same, the pane shows the refusal and
  stops. The token counts the provider reports are shown in the pane and kept in the record.
  They are what spending is worked out from (part 13). They are not what the host decides
  the window by.

### 7. Tools

- When a package with an `.mcp.json` is activated, the host connects each remote server it
  declares and offers that server's tools to the model. What a tool returns goes back to the
  model as a tool result and nowhere else. It is never added to the system prompt.
- Both kinds of remote server the standard allows are supported: `http`, which is also what a
  server with no `type` is taken to be, and `sse`. The host uses an existing MCP client
  library and writes no transport of its own. It offers a server no capabilities, so anything
  a server asks of the host is declined.
- **Consent, for each visitor.** Before the service first sends anything of a visitor's to a
  declared server, it asks that visitor, naming the package and the server and showing the
  address, and saying that their questions will be sent there and who runs it is not the
  values.md project. Consent is given for one package and one server, by one visitor, for one
  visit. It is not remembered between visits and one visitor's consent never stands for
  another's. If the visitor declines, the package is still activated, without that server's
  tools, and the pane shows that the tool is not connected.
- Listing a server's tools tells the model what the server offers and sends it nothing of a
  visitor's. The service may do that once for all visitors. No call that carries a visitor's
  words is made without that visitor's consent.
- A run from the command line (part 9) has nobody to ask. Consent is then given in the
  command itself, by naming the package and the server, and the run prints each address it
  connects to before it starts. A server not named there is not connected, and the record
  says so.
- **Where the service will connect.** Only to the address a package declares, and only if
  that address is on the public internet. An address that resolves to the service's own
  machine or to a private network is refused. The service does not follow a redirect to
  another address. A server that cannot be used for either reason is shown as not connected.
- **Local servers.** The host starts none, as the standard allows. A package that declares
  one is still activated, and the pane shows that the server was not started.
- A server that cannot be reached is shown in the pane as not connected. The conversation goes
  on without its tools.
- The pane shows each tool call and what came back.
- A turn may make at most eight tool calls. When the model asks for several at once they are
  made in the order given, and each one counts. A turn that reaches the limit stops with a
  message saying so.
- A tool call that has not answered in 120 seconds has failed. A failed call is reported to
  the model as failed, so that it can say it could not reach its source, and is shown in the
  pane. Both figures are settings, and these are their defaults.
- Tools stay connected in every mode, mode C included.

### 8. What the visitor is shown

Before a value system is activated, in the place where it is chosen:

- its name, description, steward, kind of claim and steward address, and its version;
- where it came from: its folder in the collection, as a link to that folder at the commit
  being served;
- the tools it declares, by server name and address, and the models it declares, each with
  its provider, base, adapter, `prompt` value and description;
- a link to its page in the collection's browser, once that address is set.

For as long as it is active, at the head of its pane:

- its name, steward, kind of claim and source;
- which model is answering, and when that is a declared model, that it is a fine-tuned model
  and which one;
- whether the prompt is injected and whether the core is reinjected;
- the word "control" on a pane that is one.

This holds in every mode. In mode C it is the only thing that tells the visitor what is
installed, so the pane also says that the prompt is not injected.

On the page at all times, where a first-time visitor will see it:

- that this is an experiment, and that what the model says is not religious, legal or
  medical advice and is not a ruling;
- that the example value systems are illustrative and are endorsed by no religious authority
  and by nobody they describe;
- where what the visitor types goes: to the model's provider, and, only if they agree, to the
  operator of a package's tool; and that the service itself keeps none of it (part 13);
- who runs the service, and a link to the repository.

The page shows everything that comes from a package, a model or a tool as text. None of it is
run or treated as markup by the browser.

### 9. Scripts and the long conversation

Prompt fade shows only in a long conversation, and nobody can type one by hand several times
over. So the conversation can be written down and played.

- A script is a list of turns in order. A turn is a user message, and is one of two kinds.
  An ordinary turn carries a reply written in advance, which is used in every pane in place of
  calling the model. A probe carries none: it is a question whose answers are the ones worth
  comparing.
- A reply written in advance lets a long stretch of conversation be the same in every pane and
  costs no model call. Such a reply is always shown as written in advance and not as that
  pane's own answer. It counts toward the reinjection interval like any other text, so
  reminders fall where they would have fallen in a live conversation.
- A probe is always answered by the model. The question and the answer are shown in the pane
  and kept in the record, and then left out of what the pane carries forward. Every pane
  therefore goes on from the same conversation, whatever it answered, and an early answer
  given from inside a value system cannot prop up a later one.
- A probe is sent with whatever any user message would carry at that point, including a
  reminder if one is due. Because the probe is not carried forward, it does not return the
  count to zero. The reminder is attached again to the next message that is carried forward.
- A conversation typed into the window has no probes. Every reply in it comes from the model
  and everything in it is carried forward.
- One long script ships with the project. It is long enough to pass the reinjection interval
  at least five times, comes to no more than 50,000 tokens by the host's own count, so that it
  fits the 65,536-token window with room for a reply, and has probes before the first interval
  and near the end. Any text in it that the project did not write is in the public domain and
  says where it came from.
- **For a visitor.** A visitor can play the long script into the prompt fade arrangement. The
  long stretch appears at once, since it calls no model. The probes are answered live, and
  afterwards the visitor can type questions of their own into all four panes, at the far end
  of the long conversation. Each such question sends the whole conversation to four models,
  so it draws on the visitor's allowance much faster than an ordinary question, and the page
  says so before the script is played.
- **For the project.** A script can also be played from the command line with no browser,
  against the same arrangements. This is how the runs behind the findings are made.
- The service plays only the scripts that ship with it. It takes no script from a visitor.

### 10. Records and recordings

- **The service stores no conversation.** What a visitor types, and what the models and tools
  answer, is held in the service's memory for the length of the visit and nowhere else. It is
  not written to a disk or a log, and it is gone when the visit ends, after 30 minutes with
  no activity, or when the service restarts.
- A visitor can save their own run as a record, to their own machine. The service makes the
  record, hands it to the browser and keeps no copy.
- A record holds, for each pane, its configuration, the model addressed, the generation
  settings, and every message sent and received in order, with reminders, tool calls, tool
  results, the token counts the provider reported and the times. It holds no key, no request
  header, no network address and nothing that identifies the visitor or a machine. It names a
  package by its folder in the collection and the commit.
- **The project's own records.** The runs behind the findings in part 12 are made from the
  command line and saved as records. Those records are kept in the repository, in a place of
  their own under `reference/`. Only records of scripted runs made for the findings are kept
  there, and each is read through before it is committed.
- **Recordings.** The service can open one of those committed records in the window, pane by
  pane, as it would show a live run. A recording is marked as a recording wherever it is
  shown, with the date it was made and the commit it was made at. Opening one calls no model
  and no tool, so recordings stay available when a limit has been reached or live chat is
  switched off (part 13).
- A record quotes what was sent, so it contains rendered prompt text. That is output. The
  rule that `reference/` keeps no copy of a package or a normative text is about what goes
  into a prompt, and nothing from a record ever does.

### 11. The Claude Code prompt adapter

This part is not changed by hosting. The adapter is a tool a person runs with their own
Claude Code, on their own machine.

A package loaded in Claude Code as a plugin has its tools and skills and nothing of its
prompt. The adapter supplies the prompt and the reminder through Claude Code's hooks.

**It does not make Claude Code a conforming host**, and nothing this project writes says that
it does. The standard's compatibility note (`spec/compatibility.md`, "Where this departs from
the specification") sets out where a hook adapter departs from the standard, and the adapter's
README repeats it:

- **Placement.** The standard places the wrapper in the system prompt. Claude Code puts a
  hook's text into the conversation, inside a system reminder, at the point where the hook
  fired.
- **Exactness.** The standard has a host change nothing in the text. Claude Code adds its own
  framing around a hook's text, and rewrites a `<system-reminder>` tag if the text contains
  one.
- **Once.** The standard places the wrapper once. A session start fires for five reasons, and
  whether text a hook added earlier is still in the conversation after some of them is not
  documented.
- **A reminder can be lost.** A hook that reaches its time limit has its output discarded,
  and the prompt goes to the model without it.
- **Not only the user.** The hook that carries the reminder also fires for some messages the
  user did not type, where the standard's boundary is what the user sends.
- **Order.** With several value systems the standard puts the preamble first and the
  wrappers in activation order. The order in which several hooks' outputs arrive is not
  documented.

The standard is about to be changed, on pull request #4, so that an adapter outside the host
may place the wrapper at the start of the conversation if it says that it does. The adapter
says so, in its README and wherever it describes itself, in the words the final text of the
standard asks for. That change is about placement. The other five points stand, and the
adapter goes on naming them.

What the adapter does:

- **The wrapper.** At a session start it emits the rendered wrapper for a package the user
  has chosen to install, according to why the session started:

  | Kind of session start | What the adapter does |
  |---|---|
  | Start-up | Emits the wrapper. |
  | Clear | Emits the wrapper. The conversation that held it is gone. |
  | Compaction | Emits the wrapper. The conversation that held it has been replaced by a summary. |
  | Resume, fork | Emits the wrapper only if the conversation being continued does not already hold it. |

- **The reminder.** It emits the reminder with the user's next prompt once the conversation
  has grown by the package's interval since that package's text was last placed. Claude Code
  gives a hook no running token count, so the adapter works the count out from the session's
  transcript, at one token for every four characters. The transcript can run a turn behind
  the conversation, which the interval, being approximate, allows for.
- **Where it last placed a package's text.** It looks in the transcript for what it emitted
  itself: the most recent wrapper or reminder carrying that package's name. It counts what
  comes after that. It keeps no state of its own between runs, so two hooks running at once,
  or a restart, cannot put it out of step. The same look tells it, on a resume or a fork,
  whether the wrapper is already there.
- This rests on Claude Code writing hook-supplied text into the transcript, as its
  documentation says. It is the first thing checked against a real session. If it does not
  hold, the adapter instead keeps, for each session and package, the position in the
  transcript of its last placement and nothing else, and the plan says so before the adapter
  is built.
- **Validity.** It uses the same reading, validity and rendering rules as the chatbot. A
  package that is not valid is refused with an error naming the rule, and nothing is
  emitted. This is the one place a package loaded in Claude Code is checked, since Claude
  Code's own plugin validation does not apply the standard's rules.
- **The size cap.** It refuses, with an error naming the package and the sizes, to emit a
  text over Claude Code's cap of 10,000 characters. It does not truncate, and it does not
  leave Claude Code to replace the text with a preview. Claude Code's documentation does not
  say what it counts as a character, so the adapter counts the stricter way, in UTF-16 code
  units.
- **Several packages.** It emits one output for each package and the preamble as an output of
  its own, because the cap is measured on each output alone.
- **Installation.** It prints the hook configuration for a given list of packages, ready to
  put into Claude Code's settings, a plugin manifest or a marketplace entry. Nothing is
  installed without the user doing so. Putting that configuration in place is the explicit
  installation the standard requires.

The compatibility note was written from documentation, and marks several things as not
tried. The adapter is where they are tried. The review reports what a real session showed for
each of these: whether hook text is in the transcript, whether it survives a resume, a fork
and a compaction, and the order in which several outputs arrive.

### 12. What this project finds out

The standard hands these to this project. Each is tried against the real model or the real
tool, and the result goes in the review with the date and the record behind it. Each is
either answered or reported as not verified, with the reason. None is ticked on trust.

1. Whether Inkling 2 Small on Tinker takes a system prompt and calls tools through this
   endpoint, and its exact model name. Answered for this spec (see Current State). The review
   records it with the first full run.
2. How the declared checkpoint is addressed, and whether `base` and `adapter` are enough.
   Answered for this spec: they are.
3. Whether the declared checkpoint loads from an account other than the one that trained it.
   The access this project has is through the account that trained it, so this is reported as
   not verified unless a second account is provided.
4. Whether the wrapper wording holds on the real model. There is at least one probe for each
   of the wrapper's seven rules.
5. How the declared checkpoint behaves with the value-system prompt on top of it. The package
   declares `prompt: omit`, so a conforming host will not run that combination. The test is
   run from the command line against a temporary copy of the package, outside the collection
   and never on the public service, with the value changed to `optional`. The result is a
   recommendation to keep `omit` or change to `optional`.
6. What the prompt fade arrangement shows on the long script: how the four panes answer the
   same probes early and late. The fine-tuned pane differs from the base pane in two ways, not
   one: its weights, and the package's tools, which stay connected in mode C with nothing in
   context telling the model to use them. The review says so when it reads that pane.
7. What a real Claude Code session shows for the behaviours the compatibility note could
   only take from documentation (part 11).
8. Anything the host needed that the standard does not define, and anything in the standard
   that could not be implemented as written.
9. What the service cost to run in its first days: what a typical question and a prompt fade
   run cost against the estimates in part 13, and how far the host's estimate of four
   characters to a token was from the counts the provider reported.

Probe answers are judged by reading them, and the review says so. This is a demonstration
with its evidence attached. It is not a benchmark, and it makes no claim beyond the
conversations it ran.

Findings about the standard or the examples are reported to the architect and listed in the
review. This project does not change `spec/` or `values/` to act on them.

### 13. The public service: limits, abuse and privacy

**Whose key and whose bill.** The service holds one Tinker key, the operator's. It stays in
the service's process. It is never sent to a browser, written to a record or a log, or
printed. A visitor needs no key and cannot supply one.

**What the model costs.** At the published prices, and before any saving from the prompt
cache:

| What a visitor does | Roughly what it sends | Roughly what it costs |
|---|---|---|
| One question in the value systems arrangement, three panes | 3 × (2,000 to 6,000 tokens in, about 1,000 out) | under 1 cent |
| One question at the end of the long script, four panes | 4 × (about 50,000 tokens in, about 1,000 out) | about 6 cents |
| The long script from start to finish, with its probes | a few such questions, most of them early and small | about 10 to 15 cents |

A question that leads a pane to call a tool sends that pane's conversation once more for
each call, so it costs that pane up to twice as much for one call and more for several.

Much of what is sent in a long conversation is the same from one request to the next, and
the provider charges a tenth of the price for input it has cached, so the real figures should
be lower. Finding 9 reports what they turned out to be.

**Limits on spending.** The service works out what each request cost from the token counts
the provider reports and the provider's prices, which are settings. It keeps two running
totals for the day. It checks both before it starts a turn, and again before each further
model request inside a turn, such as the one that follows a tool call:

| Limit | Default | When it is reached |
|---|---|---|
| One visitor, one day | $0.50 | That visitor is told they have used today's allowance and when it starts again. A turn in progress stops where it is, and says why. Recordings stay open to them. |
| All visitors, one day | $5.00 | Every visitor is told that the service has used its allowance for the day and when it starts again. Turns in progress stop where they are. Recordings stay open. |

- Both are settings. The defaults put the most the model can cost at about $150 a month if
  the daily limit were reached every day.
- At prices before any saving from the cache, a visitor's default allowance covers about
  fifty ordinary questions, or the long script and about five questions after it. The
  service's covers ten visitors a day who each use all of theirs. These are first figures.
  They are set again once finding 9 says what the service really costs.
- A request already sent to the model is allowed to finish. The largest request the service
  will send costs about 3 cents. A visitor's total can therefore pass its limit by the four
  requests of one turn, about 10 cents, and the service's by the sixteen it allows at once,
  about 40 cents.
- The totals are numbers only, and they are kept across a restart, so that deploying the
  service does not hand everyone a fresh allowance.
- "A visitor" for this purpose is a network address, as the hosting platform reports it.
  People who share an address share an allowance. The page says so when a limit is reached.
- The provider offers no spending cap of its own that this project could find. The service's
  own limit is therefore the only automatic one. The operator's guide recommends paying for
  the service's account in advance with a fixed amount of credit, so that there is a ceiling
  even if the service's own limit fails.

**Limits on use.** These bound how hard one visitor or one program can drive the service,
whatever it costs:

- A message is at most 4,000 characters.
- One visitor has one turn in progress at a time, and at most 20 turns in any 10 minutes.
- The service has at most 16 model requests in progress at once. Beyond that, a visitor is
  told the service is busy and asked to try again shortly.
- The service makes at most 500 calls a day to any one declared tool server, so that it
  cannot be used to flood somebody else's server. When that is reached, the tool is shown as
  not available for the rest of the day and conversations go on without it.
- A visitor reaches a model and a tool only through a pane. The service offers no way to send
  a request of the visitor's own making to either.

All of these are settings, and these are their defaults.

**Switching it off.** The operator can switch live chat off with one setting. The page then
says so and shows recordings only.

**What is logged.** For each turn: the time, which packages and modes the panes had, the
token counts, the cost, how long it took and whether it failed and how. To apply the limits,
the service keeps a visitor's network address in a form that cannot be turned back into the
address and that changes every day. Nothing a visitor typed, nothing a model or tool
answered, and no network address in plain form is logged by the service. The hosting platform
keeps its own request logs, which the service does not control, and the page's privacy note
says so.

**What is not stored.** No conversation (part 10). No account, because there are none. No
cookie beyond the one that ties a browser to its conversation for the length of the visit.

**Who else sees what a visitor types.** The model's provider receives every conversation. A
package's tool receives the questions the model puts to it, and only after that visitor's
consent (part 7). The page says both, plainly, before the visitor types anything.

**What the service does not do.** It does not moderate what visitors type or what the model
says beyond what the model does itself. It adds no instructions of its own (part 2), because
a reference implementation that quietly added a safety prompt would no longer be showing what
the standard does. The limits above, the notices in part 8 and the off switch are what stand
between the service and misuse. This is a judgement for the owner, and it is open question 5.

**Security.**

- The service is reached over HTTPS only.
- A request that sends a message or changes anything is accepted only from the service's own
  page. Another site open in the visitor's browser cannot use the visitor's allowance or read
  their conversation.
- The page loads no script, style or font from anywhere but the service itself, and tells the
  browser to run nothing else.
- One visitor cannot reach another's conversation.
- Everything from a package, a model or a tool is shown as text (part 8).
- The service's key, its settings and its logs are reachable only by the operator.

### 14. Where it runs, and what running it involves

- **One instance.** The service runs as a single small instance that stays up. Conversations
  and consent live in its memory, so there is exactly one of it. It is restarted by each
  deployment.
- **Where.** The recommended platform is in Solution Approaches, with the alternatives and
  what each costs. The owner decides. The service asks only this of a platform: that it
  builds and runs a container from the repository when `main` changes, keeps one instance
  up, holds one secret, keeps a small amount of data across restarts for the day's totals,
  lets a response stay open for five minutes, and gives the service an HTTPS address.
- **The address.** The platform's own address to begin with. A name of the project's own can
  be put in front of it later with no change to the service.
- **What it costs to keep up.** Hosting, at the recommended platform, about $5 to $20 a
  month. The model, whatever visitors use, up to the daily limit: at most about $150 a month
  at the defaults, and probably a small part of that. Nothing else.
- **The first deployment** is made with the owner's hosting account and on his say-so. This
  project prepares everything a deployment needs and checks it on a private address first.
  It puts nothing at a public address without that say-so.
- **On one's own machine.** The same program runs on a person's own machine with their own
  key, for development and for anyone who wants to. It is no longer how people are expected
  to use it. One documented command starts it. Without a key it does not start, and says what
  is missing.
- The project's tests run with no network and no key, against a stand-in for the model and a
  stand-in for a tool server. Checks that need the real provider, the real tool or the real
  service are separate, and are run and reported with their dates.

## Success Criteria

Criteria marked (live) need the real provider, tool or service. If one cannot be run, it is
reported as not verified in the review and to the architect.

Scope and layout

- [ ] Everything this project adds is under `reference/`, apart from Codev artifacts and what
      the platform or repository needs at a fixed place for deployment. Nothing under `spec/`
      or `values/` is changed. `reference/` holds no copy of a package, the schema or a
      normative prompt text that could go into a prompt. Records are kept apart, and nothing
      from a record goes into a prompt.
- [ ] The README gives the public address, the level claimed, which panes are controls, and
      one command that starts the host on a person's own machine. The operator's guide says
      how to deploy, set the key and limits, see what was spent, and switch live chat off.

The public service

- [ ] (live) The service answers at a public HTTPS address. A person with a browser, no key,
      no account and nothing installed can open it, see the value systems arrangement, type a
      question and get an answer in each pane.
- [ ] (live) After a change to `values/` is merged to `main`, the service is deployed again
      with nobody doing anything, the change is in the list, and the page shows the new
      commit.
- [ ] The page shows the commit it is serving, as a link to that commit.

Limits

- [ ] A visitor whose spending for the day has reached their limit cannot start a turn, and
      a turn of theirs in progress makes no further model request. The visitor is
      told so and when the allowance starts again, and can still open recordings. The same
      holds for every visitor when the service's limit for the day is reached.
- [ ] Spending is worked out from the token counts the provider reports and the prices held
      as settings, with cached input at its own price. Both daily totals survive a restart.
- [ ] A message over 4,000 characters is refused. A visitor's second turn while one is in
      progress is refused, and so is a 21st turn within 10 minutes. A 17th model request at
      once is answered with a message that the service is busy.
- [ ] The 501st call in a day to one tool server is not made, and the tool is shown as not
      available.
- [ ] With live chat switched off, no turn can be started, the page says so, and recordings
      open.
- [ ] A visitor has no way to supply a key, a package, a script or a request of their own
      making to a model or a tool.

Privacy

- [ ] After a conversation, nothing the visitor typed and nothing a model or tool answered is
      in any file or log the service writes. A conversation left idle for 30 minutes is gone
      from memory.
- [ ] The service's logs hold, for each turn, the time, the pane configurations, token
      counts, cost, duration and outcome, and no network address in a form that can be read
      back.
- [ ] A record a visitor saves reaches only their browser, and holds no key, request header,
      network address or anything identifying the visitor.
- [ ] The page states, where a first-time visitor sees it before typing: that this is an
      experiment and not advice or a ruling; that the examples are illustrative and not
      endorsed; that what is typed goes to the model's provider and, with consent, to a
      tool's operator; that the service keeps none of it; and who runs it.

Security

- [ ] A request to send a message or change anything that does not come from the service's
      own page is refused.
- [ ] One visitor's conversation cannot be read or continued with another visitor's
      identity.
- [ ] The page loads nothing from another origin, and text from a package, a model or a tool
      that contains markup is displayed as text.
- [ ] A declared server whose address resolves to the service's own machine or a private
      network is not connected. A server that redirects to another address is not connected.
- [ ] No record, log or response contains the key.

The collection

- [ ] The list of value systems is read from the collection directory each time it is asked
      for. A valid package folder added to that directory appears in the list at the next
      refresh, with no other change.
- [ ] An invalid package in the collection is listed as refused with its rule identifiers and
      cannot be activated. A package targeting a later `spec-version` is listed as one the
      host cannot judge.
- [ ] For every valid fixture in `spec/fixtures/`, the system prompt the host would send
      equals the fixture's expected wrapper, and the reminder it would attach equals the
      expected reminder. For every invalid fixture, the host refuses the package.
- [ ] With the address of the collection's browser set, each listed value system links to its
      page there. With it not set, there is no such link and nothing else changes.

The prompt and reinjection

- [ ] A pane with one value system sends a system prompt that is exactly the rendered
      wrapper. A pane with nothing installed sends no system prompt and no tools.
- [ ] Host test 31: with the default interval, the first reminder is attached to the first
      user message after 5,000 counted tokens, as the first content block of that message,
      with the user's text unchanged in the block after it. Nothing is attached before that.
      One very large tool result produces one reminder, not several.
- [ ] A package's own `every-tokens` and `section` values are honoured.
- [ ] Host test 36: with two value systems in a pane, the preamble comes first, each package
      has its wrapper in activation order and its own count, and each core is reinjected
      when due. A second package with the same name is refused.
- [ ] With two value systems in a pane and one of them on its declared model in mode B, that
      package gets no reminder and the other is reinjected when due.
- [ ] The pane marks the turns that carried a reminder, and the view of what the model was
      sent shows the full text of each one.

Declared models

- [ ] Host test 33: with the host's model set to a name that matches no entry, the package's
      `models` are ignored and the pane runs in mode A.
- [ ] Host test 32: with an entry whose `prompt` is `required` or `optional`, the visitor can
      choose mode B. The wrapper is injected, no reminder is attached, and the pane shows
      that a fine-tuned model is in use and names it.
- [ ] Host test 38: with `prompt: omit`, or `optional` and the visitor choosing to drop the
      prompt, nothing from the package is sent to the model. The pane still shows the name,
      steward, kind of claim and source, names the model, and shows that the prompt is not
      injected. The host said what mode C gives up before the pane started.
- [ ] Host test 39: with `prompt: required`, or with the field absent, mode C is not offered.
- [ ] Host test 40: with two value systems active in a pane, mode C is not offered for
      either.
- [ ] Host test 34: when a declared model fails to load, the pane names the model that
      failed and continues in mode A.
- [ ] No pane runs a declared model, or runs without the prompt, unless the visitor chose
      that for that pane. With declared models switched off by the operator, none is offered.
- [ ] A pane whose next request, by the host's count, would not fit its context window with
      room for a reply stops and says so before anything is sent. A pane the provider refuses
      as too long shows the refusal and stops.

Tools

- [ ] Host test 37: nothing of a visitor's is sent to a declared server before that visitor
      has consented for that package and that server, and the request for consent shows the
      address. Declining leaves the package active without that tool, and the pane says so.
- [ ] One visitor's consent does not carry to another visitor, or to the same visitor's next
      visit.
- [ ] A package that declares a local server is activated with that server not started, and
      the pane says so.
- [ ] Host test 35: a package with `skills/` and `references/` is activated with both
      ignored, its prompt complete and any remote tool working.
- [ ] A tool result reaches the model only as a tool result. Tool calls and results are
      visible in the pane.
- [ ] A turn stops with a message at its ninth tool call. A tool call with no answer in 120
      seconds is reported to the model as failed. A model request with no answer in 300
      seconds fails in its own pane while the other panes complete.
- [ ] A declared server of type `http` and one of type `sse` can each be connected.
- [ ] From the command line, a declared server is connected only when the command names its
      package and server, and the address is printed first.
- [ ] (live) In a pane with `example-islam` on the host's model, a question asking for a
      ruling or a verse leads to a call to `answer_islamic_question`, and the answer is built
      on what came back.

Disclosure

- [ ] Before activation the visitor is shown the name, description, steward, kind of claim,
      version, source, declared tools and declared models. While a value system is active its
      pane shows the name, steward, kind of claim, source, the model in use, whether the
      prompt is injected and whether the core is reinjected.

The window, scripts, records and recordings

- [ ] One typed message is sent to every pane. A failure in one pane is shown there and the
      other panes complete.
- [ ] The value systems arrangement opens with the three example packages named by the owner.
      The prompt fade arrangement opens with the four panes of part 4 for a package that
      declares a matching model, and with three, and the reason, for one that does not.
- [ ] On a narrow screen every pane can be reached and one message still goes to all.
- [ ] Playing a script sends the same user turns to every pane. A reply written in advance is
      used in every pane, is shown as written in advance, and counts toward the interval.
- [ ] A probe is answered by the model, shown and recorded, and absent from every later
      request. After a script with probes, the turns each pane carries forward are the same
      in every pane. A reminder attached to a probe is attached again to the next turn that is
      carried forward.
- [ ] The long script that ships with the project passes the default interval at least five
      times and comes to no more than 50,000 tokens by the host's count.
- [ ] A visitor can play the long script into the prompt fade arrangement and then type a
      question of their own into all four panes. The page says beforehand that this draws on
      the allowance faster.
- [ ] A script can be played from the command line, and the run saved as a record that holds
      each pane's configuration, the generation settings and every message sent and
      received. Every pane in a run has the same generation settings.
- [ ] A committed record opens in the window as a recording, marked as one with its date and
      commit, and opening it calls no model and no tool.
- [ ] Once a conversation has started, changing a pane's configuration starts a new
      conversation in every pane.
- [ ] (live) The prompt fade arrangement completes the long script for `example-islam` in
      all four panes, and the record is kept and can be opened on the service as a recording.

The Claude Code adapter

- [ ] For each valid fixture, the adapter's output at a start-up, a clear and a compaction
      is exactly the expected wrapper. At a resume and a fork it is the expected wrapper when
      the transcript does not hold one for that package, and nothing when it does.
- [ ] Its reminder output is exactly the expected reminder once a transcript has grown by
      the interval since the package's text was last placed, and nothing before that.
- [ ] It refuses an invalid package with the rule named, and refuses a rendered text over
      10,000 UTF-16 code units, without truncating either.
- [ ] It prints a hook configuration for one package and for several, with one output per
      package and the preamble on its own.
- [ ] The README states that the adapter does not make Claude Code a conforming host, says
      where it places the wrapper in the words the standard asks for, lists the departures
      of part 11, and points to the standard's compatibility note. Nothing in `reference/` or
      the pull request claims otherwise.
- [ ] (live) In a Claude Code session with `example-islam` installed as a plugin and the
      adapter's hooks in place, the model, asked what value system is installed, names it and
      its steward.
- [ ] (live) The review reports, from real sessions, whether hook-supplied text is written
      into the transcript, whether it is still in the conversation after a resume, a fork and
      a compaction, and in what order several outputs arrive. The adapter finds its last
      placement the way those results allow, and the review says which.

Findings

- [ ] The review answers each of the nine items of part 12, or reports it as not verified
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

Decided by the owner on 2026-11-21, copied from the issue. Also fixed.

- The chatbot runs on the internet. Anyone can open it in a browser and experiment with it,
  with no local installation or operation required. Hosting and public deployment are in
  scope.

From the issue's statement of what the chatbot should do. Also fixed.

- Load a values package exactly as the standard in `spec/` defines it, with no private
  extensions. If the implementation needs something the standard lacks, that is a finding for
  the standard.
- Inject the standard's system prompt, call the package's declared tools, and apply its
  persistence policy.
- Use a declared fine-tuned model when the package has one for the running base model.
- Make prompt fade visible: the panes should be able to show base model, prompt only, prompt
  with reinjection, and fine-tuned model on the same long conversation.

From the architect's notes on the issue (2026-11-21). Also fixed.

- The standard is read from pull request #4's branch until it merges, and from `main` after.
  Its files are not copied into `reference/`.
- This project builds the loader and everything a host does at run time, and the Claude Code
  prompt adapter.
- It tests a value-system prompt on top of the fine-tuned checkpoint, and the wrapper wording
  on a real model. A weak wrapper is a finding for the standard, not something to patch
  locally.
- Ansari is reached through its hosted MCP server, as `example-islam` declares it.
- The spec for a hosted service says: whose key and whose bill, with limits for one visitor
  and overall and what a visitor sees at a limit; what is limited and what is logged against
  abuse; how a value system merged into `values/` reaches the running service; that consent
  to a package's server is given by a visitor, for each visit; whether conversations are
  stored, with the default that they are not; and where it runs and what it costs, as a
  recommendation for the owner to decide.
- Running it on one's own machine can remain possible. It is no longer the way people are
  expected to use it.
- This project does not build a second catalogue. It lists what a visitor needs in order to
  pick panes, and links to the collection's browser (issue #3) for the rest.
- A Claude Code hook's text lands in the conversation inside a system reminder, not in the
  system prompt. The adapter is not claimed to make Claude Code a conforming host. This
  project says what it does and where it departs.

Out of scope, from the issue:

- Changes to the standard itself.

Further constraints:

- The repository is public. Nothing in `reference/`, the Codev artifacts or the pull request
  says where a credential is kept or names an account.
- Out of scope: the collection's browser, its submission check and its marketplace file
  (issue #3); Level 3 of the standard; local MCP servers; accounts and sign-in; storing
  conversations; taking a package, a script or a key from a visitor; a tool of the host's own
  such as web search; training or publishing a model; and translations of the normative
  texts or of the page.

## Assumptions

- Pull request #4 merges, or its branch is otherwise made available to this project's branch,
  before the implementation needs `spec/` and `values/` in the working tree. If it has not
  when implementation starts, the architect decides how this branch gets them.
- The specification text on pull request #4 is what the host is built to. It was read for
  this spec on 2026-11-21. Two changes to that pull request are expected and are allowed for
  here: the Roman Catholic example loses its bundled catechism and takes its detail from web
  search (open question 3), and part 4 is relaxed so that an adapter outside the host may
  place the wrapper at the start of the conversation if it says so (part 11). Any other change
  to a run-time rule goes to the architect.
- The provider's terms allow a public service of this kind on the owner's account, and the
  endpoint stays available to it. Both are the owner's to confirm. The provider may throttle
  or suspend access without notice, and the service then shows each pane's failure plainly.
- The provider's published prices are what the service is charged, and the token counts it
  reports are what it charges for.
- The declared checkpoint stays loadable with the service's key.
- The Ansari server stays available without a key, and the Ansari project is content for a
  public demonstration to call it up to the daily limit in part 13. The owner confirms this.
- The estimate of one token for every four characters is close enough for English text that
  reminders fall near every 5,000 tokens. The interval is approximate by the owner's own
  wording.
- Claude Code's hook behaviour is as its documentation says. The adapter is checked against a
  real session before its criterion is ticked.
- A network address is a good enough stand-in for a visitor to apply a daily allowance. It is
  not exact: people behind one address share an allowance, and one person can come from
  several.
- The service gets light use. One small instance is enough, and what happens beyond that is
  that visitors are told it is busy.

## Solution Approaches

### The form of the service

The owner fixed the window as side by side and the chatbot as something anyone can open on
the internet. What remains open is what kind of thing serves it.

### Approach 1: A small web service that holds the key (recommended)

One server process holds the key, the conversations in progress, the tool connections and the
limits, and serves one page with the panes. The server is written in Python and the page
needs no build step. It runs as one instance on a hosting platform.

- For: the key never leaves the server. Python is what the standard's checker is written in,
  so the host uses the checker's reading and validity rules directly, and one toolchain serves
  the repository. The same program runs on a person's own machine. Limits, consent and
  privacy are all enforced in one place.
- Against: a server to keep up and pay for, and a restart ends the conversations in progress.
- Risk: low.

### Approach 2: A page with no server, where each visitor brings a key

A static page calls the model from the browser with a key the visitor pastes in.

- For: nothing to host but files, and no bill for the operator.
- Against: a visitor has no key, which is the whole of the owner's objection to the first
  draft. The standard's rules would have to be written a second time in the browser's
  language. A browser cannot call most tool servers directly.
- Risk: it does not meet the requirement.

### Approach 3: A ready-made hosted demo kit

Platforms for machine-learning demos give a chat page for very little code.

- For: the least work for a first screen, and an audience that already looks there.
- Against: these kits own the layout and the conversation. Several conversations fed from
  one box, with reminders, per-visitor consent, a disclosure header on each pane and spending
  limits, means working against the kit. Limits on spending would still have to be built.
- Risk: medium.

### Approach 4: Functions that start on each request, with no instance that stays up

- For: costs nothing while nobody is visiting.
- Against: conversations, consent and open tool connections would have to live somewhere
  outside the process, which means a store, which is the thing part 10 says the service does
  not have. Long open responses and cold starts fit this model poorly.
- Risk: medium. More moving parts for a saving of a few dollars a month.

Approach 1 is recommended.

### Where it runs

Read from each platform's own pages on 2026-11-21. Costs are for one small instance that
stays up.

| Platform | Cost a month | Notes |
|---|---|---|
| Railway (recommended) | $5 plan, including $5 of use. An instance of half a processor and 512 MB to 1 GB comes to about $15 to $20 if it were busy all the time, and is charged by actual use, so less for a service that is mostly idle. | Has a usage limit the account holder sets. Keeps data across restarts on a volume. Whether it deploys from GitHub on a push, and its limit on an open response, were not on the pages read and are to be confirmed before the choice is final. |
| Fly.io | About $4 to $7 for the smallest shared instances. | Can stop an idle instance, which this service cannot use while conversations are in memory. No spending cap found. |
| Render | A free instance exists but sleeps after 15 minutes, takes about a minute to wake, and may be suspended for making many calls to outside services, which is what this service does. The price of the smallest paid instance could not be read. | Deploys on a push to a linked branch. |
| Hugging Face Spaces | $9 for the account that a container-based Space needs, on free hardware that sleeps after 48 hours idle, or about $31 with hardware that stays up. | Where many people look for demonstrations of models. Deploys from its own repository, not from GitHub. |
| Google Cloud Run | Prices could not be read. | Responses may stay open up to 60 minutes. Scales to nothing when idle, which has the same difficulty as approach 4. |

Railway is recommended: it keeps one instance up for a few dollars, has a limit on what the
account can be charged, and keeps the day's totals across a restart. The service asks nothing
of a platform that the others do not also offer (part 14), so the choice can be changed
later. The owner decides.

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

**How a merged value system reaches the service.**

- Adopted: the service is deployed again whenever `main` changes, and reads the collection
  from the commit it was built from. The packages, the normative texts and the checker a
  visitor gets are then always from one commit, and nothing is fetched while the service
  runs.
- Rejected: the running service fetches `values/` from GitHub from time to time. A newly
  merged package would appear without a deployment, but the service would be running
  packages against a copy of the standard from a different commit, would need a cache and
  an answer for when GitHub does not respond, and would be executing whatever is at an
  address rather than what was built and tested. It would arrive only a few minutes sooner.

**Where a conversation lives.**

- Adopted: in the service's memory, for the length of the visit. Nothing is written anywhere,
  which is the simplest way to be able to say that nothing is stored.
- Rejected: in a database. It would let a conversation survive a restart and let the service
  run as several instances, and it would be a store of what people typed about their faith.
- Rejected: in the visitor's browser, sent back whole with each message. The service would
  hold nothing between requests. But every request would carry the whole conversation, up to
  a megabyte for four long panes, and the service would have to treat its own past output as
  untrusted input each time.

**What the limits are counted in.**

- Adopted: money, worked out from the provider's reported token counts and its prices. It is
  the thing the operator cares about, and it treats a short question and a question at the
  end of a 50,000-token conversation according to what each really costs.
- Rejected: a number of messages. A message in the prompt fade arrangement costs about
  thirty times what a message in the value systems arrangement costs.
- Rejected: the host's own estimate of four characters to a token. The provider's counts are
  what the bill is made from, and they are free with every reply.

**What a visitor may bring.**

- Adopted: nothing but questions. Packages come from the collection, which is reviewed
  before anything is merged. Scripts ship with the service.
- Rejected: letting a visitor paste a `VALUES.md` of their own to try. It would be a good way
  to try a value system before submitting it, and it would put any text anyone likes behind
  the project's public address and the operator's key. It is named under open questions as
  later work.

**How tokens are counted for reinjection.**

- Adopted: one token for every four characters, the standard's rule for a host with no
  tokenizer. It is the same on every run, the same in the chatbot and the adapter, and can be
  tested with no model.
- Rejected: the provider's reported token counts. They are exact, but they arrive only after
  a call, they include overhead the provider adds, and a reply written in advance has none.
  The same holds for the context window, where the host has to know whether a request fits
  before it sends it.
- Rejected: loading the model's tokenizer. It adds a dependency and a download for an
  interval the owner describes as approximate.

**Where the long conversation comes from.**

- Adopted: a script whose ordinary turns carry replies written in advance and whose probes
  are answered by the model and then left out of what is carried forward. The conversation
  is then identical in every pane from start to finish, a run costs a handful of model calls
  and takes minutes, and the result can be repeated. On a public service it also means a
  visitor can reach the far end of a long conversation in a second and for a few cents.
- Rejected: keeping each pane's probe answers in its conversation. The panes would drift
  apart from the first probe, and a pane that answered an early probe from inside its value
  system would have that answer in context as an example, which would hide the fade the
  arrangement is there to show.
- Rejected: typing it live. Nobody can type tens of thousands of tokens four times over.
- Rejected: a script of user turns only, with every reply generated. Each pane's history
  would then differ, and one run would be several hundred thousand tokens of generation.

**Which level of the standard the host claims.**

- Adopted: Level 2. It is what the issue asks for (the prompt, the declared tools, the
  persistence policy), it is the level the standard's worked example and host test 35 assume,
  and it is what a plain chat loop can do.
- Rejected for now: Level 3. On a public service it would mean letting the model read files
  from a package on demand, for every visitor. It is open question 3.

**How a model's prompt-on-top behaviour is tested when the package says `omit`.**

- Adopted: from the command line, against a temporary copy of the package with the value
  changed. The host stays conforming, the collection is untouched, and the public service
  never runs the combination.
- Rejected: a switch in the host that overrides a package's `prompt` value. It would be a
  private extension, and a way to do what the standard says a host does not do.

**How the controls are offered.**

- Adopted: as pane configurations the visitor chooses, labelled as controls. The issue asks
  for a "prompt only" pane, and without it nothing shows what reinjection adds.
- Rejected: leaving them out for the sake of conformance. The comparison is the point of the
  arrangement.

**How the Claude Code adapter is attached.**

- Adopted: the adapter is a command that takes the package's location, and it prints the hook
  configuration for the user to put in place. The same command then serves a package
  installed as a plugin, a marketplace entry and plain settings, and package folders stay as
  the standard defines them.
- Rejected: adding hook files to each package in `values/`. That changes the collection and
  copies the adapter into every package.
- Rejected: a forced output style carrying the wrapped prompt. It puts the text with Claude
  Code's instructions, which is nearer to where the standard wants it than a hook gets. But
  it cannot reinject, it carries one value system only, it overrides the style the user
  chose, and it drops Claude Code's own coding instructions unless told to keep them.

## Open Questions

**Critical** (blocks progress)

None for writing the plan. One practical matter blocks implementation, and the architect is
asked to settle it at the gate:

- **The standard's files.** This project's branch has no `spec/` and no `values/`, because
  pull request #4 has not merged. The plan can be written without them. The implementation
  cannot start without them, since its first tests run against the fixtures.

**Important** (shapes the design, and the owner decides)

Desired State is written on the recommended answer to each of these, so that the spec states
one design. If the owner decides otherwise at the gate, the spec is revised to match before
the plan is written.

Raised by hosting:

1. **Where it runs.** Recommended: Railway, as one instance that stays up, at the platform's
   own address to begin with. The alternatives and their costs are under Solution Approaches.
2. **The limits.** Recommended: $0.50 a day for one visitor and $5.00 a day for all visitors,
   which puts the most the model can cost at about $150 a month, and the limits on use in
   part 13. And that the service's account with the provider is paid for in advance with a
   fixed amount of credit, since the provider offers no cap of its own.
3. **The Roman Catholic pane and web search.** That example is changing to take its detail
   from web search. This host gives the model no tools of its own, and a search tool on a
   public service would be a second paid provider with its own key, limits and abuse to
   think about. Recommended: no search tool in this project. If the changed package declares
   a search server in `.mcp.json`, the host connects it like any other, with consent. If it
   relies on the host being able to search, this host cannot, the pane answers from its
   prompt, and the model says it cannot search. The alternative is to give every pane a
   search tool, which the owner would need to choose a provider and a budget for.
4. **Declared models on the public service.** Recommended: allowed. The fine-tuned pane is
   the fourth pane of the prompt fade arrangement, it costs the same per token as the base
   model, and without it the service cannot show one of the two ways the standard addresses
   prompt fade. The operator can switch it off.
5. **No moderation of the host's own.** Recommended: none beyond the model's own behaviour,
   the limits, the notices and the off switch (part 13). A reference implementation that
   added its own instructions would no longer show what the standard does. The cost is that
   the project's public address will sometimes show a model saying something the project
   would not. The alternative is a filter in front of the model, which is more to build and
   run and changes what is being demonstrated.
6. **Ansari on a public service.** The Islam pane sends visitors' questions to the Ansari
   server, with consent, up to 500 calls a day. Recommended: confirm with the Ansari project
   that it is content with that before the service is announced.

From the first draft, with hosting taken into account:

7. **The length of the prompt fade demonstration.** Unchanged. Recommended: keep it under
   64K, because the declared checkpoint has a 65,536-token window and no larger copy. Hosting
   adds a reason: at this length a visitor's question at the far end costs about 6 cents, and
   at four times the length it would cost four times as much.
8. **What "live link" means.** Changed by hosting. Recommended: the service is deployed again
   whenever `main` changes and reads the collection from the commit it was built from, so a
   merged value system is in the service within minutes and no copy is kept anywhere. The
   first draft's answer, a directory on the user's machine, still holds for a person running
   it themselves.
9. **Level 2 or Level 3.** Unchanged. Recommended: Level 2. The reason given in the first
   draft, a large bundled catechism, is going away with the change to the Roman Catholic
   example. What takes its place is question 3.
10. **Replies written in advance.** Unchanged. Recommended: yes. Hosting adds a reason: they
    are what let a visitor reach the end of a long conversation at once and for a few cents.

**Nice-to-know** (does not block)

11. Whether replies can be shown as they are generated when the model is also calling tools.
    The provider's documentation does not say how streamed tool calls are assembled. The plan
    settles it with a live call. Showing each reply when it is complete is acceptable.
12. Whether the model's reasoning is shown in the pane. Recommended: hidden by default and
    available in the view of what the model was sent.
13. Whether Claude Code keeps the order of several hook outputs, and whether it writes text
    supplied by a hook into the transcript. Both are checked with a real session and
    reported. Part 11 says what the adapter does in either case.
14. Letting a visitor try a value system of their own. Not in this project. It would need
    its own answer on what may be put behind the project's address.
15. A name of the project's own for the service, and whether the collection's browser and
    the chatbot should share one. Neither blocks anything here.

## Test Scenarios

Without a network, against a stand-in model and a stand-in tool server:

The host

1. **Fixtures.** Every valid fixture gives the expected wrapper as the system prompt and the
   expected reminder. Every invalid fixture is refused. The unsupported-version fixture is
   reported as one the host cannot judge.
2. **The collection.** The four example packages are listed. A folder added to the directory
   appears at the next listing. A broken package beside valid ones is refused and the others
   still load.
3. **Nothing installed.** No system prompt, no tools, no reminder.
4. **Reminder timing.** Messages totalling just under the interval attach no reminder. The
   next user message after the interval is passed carries one, as its first content block.
   The count then starts again. The system prompt, tool definitions and the reminder itself
   are not counted.
5. **One large tool result.** A result many times the interval produces one reminder.
6. **Custom interval and section.** A package with its own `every-tokens` and `section` is
   reinjected at that interval with that section.
7. **A body that is its own core.** For `example-principled-pluralism` the reminder carries
   the whole body.
8. **Prompt only.** The control attaches no reminder however long the conversation, and is
   labelled a control.
9. **Two value systems.** Preamble, two wrappers in order, separate counts, each reminder
   when due. The same name twice is refused. With one of the two on its declared model in
   mode B, only the other is reinjected.
10. **Model matching.** An entry whose `base` equals the host's model is offered. With the
    host's model set to any other name, including the same model at another context length,
    it is not.
11. **Mode B.** With `prompt: optional` and the model chosen with the prompt, the wrapper is
    sent to the declared model and no reminder is attached.
12. **Mode C.** With `prompt: omit`, nothing from the package is sent, the tools are still
    offered, and the pane carries the disclosure and the statement that the prompt is not
    injected.
13. **Modes not offered.** Mode C is not offered for `required` or an absent `prompt`. Mode B
    is not offered for `omit`. Mode C is not offered with two value systems active. No
    declared model is offered when the operator has switched them off.
14. **Model fails to load.** The stand-in answers "not found" for the declared model. The
    pane names it and continues in mode A with the wrapper and reinjection.
15. **Consent.** Nothing of a visitor's is sent to a server before that visitor consents. The
    request shows the address. After declining, the package is active with no tool and the
    pane says so. After consenting, the tool is offered. Consent for one package's server
    does not cover another's, one visitor's does not cover another visitor, and it is gone
    at the next visit.
16. **Local server.** Not started, and shown as such.
17. **Server unreachable.** Shown as not connected, and the conversation continues. The same
    for a server that redirects to another address, and for one whose address is the
    service's own machine or a private network.
18. **Tool round trip.** The model's call reaches the stand-in server, the result returns as
    a tool result, and both are shown in the pane, for a server of each type. A turn stops
    with a message at its ninth tool call. A call that does not answer in time is reported to
    the model as failed.
19. **Level 3 package on this host.** A package with `skills/` and `references/` activates,
    neither is offered, and its prompt is complete.
20. **Context window.** A request that would not fit, by the host's count and with room for a
    reply, is not sent, and the pane stops with a message. Nothing earlier is dropped. A
    refusal from the stand-in as too long is shown and the pane stops.
21. **One pane fails.** The stand-in fails for one pane, and in another run does not answer in
    time. That pane shows the error and the others finish.
22. **Markup.** A package body, a model reply and a tool result that contain markup are shown
    as text.
23. **Script.** User turns go to every pane. A reply written in advance appears in every pane,
    marked as such, and counts toward the interval. Probes are marked in the record.
24. **Probes.** With stand-in answers of different lengths in different panes, every later
    request carries the same turns in every pane and no probe. A reminder due at a probe is
    sent with the probe and again with the next turn that is carried forward.
25. **Record.** A saved record holds each pane's configuration, settings and messages, and
    contains no key, header, network address or anything identifying a visitor or machine.
26. **Recording.** A committed record opens in the window marked as a recording, and the
    stand-in model and tool server receive nothing.
27. **Changing a pane.** After the first message, changing a pane's configuration starts a
    new conversation in every pane.
28. **Command-line consent.** A script run with no server named connects to none. With the
    package and server named, it prints the address and connects.

The service

29. **A visitor's limit.** With the stand-in reporting token counts, a visitor's total
    reaches the limit. Their next turn is refused with the message, another visitor's is
    not, and recordings open. When the limit is reached by the first request of a turn that
    calls a tool, the request that would follow the tool call is not made, and the pane says
    why.
30. **The service's limit.** The total for all visitors reaches the limit. Every visitor's
    next turn is refused with the message, and recordings open.
31. **Cost.** For given reported counts of input, cached input and output, the cost recorded
    is what the prices give.
32. **Totals survive.** After a restart both totals are what they were.
33. **A new day.** Both totals start again, and a visitor refused yesterday can start a turn.
34. **Limits on use.** An over-long message, a second turn at once, a 21st turn in 10
    minutes, a 17th model request at once and a 501st tool call in a day are each refused
    with their own message.
35. **Off switch.** With live chat off, no turn starts and recordings open.
36. **Nothing stored.** After a conversation with distinctive text in the question, the reply
    and a tool result, that text is in no file or log the service wrote.
37. **Idle.** A conversation idle for 30 minutes is gone, and its visitor is told so on their
    next message.
38. **Logs.** A turn's log line has the fields of part 13 and no network address that can be
    read back.
39. **Another site.** A request to send a message that does not come from the service's own
    page is refused.
40. **Another visitor.** A request for one visitor's conversation with another's identity is
    refused.
41. **No key.** The program refuses to start and says what is missing. No response, record or
    log contains the key.
42. **What a visitor cannot send.** There is no request that accepts a package, a script, a
    key, a model name or a tool address from a visitor.

The adapter

43. **Session start.** For a fixture, the output is the expected wrapper at a start-up, a
    clear and a compaction. At a resume and a fork it is the expected wrapper when the
    transcript holds none for that package, and nothing when it holds one.
44. **Reminder.** With a transcript shorter than the interval there is no output. Past the
    interval the output carries the expected reminder, and not again until the interval
    passes once more, counted from the reminder found in the transcript. A session start in
    between starts the count again.
45. **Refusals.** An invalid package is refused with the rule named. A rendering over the cap
    is refused, including one that is under 10,000 code points and over 10,000 UTF-16 code
    units.
46. **Configuration.** The printed configuration for one package and for two is well formed,
    with the preamble separate.

With the real provider, tool and service (live):

47. **The endpoint.** Inkling 2 Small answers with a system prompt, and calls a tool.
48. **Ansari.** The Islam pane calls `answer_islamic_question` for a ruling and reports what
    came back.
49. **The checkpoint.** The declared model loads from `base` and `adapter`, in mode C.
50. **Three value systems.** One question, three panes, three answers each from its own
    value system.
51. **Prompt fade.** The long script runs in all four panes for `example-islam`.
52. **The wrapper's rules.** One probe or more for each of the seven.
53. **Prompt on top of the checkpoint.** The temporary copy, in mode B, from the command
    line.
54. **Claude Code.** A session with the adapter in place names the installed value system
    when asked, and its transcript shows whether the wrapper was written into it. Further
    sessions show what a resume, a fork and a compaction leave in the conversation, and the
    order of two packages' outputs.
55. **The public address.** From a browser with nothing installed and no key: the page
    opens over HTTPS, a question is answered in three panes, consent is asked before Ansari
    is called, and a recording opens.
56. **A merge reaches the service.** A change merged to `main` is deployed with nobody doing
    anything, and the page shows the new commit.
57. **A limit on the real service.** With a visitor's limit set very low for the test, the
    limit is reached and the message is shown.

Non-functional:

58. **No copies.** Apart from records, `reference/` contains no package, schema or normative
    text, and nothing from a record goes into a prompt.
59. **Honesty of the display.** A control is never shown without its label, a reply written
    in advance is never shown as a pane's own, and a recording is never shown as live.
60. **A narrow screen.** On a phone-sized screen every pane can be reached and one message
    goes to all.

## Risks and Mitigation

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| The service is driven hard by a program or a crowd and runs up a bill. | Medium | High | Two daily limits in money, checked before every turn, limits on use, and an off switch. The most the model can cost at the defaults is about $150 a month. The account is paid for in advance with fixed credit, so there is a ceiling even if the service's own limit fails. |
| The limit on one visitor is got round by changing network address. | High | Low | The limit on all visitors does not depend on telling visitors apart, and it is the one that bounds the bill. |
| The public address shows a model saying something offensive or wrong about a faith, under the project's name. | Medium | High | Notices on the page that this is an experiment, not advice and not endorsed. Example bodies are kept to high-consensus basics by the standard's own project. The off switch. Whether to add a filter is open question 5. |
| The service is used to send a flood of questions to Ansari. | Low | Medium | A daily cap on calls to any one tool server, the limits on use, and consent before any call. The owner confirms the arrangement with the Ansari project. |
| The provider throttles or suspends the endpoint, or stops serving this model on it. | Medium | High | Each pane shows its failure plainly. Recordings need no provider, so the page still shows something. The model name is a setting. The owner confirms that the account may be used this way. |
| Something a visitor typed is kept after all. | Low | High | Conversations are held in memory only. A test puts distinctive text through a conversation and looks for it in everything the service wrote. The page says plainly that the provider and, with consent, a tool's operator do receive it, and that the platform keeps its own request logs. |
| The key leaks into a record, a log or the page. | Low | High | The key stays in the server process. A test checks that no record, log or response contains it. |
| A deployment ends conversations in progress. | High | Low | The visitor is told the service was updated. Nothing is lost that was meant to be kept. |
| A package merged into `values/` declares a tool server or model that is costly or hostile, and the service runs it for every visitor. | Low | High | What is merged is decided by the collection's acceptance policy (issue #3). On the service's side: consent before any call, no private addresses, no redirects, a daily cap for each server, declared models switchable off, and the limits on spending. |
| A tool result or a package body tries to instruct the model or the page. | Medium | Medium | Tool results go only where tool results go. Everything from a package, model or tool is displayed as text, and the page runs nothing it did not ship with. |
| Prompt fade does not show within 64K, so the four panes look alike. | Medium | Medium | The project's job is to make the comparison possible and report what it shows. A result of "no visible fade at this length" is recorded as a finding, with open question 7 as the way to go further. |
| The wrapper wording proves weak on this model. | Medium | Medium | That is a finding for the standard, reported with the record. The wording is not patched here. |
| A reply written in advance, a control or a recording is taken for something it is not. | Low | Medium | Each is marked wherever it is shown and in the record, and described in the README. |
| The Roman Catholic pane can do little, because its package now relies on web search and this host has none. | Medium | Medium | Open question 3. The pane says what it cannot do, as the wrapper tells the model to. |
| Pull request #4 changes after this spec is approved. | High | Medium | Two changes are expected and allowed for. The host takes the rules from the checker and the texts from `spec/` and holds no copy, so most changes arrive without work here. A change to a run-time rule goes through the architect. |
| Claude Code's hook behaviour differs from its documentation, or changes. | Medium | Low | The adapter is checked against a real session, and the README records the version it was checked with. |
| The adapter is taken to make Claude Code a conforming host. | Medium | Medium | The README says it does not and lists the departures, in the compatibility note's own terms. A success criterion checks that nothing claims otherwise. |
| The declared checkpoint cannot be loaded by anyone but its trainer. | Low | Medium | Not something this project can test with the access it has. Reported as not verified. On the service it does not matter, since the service's key can load it. |
| The estimate of four characters to a token is far off for this model. | Low | Low | The provider's reported counts are in every record, so the review can say how far off it was. Spending does not depend on it. |
| The project has grown: a host, a public service with limits, a script player, recordings and an adapter. | High | Medium | The plan orders the work so that the host is complete and tested before the service is put in front of it, and the adapter comes last. If something must be left out or moved to later work, the architect decides what. |

## References

- Issue #2 (this work), with the checkpoint details in its first comment, the architect's
  starting notes in its second and the owner's decision on hosting in its third. Issue #1
  (the standard) and issue #3 (the collection and its browser).
- The standard's approved spec: `codev/specs/1-values-md-standard-v0-1-the-va.md`, on pull
  request #4. Parts 3 to 11, and host tests 31 to 40.
- The standard's files on pull request #4: `spec/specification.md` (parts 4 to 7, 10, 14 and
  15), `spec/compatibility.md` (the sections on hooks and on the hook size cap),
  `spec/schema/`, `spec/prompts/`, `spec/fixtures/`, `spec/checker/`, and the example packages
  in `values/`.
- Tinker, OpenAI-compatible inference: https://tinker-docs.thinkingmachines.ai/inference/openai/overview/
  and https://tinker-docs.thinkingmachines.ai/inference/openai/chat-completions/ (read on
  2026-11-20; the endpoint called on 2026-11-21).
- Tinker models and pricing: https://tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/
  and https://thinkingmachines.ai/tinker/pricing/ (dated 2026-10-19, read on 2026-11-21).
  Terms: https://thinkingmachines.ai/legal/terms/ (updated 2026-01-10, read on 2026-11-21).
- Tinker checkpoints: https://tinker-docs.thinkingmachines.ai/tinker/howto/checkpoints/ (read
  on 2026-11-20).
- Ansari MCP server: https://github.com/ansari-project/ansari-mcp, hosted at
  `https://mcp.ansari.chat/mcp` (called on 2026-11-21 UTC).
- Model Context Protocol: https://modelcontextprotocol.io/
- Claude Code hooks: https://code.claude.com/docs/en/hooks.md. Plugin manifest reference:
  https://code.claude.com/docs/en/plugins-reference.md. Marketplaces:
  https://code.claude.com/docs/en/plugin-marketplaces.md (read on 2026-11-20).
- Hosting, each read on 2026-11-21: https://railway.com/pricing and
  https://docs.railway.com/reference/pricing/plans; https://docs.fly.io/about/pricing;
  https://render.com/docs/free; https://huggingface.co/pricing and
  https://huggingface.co/docs/hub/spaces-overview;
  https://docs.cloud.google.com/run/docs/configuring/request-timeout.
