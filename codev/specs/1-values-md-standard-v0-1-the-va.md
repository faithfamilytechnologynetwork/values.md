# Specification: values.md standard v0.1 — the VALUES.md package format

<!--
SPEC vs PLAN BOUNDARY:
This spec defines WHAT and WHY. The plan defines HOW and WHEN.
Keep implementation phases, file paths, code, and "first we will… then we will…"
out of the spec — those belong in codev/plans/<id>-*.md.
-->

Issue: #1. Protocol: SPIR. The repository has three parts: `spec/` (the standard), `reference/`
(the reference implementation, issue #2) and `values/` (the collection of value systems, issue
#3). This project delivers the standard under `spec/` and the first four packages of the
collection under `values/`. It builds neither the reference implementation nor the collection's
browser and submission check.

Terms used throughout:

- **Value system**: a body of values that a person or community wants an AI model to answer
  from, such as a faith tradition, a professional code or a family's house rules.
- **Package**: the files that carry one value system. Either a single `VALUES.md` file or a
  folder with `VALUES.md` at its root.
- **Host**: the application that runs a model and installs a package (a chat product, a coding
  agent, a plain chat loop).
- **Steward**: the person or body that vouches for a package being a faithful statement of its
  value system.
- **Prompt fade**: a value-system prompt losing force as a conversation grows.
- **Collection**: a directory that holds many packages, one folder each. The `values/`
  directory at the root of this repository is one.

### The format at a glance

The owner's test for this format is that it is lighter than Belief Protocol. This is the
smallest valid `VALUES.md`, in full:

```markdown
---
name: plain-speaking
description: One person's rules for honest, direct advice.
steward:
  name: Sam Example
  claim: individual
---
Tell me the truth even when it is unwelcome. If I am wrong, say so and say why.
Do not flatter me. Give me your real view before you give me the alternatives.
When you are unsure, tell me you are unsure.
```

Three frontmatter fields and a body in ordinary prose. There is no folder, no required heading
and no required structure inside the body. For comparison, the smallest valid `BELIEF.md` needs
a `decision-surface` structure and an Agent Orientations section, and every belief in it must
carry a `layer`, a `grip` and a `source`.

**A first-time author can ignore** everything else in this specification:

- Every other frontmatter field. `version`, `license`, `tradition`, `languages`, `tags`,
  `authors`, `persistence`, `models` and `metadata` are all optional.
- The core section. A body of 1,500 characters or fewer is its own core.
- The folder and everything in it: `.mcp.json`, `skills/` and `references/`.
- The wrapper and reminder texts. The host supplies them.
- Conformance levels, collections and marketplaces.

**A Level 1 host can ignore:**

- `.mcp.json`, `skills/` and `references/`. Those are Levels 2 and 3.
- `models`. Using a declared model is always optional.
- `tradition`, `languages`, `tags`, `license`, `authors` and `metadata`. They are for listings
  and display.
- Collections, marketplaces and installing more than one value system at a time.

What a Level 1 host does do: read one file, check it against validity rules V1 to V6, put the
body inside the wrapper text, count tokens, add the reminder when the count passes the
interval, and show the user the name, the steward and the kind of claim.

## Problem Statement

Almost all questions about faith and values go to general-purpose assistants, not to
purpose-built ones. A person who wants answers grounded in their own tradition has two poor
choices today: use a separate custom assistant that few people will ever open, or paste a
prompt into a general assistant and hope it holds.

There is no portable way to hand a general assistant a value system. The existing formats each
cover one piece. AGENTS.md carries free-form instructions for a code repository. Agent Skills
carry on-demand procedures. MCP carries tools. Claude Code plugins bundle those for one product.
None of them says "this is the value system to answer from, here is who vouches for it, here are
its sources, and here is how to keep it in force over a long conversation".

The people affected are users who want tradition-grounded answers, communities that want to
state their values once and have them work in many assistants, and host developers who will
only adopt something that is cheap to implement. A custom assistant cannot reach the first
group, which is why the answer has to be a small package that general assistants can install.

## Current State

The table records what was checked on 2026-11-20 and how it differs from the research notes in
the issue. "Checked" means the source page or repository was read directly. Items marked
"summary only" were read through a page summary and need re-checking before the rationale
document relies on them.

| Subject | Finding | Status |
|---|---|---|
| AGENTS.md | Plain Markdown, no required fields, no schema. The nearest file to the edited file wins, and an explicit user prompt overrides it. Silent on frontmatter, tools, models, metadata and versioning. Stewarded by the Agentic AI Foundation under the Linux Foundation. | Checked. Matches the issue. |
| Agent Skills | Frontmatter fields are `name`, `description`, `license`, `compatibility`, `metadata` (string to string) and `allowed-tools` (experimental). `name` is 1 to 64 characters, lowercase letters, digits and hyphens, and must match the folder name. A skill folder may hold `scripts/`, `references/`, `assets/` and anything else. Name and description load at startup, the body on activation, other files on demand. The body should stay under 500 lines. | Checked. Matches the issue. |
| Agent Skills, unknown keys | The specification does not say what a client does with an unknown frontmatter key. The client guide says to warn and still load. The issue's claim that claude.ai uploads and the Skills API reject unknown keys was not verified. Ansari's own `SKILL.md` carries a non-standard `runtime` key. | Unverified. Does not affect the design, because new fields live in `VALUES.md`. |
| Claude Code plugins | The manifest is `.claude-plugin/plugin.json` and is optional. `name` is its only required key. Components sit at the plugin root: `skills/`, `commands/`, `agents/`, `hooks/hooks.json`, `.mcp.json`, `output-styles/` and others. An unknown top-level manifest key is stripped with a warning and the plugin still loads. A `CLAUDE.md` at the plugin root is not loaded as context. The documentation is silent on other unrecognised files at the root, such as `VALUES.md` or `references/`. | Checked. One gap: behaviour with extra root files must be tested. |
| Claude Code output styles | A plugin can ship an output style and force it on with `force-for-plugin: true`. A custom style drops Claude Code's built-in coding instructions unless `keep-coding-instructions: true` is set. | Checked. |
| Claude Code hooks | `SessionStart` and `UserPromptSubmit` can add context, through plain output or `additionalContext`. `SessionStart` fires again after compaction. Injected strings are capped at 10,000 characters. Hooks receive `transcript_path` and no running token count. One exception: `SessionStart` on resume or fork receives `context_tokens`. | Cap and common fields are summary only. Re-check before relying on them. |
| Belief Protocol | `BELIEF.md`, version 2.2, Apache-2.0. A schema for the beliefs themselves, with 10 structure types and per-belief attributes. Loaded at session start and kept active. Its "Agent Orientations" section of about 200 to 500 tokens is held in context throughout. It has nothing for tools, models, a host-side wrapper or reinjection, and calls itself complementary to Agent Skills. | Checked. Matches the issue. |
| Claude Code marketplaces | `.claude-plugin/marketplace.json` requires `name`, `owner` and `plugins`. Each plugin entry requires `name` and `source`. An entry name is letters, digits, `.`, `_` and `-`, starting with a letter or digit. A relative `source` starts with `./` and resolves from the marketplace root. An entry may also carry `description`, `version`, `author`, `homepage`, `license`, `category` (a string) and `tags` (a list of strings). A plugin folder with no `plugin.json` can be listed: "the entry is the manifest". An entry can declare hooks inline. | Checked. |
| Tinker fine-tunes | A checkpoint runs on the base model it was trained on. Sampler weights are addressed as `tinker://<run_id>/sampler_weights/<name>`. The OpenAI-compatible API accepts that path alone, or `<base model ID>;<path>` to select a context length. Publishing lets other accounts load a checkpoint. `thinkingmachines/Inkling-2-Small` is listed as a base model. | API forms checked. Publishing and the model list are summary only. |
| The project's fine-tuned checkpoints | Described in a comment on issue #2, as checked against the Tinker API on 2026-11-20. Stage 1 is a LoRA fine-tune of Inkling 2 Small: Islamic (Sunni), English only, trained to be good company for a practising Muslim and not to issue rulings, with no system prompt in training. Both the base model and that checkpoint honour a system prompt on the OpenAI-compatible endpoint. A value-system prompt on top of the fine-tune is untested. A later stage 2 checkpoint is the one the Islam example is to declare. Its base model, context window and publication status were still being confirmed when this was written. There is no Roman Catholic checkpoint. | Reported, not re-checked here. |
| Ansari | A hosted MCP server exists at `https://mcp.ansari.chat/mcp`. It needs no key. On 2026-11-20 it answered `initialize` (protocol version `2024-11-05`) and listed one tool, `answer_islamic_question`, which takes a `question` string. Its repository was last pushed in September 2025 and has no licence file. The separate Ansari skill (MIT, version 3.4.1, August 2026) calls a different HTTP endpoint with `curl`, so it needs a shell. | Checked by calling the server. |
| Principled pluralism | Michael Graham, The Gospel Coalition, 21 May 2026. For basic, high-consensus questions the answer opens by saying it comes from the tradition's perspective, gives the body to that tradition alone, and closes by offering other or skeptical perspectives. Lower-consensus questions get a summary of each view within the tradition. Published as prose with one worked example. No prompt, skill or licence statement. Silent on comparative questions and on questions that name no tradition. | Checked. Matches the issue. |

The limitations that motivate the work:

- A user who pastes a values prompt into an assistant gets no sources, no statement of who
  vouches for the text, and no protection against the prompt fading.
- A community that wants its values available in several assistants has to rebuild them for
  each one.
- A host developer has no agreed text to put around third-party values content, so each one
  would write its own, and the same package would behave differently everywhere.
- A public collection of value systems (issue #3) has no rule for deciding whether a submission
  is well formed, and no agreed fields to list and filter by.

## Desired State

A community writes one `VALUES.md` file and, if it wants, a folder around it. Any host that
follows the standard installs it the same way: the same prompt goes into the conversation, the
same reminder keeps it in force, the same tools become available, and the user can always see
what is installed and who vouches for it. A collection can check a submitted package against one
stated rule, list it from its own metadata, and offer it to Claude Code through a marketplace
file without the author doing anything further.

The rest of this section states what the standard says. These are the decisions the plan and
implementation follow. The reasoning and the alternatives are under Solution Approaches.

### 1. Package shape

A package is one of two things:

- **A single file** named exactly `VALUES.md`. This is a complete value system on its own.
- **A folder** with `VALUES.md` at its root and any of these beside it:

| Entry | Purpose | Format |
|---|---|---|
| `VALUES.md` | The value system: metadata and the always-on prompt. Required. | Defined by this standard. |
| `.mcp.json` | Tools and sources. | A JSON object with an `mcpServers` key, as MCP clients already use. See part 7. |
| `skills/` | Depth that loads on demand. One folder per skill. | Agent Skills, unmodified. |
| `references/` | Bundled texts the model can read on demand. | Any text files. |

The standard defines nothing else in the folder. A host ignores every other entry. Files such
as `.claude-plugin/plugin.json` or `hooks/` may be present for one product's benefit, and other
hosts ignore them. A folder package contains no symbolic links, and a host reads nothing
outside the folder on a package's behalf.

Installing a package runs nothing. The only thing in a package a host may ever execute is a
local MCP server command, and only under the consent rule in part 7.

### 2. `VALUES.md` frontmatter

YAML frontmatter followed by a Markdown body. Multiword keys use hyphens, as Agent Skills and
Claude Code do.

| Field | Required | Type and limits | Purpose |
|---|---|---|---|
| `name` | Yes | 1 to 64 characters. Lowercase letters `a` to `z`, digits and hyphens. No leading, trailing or doubled hyphen. | Identifier. Unique within a collection. Appears in the injected prompt. |
| `description` | Yes | 1 to 1,024 characters. | What the value system is and who it is for. Shown to the user at install and on a listing. |
| `steward` | Yes | Object. `name`: 1 to 100 characters on one line, without `<`, `>` or `"`. `claim`: one of `individual`, `organization`, `official`. `url`: an `https` URL of at most 500 characters, required unless `claim` is `individual`. | Who vouches for the package and what kind of authority they claim. See part 9. The name appears in the injected prompt. |
| `version` | Recommended | A version string as Semantic Versioning 2.0.0 defines it. | Version of the package. |
| `spec-version` | No | Two numbers joined by a dot, as a string. Default `"0.1"`. | Version of this standard the file targets. |
| `license` | No | 1 to 100 characters. An SPDX identifier where one exists. | Licence of the package's content. |
| `authors` | No | List of 1 to 20 strings, each 1 to 100 characters. | Who wrote the text, when different from the steward. |
| `tradition` | No | List of 1 to 4 strings, each 1 to 64 characters, broadest first, for example `[Islam, Sunni]`. | The tradition, school or community the value system belongs to, in its adherents' own terms. A listing groups and filters by it, comparing without regard to case. Any controlled vocabulary belongs to the collection. |
| `languages` | No | List of 1 to 20 BCP 47 language tags. | The languages the package is written in and meant to answer in. |
| `tags` | No | List of 1 to 20 strings in the same form as `name`. | Free keywords for search. |
| `persistence` | No | Object holding `reinject`, an object. `reinject.every-tokens`: integer from 1,000 to 1,000,000, default 5,000. `reinject.section`: 1 to 100 characters on one line, default `Core`. | Tunes reinjection. See part 5. |
| `models` | No | List of 1 to 20 objects. See part 6. | Declares fine-tuned models. |
| `metadata` | No | Object with any JSON values. | Extension space. The standard gives it no meaning. |

Unknown keys:

- At the top level, an unknown key is allowed and ignored. The schema permits it. This is what
  lets a later version add a field without breaking a v0.1 host.
- Inside `steward`, `persistence`, `persistence.reinject` and each `models` entry, an unknown
  key makes the file invalid. A misspelled `claim` or `access` must not pass silently.

A collection may require fields that are optional here, such as `version` and `license`. It
adds fields of its own only under `metadata`.

### 3. Body, prompt and core

The always-on prompt is the entire Markdown body. The core is the short part of it that is
reinjected. To make two independent readers get the same text, the standard fixes how the file
is read:

1. **Encoding.** The file is UTF-8. A leading byte-order mark is dropped. Every CRLF or lone CR
   is turned into LF before anything else is done.
2. **Frontmatter.** The first line is exactly `---`. The frontmatter runs to the next line that
   is exactly `---`. It is at most 8,000 characters. It is parsed as YAML 1.2 with the core
   schema, and it must be a mapping with no duplicate keys, no anchors and no aliases.
3. **Body.** Everything after the closing `---` line, with whitespace trimmed from both ends.
4. **Characters** means Unicode code points, counted after steps 1 to 3. No Unicode
   normalization is applied.
5. **Headings.** Only ATX headings count: a line that starts with one or two `#` characters and
   a space. Lines inside a fenced code block (opened by three or more backticks or tildes) are
   never headings. Setext headings (a line underlined with `---` or `===`) are not recognised.
6. **Heading text** is the rest of the line after the `#` characters, with any closing run of
   `#` characters removed and whitespace trimmed. Inline formatting is not stripped, so
   `## **Core**` has the text `**Core**`.
7. **The core section** is the second-level heading whose text equals
   `persistence.reinject.section` (default `Core`), compared without regard to case. **The
   core** is the text after that heading line, up to the next first- or second-level heading
   or the end of the body, with whitespace trimmed from both ends. The heading line itself is
   not part of the core.
8. **No core section.** If no heading matches and the body is 1,500 characters or fewer, the
   whole body is the core. If no heading matches and the body is longer, the file is invalid.
   If a heading matches, that section is the core, whatever the body's length. Two matching
   headings make the file invalid.

Limits: the body is at most 7,500 characters and is not empty. The core is at most 1,500
characters and is not empty.

Reserved text: the body must not contain a tag that belongs to the normative texts in part 4,
whether opening or closing. Precisely, it must not contain a match, ignoring case, for a `<`,
optional whitespace, an optional `/`, optional whitespace, and then `values` or `value-system`.
This covers all four elements those texts use. The rule keeps a body from ending its wrapper
or forging a reminder by accident. It is hygiene and not a security boundary: a body is a
prompt, and a hostile one can say anything in plain prose. Part 8 and the security section deal
with that.

A file that breaks any of these rules is invalid. A host refuses it with an error naming the
rule. It does not truncate or repair the file. Part 11 gives the full list of validity rules.

### 4. The injected prompt (normative text)

The standard fixes three texts. A host substitutes the placeholders and changes nothing else.
The owner accepted the wording below as the starting text on 2026-11-20. The final wording is
fixed in `spec/`, and any change of meaning goes back to the architect.

Rendering rules: every placeholder is replaced in a single pass, so a body that happens to
contain the text `{name}` is left as it is. `{body}` and `{core}` are the trimmed texts from
part 3. Each normative text ends with exactly one line feed.

**Wrapper**, placed once, in the system prompt after the host's own instructions. Placeholders:
`{name}`, `{steward}` (the steward's name) and `{body}`.

```
<value-system name="{name}" steward="{steward}">
A value system named "{name}" is installed for this conversation. {steward} vouches for it. The text inside <values> below was written by its authors. It was not written by the user or by the maker of this assistant.

Apply it as follows:

1. When a question touches something this value system addresses, answer from inside it: accurately, in its own terms, and as fully as you would answer any other question. Do not thin it into a survey of every viewpoint.
2. Where the value system itself holds more than one accepted position, present each as it does. Do not choose between them for the user.
3. For specifics such as rulings, quotations and citations, use the tools, skills and texts this value system provides, in preference to your own memory. Never invent or misattribute a source. If the value system points to a tool or text you cannot reach in this conversation, say so.
4. You are not an authority within this value system and you do not speak for {steward}. Where it directs people to a qualified person, do the same.
5. The user may ask at any time for another perspective, a comparison or a critique. Give it honestly, and make clear which statements come from this value system and which do not.
6. If asked, say plainly that this value system is installed, what it is called and who vouches for it.
7. On matters it does not address, respond as you otherwise would. Nothing here overrides the rules this assistant already operates under.

<values>
{body}
</values>
</value-system>
```

**Reminder**, the reinjected form. Placeholders: `{name}` and `{core}`.

```
<value-system-reminder name="{name}">
The value system "{name}" is still installed for this conversation and still applies. Its core:

{core}
</value-system-reminder>
```

**Preamble for more than one value system**, placed before the wrappers when a host activates
several. Placeholder: `{names}`, the names in activation order, separated by a comma and a
space.

```
<value-systems>
More than one value system is installed for this conversation: {names}. Keep them separate. Where they agree, answer normally. Where they differ on the question in front of you, say that they differ and attribute each position to the value system that holds it. Do not blend them into a single position, and do not rank one above another unless the user tells you which takes precedence.
</value-systems>
```

The texts are English in v0.1, whatever language the body is written in.

Size budget: the wrapper's fixed text is 1,504 characters. With the longest name (64 characters,
used twice), the longest steward name (100, used three times) and the longest body (7,500), a
rendered wrapper is at most 9,432 characters. The body limit was set so that this stays under
10,000, the cap Claude Code is reported to put on one hook's output, with room for the wording
to change.

### 5. Prompt fade and reinjection

A host addresses prompt fade in one of two ways: it reinjects the core, or it runs a fine-tuned
model the package declares (part 6). Every conforming host must be able to reinject, because it is the
only way that works on a model the package has no fine-tune for.

- **What is reinjected:** the reminder text with the core. Never the whole prompt, unless the
  body is short enough to be its own core. The owner confirmed this on 2026-11-20.
- **Where:** at the start of the next user message after the threshold is crossed, before the
  user's own text and separate from it: a separate content block where the API has them,
  otherwise the reminder, a blank line, and then the user's text. A host whose model accepts a
  system message mid-conversation may use one instead. A host may also place a reminder at a
  tool-result boundary during a long run with no user message. A reminder never goes inside an
  assistant turn.
- **How "every N tokens" is counted:** the host counts every token added to the conversation,
  from the user, the model and tools, since that value system's text was last placed in
  context. The count starts at zero when the wrapper is injected and resets after each
  reminder. The host uses the model's tokenizer when it has one and otherwise estimates one
  token per four characters. A value system gets at most one reminder at a boundary, however
  large its count.
- A host may drop older reminders from context and keep the most recent.
- A package can change the interval and the section name. It cannot turn reinjection off.

### 6. Fine-tuned models

A `models` entry has four required fields:

- `provider`: the service that serves the weights, in the same form as `name`, for example
  `tinker`.
- `base`: the base model the fine-tune was trained from, exactly as the provider names it, 1 to
  200 characters. The same weights saved for two context windows are two entries with two
  `base` values.
- `adapter`: the provider's own reference to the fine-tuned weights, 1 to 500 characters, for
  example a Tinker `tinker://<run_id>/sampler_weights/<name>` path.
- `access`: `public` if anyone with access to the provider can load the weights, `restricted`
  if only those the publisher has authorised can. A package may declare a restricted model.
  Saying so lets a host and a listing show the truth, which is that most people cannot use it.

Four are optional:

- `prompt`: how the model relates to the package's prompt. One of `required`, `optional` or
  `omit`. Default `required`. See below.
- `context-window`: a whole number of tokens from 1 to 100,000,000.
- `description`: up to 500 characters saying what the model was trained to do and on what.
- `trained-on`: the package version it was trained to embody.

**Matching.** An entry matches when the host is using that `provider` and the model it would
otherwise run is named by exactly the `base` string. There is no nearest-match and no
conversion. When nothing matches, the entries are ignored and the host reinjects.

**With or without the prompt.** A fine-tuned model can run with the package's prompt still
injected, or stand on its own without it. Which of these a model supports is a fact about how
it was trained and tested, so the package declares it, in `prompt`:

| `prompt` | The package is saying | What a host may do |
|---|---|---|
| `required` | This model is meant to run with the wrapper and body in context. | Run it with the prompt. |
| `optional` | This model works with the prompt and also on its own. | Run it either way. With the prompt unless the user or operator chooses otherwise. |
| `omit` | This model is meant to stand on its own. Putting the prompt on top of it is untested or unwanted. | Run it without the prompt. |

That gives a package three ways to be active, and a host must offer the first:

| Mode | Model | Wrapper and body | Reinjection |
|---|---|---|---|
| A | The host's own | Injected | Yes |
| B | A declared model | Injected | The host may skip it |
| C | A declared model whose `prompt` is `optional` or `omit` | Not injected | None |

**Who chooses.** The package says which modes a model supports. The user or operator chooses
whether to use a declared model at all, and, where `prompt` is `optional`, whether to run it
with the prompt. The host does neither on its own: it never switches models automatically and
never drops the prompt unasked. A host is never required to offer modes B or C.

**What the user is shown holds in every mode.** The host shows the name, the steward, the kind
of claim and where the package came from, at install and for as long as the value system is
active (part 9). In modes B and C it also shows that a fine-tuned model is in use and names it.
In mode C the model has nothing in context that tells it what is installed, so the wrapper's
rule that the model says so when asked cannot be relied on. The host's own display carries
that duty, and the host shows that the prompt is not injected.

**What mode C gives up.** Without the wrapper and body, none of the wrapper's rules are in
context, nor are any instructions the body gives about tools. How the model behaves rests on
its weights, which neither the host nor the user can read. A host says this when the user
chooses mode C. Tools from `.mcp.json` stay connected in every mode.

Other rules:

- When a chosen model fails to load, for example because it is restricted, the host tells the
  user and goes back to mode A.
- Mode C is available only when that package is the only active value system. With several
  active, every package has its wrapper in context (part 10).

### 7. Tools, skills and conformance levels

A host claims one of three levels. Each includes the one before it.

| Level | The host does | Typical host |
|---|---|---|
| 1. Prompt | Reads `VALUES.md`, injects the wrapper, addresses prompt fade, discloses what is installed. | Any chat product. Enough for a single-file package. |
| 2. Tools | Also connects the remote MCP servers in `.mcp.json`. | A plain chat loop with an MCP client. |
| 3. Package | Also exposes `skills/` as Agent Skills and lets the model read `references/` on demand. May run local MCP servers. | A coding agent or desktop assistant. |

MCP is how a host with no skill or plugin loader uses declared tools. Consequences for authors:
anything essential goes in the body, any essential tool goes in `.mcp.json` as a remote server,
and `skills/` and `references/` are for depth a lower-level host can do without.

**The shape of `.mcp.json`.** A JSON object with an `mcpServers` object. Other top-level keys
are ignored. Each key of `mcpServers` is a server name of 1 to 64 letters, digits, hyphens and
underscores. Each value is an object that is exactly one of:

- **Remote:** has `url`, a string beginning `https://`. May have `type`, either `http` or
  `sse`. An `http://` address is invalid, loopback included.
- **Local:** has `command`, a non-empty string. May have `args`, a list of strings, and `env`,
  an object whose values are strings.

An object with both `url` and `command`, or with neither, is invalid. `headers` is not allowed
in v0.1, because the only use for it in a published package is a credential. A server that
needs a credential gets it from the host, through MCP's own authorisation or the host's
settings. Any other key is ignored.

**Consent and trust.** Installing a package does not authorise what it declares.

- A host must have the user's or operator's consent, given for that package and that server,
  before it first connects to a remote server, and it shows the address when it asks. A user's
  questions go to that address.
- A host must not start a local server without the same consent, shown with the full command.
  A host may refuse all local servers, and a collection may refuse to list packages that have
  them.
- What comes back from a tool, and what is in a skill or a reference text, is untrusted
  content like any other tool output. It does not gain the standing of the wrapper or of the
  host's own instructions.

### 8. Discovery and installation

- The file name is exactly `VALUES.md`, in upper case, matched case-sensitively.
- There is no ambient discovery. A value system becomes active only when a user or operator
  explicitly installs it. A host that finds a `VALUES.md` in a working directory may offer to
  install it and must not activate it unprompted. This is deliberate: cloning a repository must
  not change an assistant's values.
- A folder is a package if and only if `VALUES.md` is at its root.
- Where a host keeps installed packages is its own business. The suggested shared location for
  file-based hosts is `~/.agents/values/<name>/`.
- Before activating, a host shows the user the name, description, steward and kind of claim,
  version, where the package came from, and the tools and models it declares.
- The specification text has a security section. It says, in one place: the standard is neutral
  on content; a body is third-party prompt text and can say anything; the wrapper cannot
  override the host's rules; installation is explicit; declared tools and models need their own
  consent; and a steward's claim is unverified.

### 9. Provenance

`steward` says who vouches for the package, and `steward.claim` says what kind of authority
that is:

| `claim` | Meaning |
|---|---|
| `individual` | A person offering their own statement of the value system. They speak for nobody else. |
| `organization` | An organization that stands behind the package as its own work. It does not claim to be the authority over the value system. |
| `official` | The steward says it is the body with authority over this value system, or is authorised by that body, and that this package is its official statement. |

Both are claims made by the package. The standard cannot verify them in v0.1. For
`organization` and `official`, `steward.url` is required, so that there is somewhere to check
the claim. What evidence a claim needs before a package is listed is for the collection that
lists it to decide (issue #3). What a host must do is make the claim and its origin visible:
show the steward, the kind of claim and the source at install, keep them available afterwards,
and never tell the model to conceal the installed value system. This holds in every mode of
part 6, including a fine-tuned model running without the prompt, where the host's display is
the only thing that tells the user what is installed. When the wrapper is in context, it makes
the model state the name and steward when asked. `authors` records who wrote the text when that differs
from who vouches for it. Verifying a steward mechanically, for example through a well-known URL
on the steward's domain or a signature, is left to a later version.

### 10. More than one value system

A host must support one active value system per conversation. It may let a user keep several
installed and choose between them. It may activate several at once, under these rules:

- The preamble in part 4 comes first, then one wrapper per package, in the order the user
  activated them.
- Two packages with the same `name` are never active together. The host refuses the second.
- Each package has its own token count and its own interval. At a boundary, every package
  whose count is due gets its reminder, in activation order.
- A fine-tuned model belongs to the package that declares it. Running it lets the host skip
  reinjection for that package only. The others are reinjected as usual. With several value
  systems active, every package's wrapper is in context, so a model cannot run without its
  prompt (part 6, mode C).
- Value systems are never merged. A package cannot declare precedence over another. Only the
  user can.

### 11. Validity

The standard gives one definition of a valid package, so that a host at install and a
collection's pull request check reach the same answer. Validity is decided from the package's
files alone. It needs no network call and no model.

A check has three possible outcomes:

- **Valid.**
- **Invalid**, with the identifiers of every rule that failed.
- **Unsupported version**, when `spec-version` is well formed but names a version the checker
  does not implement. This is not a rule failure. A package written for a later version is not
  malformed, and a v0.1 checker says only that it cannot judge it.

The rules apply in three scopes. A single file is checked against the file rules. A folder is
checked against the file and folder rules. A collection checks every package against all of
them.

| Rule | Scope | A package is valid only if |
|---|---|---|
| V1 | File | The file is named exactly `VALUES.md`, is UTF-8, and opens with frontmatter between two `---` lines, of at most 8,000 characters. |
| V2 | File | The frontmatter is a YAML 1.2 mapping with no duplicate keys, anchors or aliases. |
| V3 | File | The frontmatter validates against the schema. The schema carries every field rule in parts 2 and 6, including the `steward.url` condition and the rules on unknown keys. |
| V4 | File | The body is not empty and is at most 7,500 characters. |
| V5 | File | The core resolves to exactly one non-empty text of at most 1,500 characters, by the rules in part 3. |
| V6 | File | The body contains no reserved text, as part 3 defines it. |
| V7 | Folder | `.mcp.json`, if present, has the shape part 7 defines. |
| V8 | Folder | Every folder under `skills/` is a valid Agent Skill by that standard's own rules. |
| V9 | Folder | The folder contains no symbolic links. |
| V10 | Collection | The package's folder name equals its `name`, and no other package in the collection has that name. |

Things validity does not cover: whether a declared tool answers, whether a declared model
loads, whether a steward's claim is true, and whether the content is acceptable. Those need a
network, an account or a human, and a collection adds them as its own checks.

`spec/` carries a set of fixtures: valid packages, each with its expected rendered wrapper and
reminder, and at least one invalid package for each rule, labelled with the rule it breaks.
Fixtures are small and purpose-made. They are not copies of the packages in `values/`. V3 and V7 have several structural branches, and each
branch has a fixture. A checker written for a collection can be tested against them.

### 12. Collections and listings

A collection is a directory with one folder per package, each named for its package. The
standard defines this much so that a browser and a Claude Code marketplace can be generated
from the same folders. In this repository the collection is `values/`.

A listing page has what it needs from the frontmatter: `name`, `description`, the steward with
the kind of claim, `version`, `license`, `tradition`, `languages`, `tags`, the declared models
with their `access` and `prompt`, and from `.mcp.json` the tools a package connects to.

Every valid package maps to a Claude Code marketplace entry with no information invented:

| Marketplace entry | Taken from |
|---|---|
| `name` | `name`. Every valid package name is a valid entry name. |
| `source` | The path from the marketplace file's root to the package folder, beginning `./`. For a marketplace at the root of this repository, `./values/` followed by the folder name. |
| `description` | `description`, then a space, then the fixed sentence `Vouched for by {steward.name} ({steward.claim}).` |
| `version` | `version` |
| `author` | An object with `name` from `steward.name`, and `url` from `steward.url` when there is one. |
| `license` | `license` |
| `category` | The first item of `tradition` |
| `tags` | The items of `tradition`, then `languages`, then `tags`, in that order, with a repeated value kept once. |

When an optional field is absent from `VALUES.md`, its marketplace key is left out. It is never
written as null or as an empty value. The claim goes into the description because a
marketplace entry has no field for it, and Claude Code shows a user the description at install.

A package folder needs no `.claude-plugin/plugin.json` to be listed this way, because Claude
Code treats the marketplace entry as the manifest when the folder has none.

### 13. Example packages

Four examples. They are the first entries of the collection and live in `values/`, one folder
each, and nowhere else. `spec/` refers to them where they live and keeps no copy. The reference
implementation loads value systems from `values/`, so each example must be loadable from there
by the standard's rules alone, with nothing beside it in `spec/` needed to make it work.

- **`example-islam`**: a folder package. `.mcp.json` declares the Ansari MCP server. The body
  tells the model to use it for rulings, verses and hadith. The Ansari skill is not bundled, so
  that the model has one path to Ansari and the package works at Level 2. It declares the
  project's stage 2 fine-tuned checkpoint, so that the reference implementation can load a
  fine-tuned model from the package with no extension of its own. The entry, with two items
  still to be confirmed:

  ```yaml
  models:
    - provider: tinker
      base: # to be confirmed
      adapter: tinker://b1ced84d-f02a-5c16-8930-4f7f2e6636cd:train:0/sampler_weights/final
      access: # to be confirmed
  ```

  The owner's decision is that the checkpoint is published and declared `access: public`. That
  value is written only after the architect confirms publication, and nothing is pushed with
  it before then. Until `base` and `access` are filled in, the entry is incomplete and the
  example does not pass V3.
- **`example-roman-catholic`**: a folder package built around bundled texts and a skill, so
  that between them the examples exercise every part of the layout. It declares no model,
  because none exists and a placeholder would be a false claim. It declares an MCP server only
  if research during planning finds one with clear standing. Its bundled texts are limited to
  ones whose public-domain status can be shown. The candidates are the Douay-Rheims Bible in
  the Challoner revision, the Baltimore Catechism, and the Apostles' and Nicene creeds in an
  English translation old enough to be out of copyright. Where the status of a text cannot be
  shown, the package cites and links it and does not reproduce it.
- **`example-principled-pluralism`**: a minimal package, `VALUES.md` alone. It is a value
  system about how to answer questions on religion, taken from Michael Graham's published
  essay: answer a basic, high-consensus question about a religion from that religion's own
  vantage point and say that you are doing so, offer other perspectives at the close, and
  where the tradition is itself divided, summarise each view. Everything that is this value
  system's own position is in the package's body. The package cites the essay as its source,
  as any package cites its sources.
- **`plain-speaking`**: the file shown at the top of this spec. A non-religious value system
  in a single file, and the smallest valid package.

The three examples that describe someone else's tradition or work name the values.md project
as steward with the claim `organization`, and each carries a notice that it is illustrative and
not endorsed: by any religious authority for the two faith examples, and by its author for the
principled pluralism example. The notice appears in the description, the body and the
package's README. Their own statements are kept to high-consensus basics.

No example is treated specially by the standard. The wrapper, the validity rules and the
specification text are the same for all four and mention none of them outside the places where
examples are listed.

### 14. Deliverables

Under `spec/`:

1. The specification text, in RFC 2119 language, covering parts 1 to 12 and including the
   security section described in part 8.
2. The rationale document.
3. A JSON Schema (draft 2020-12) for the frontmatter.
4. The three normative prompt texts, each available as a standalone file a host can copy.
5. The compatibility note.
6. The validity fixtures described in part 11, with their expected renderings.
7. A checker, in its own directory, that applies the validity rules and checks the renderings.
   See part 16.

Under `values/`:

8. The four example packages of part 13, one folder each.

### 15. Compatibility note: what it must say

- **Claude Code.** Adding `.claude-plugin/plugin.json` makes a package folder load as a plugin.
  Claude Code then provides the package's skills and MCP servers. It does not read `VALUES.md`,
  so it does not inject the prompt or reinject the core. Getting those needs one adapter beyond
  the manifest: hooks that emit the wrapper at session start and the reminder as the transcript
  grows, or a forced output style that carries the wrapped prompt without reinjection. The note
  describes both. The hook adapter is code and belongs to issue #2.
- **The hook size cap.** A rendered wrapper is at most 9,432 characters (part 4), under the
  10,000-character cap on one hook's output. Each hook's output is measured separately, so with
  several value systems the adapter emits one hook output per package, and the preamble on its
  own. If a rendered text would still exceed the cap, the adapter refuses with an error. It
  does not truncate. The note re-checks the cap against the documentation before stating it.
- **A Claude Code marketplace.** The mapping in part 12, with a worked `marketplace.json` for
  the examples. The note says plainly that Claude Code's install screen shows the steward and
  the kind of claim only through the description, and that this is weaker than what part 9
  asks of a conforming host. It also records that a marketplace entry can declare hooks
  inline, which gives a collection one place to attach the prompt adapter for every package it
  lists.
- **A host that only understands skills** gets the skills in `skills/`, each a valid Agent
  Skill, and nothing always-on.
- **A host that only understands AGENTS.md** gets nothing automatically. A user can paste the
  body in by hand and gets the prompt once, with no wrapper, reminder or tools.

### 16. How this project is verified without a host

This project ships a standard and no host, so its checks are of two kinds.

- **Checked here.** Whether a fixture is valid and renders to its expected wrapper and
  reminder, whether every package in `values/` is valid where it lives, and whether the field
  table, the schema and the quoted texts agree. A checker in its own directory under `spec/`
  applies the validity and rendering rules mechanically, so that anyone can re-run the checks.
  It is the standard testing itself. It is not a loader and it talks to no model. Issue #3's
  check on a submitted package uses it.
- **Defined here, exercised by issue #2.** What a host does at run time: when it reinjects,
  what it does with a declared model, how it handles several value systems, what it asks
  consent for. The specification states each as a rule and shows it in a worked example.
  Running them needs a host, which is issue #2.

Some checks need outside tools: `claude plugin validate` and a Claude Code install (present
where this was written, version 2.1.329), `skills-ref validate` (to be installed from the
Agent Skills repository), and a network call to the Ansari server. If one of them cannot be
run, the criterion that depends on it is reported as not verified in the review and to the
architect. It is never ticked on trust.

### 17. Where the issue's eight questions are answered

| The issue asks | Answered in |
|---|---|
| 1. How a host with no skill or plugin loader uses declared tools | Part 7 |
| 2. What is reinjected, where, and how "every N tokens" is counted | Parts 3 and 5 |
| 3. How model declarations work across providers, and what a host does on a base model with no adapter | Part 6 |
| 4. Whether a fine-tuned model replaces reinjection, the prompt, both or neither | Part 6: it may always replace reinjection, and it replaces the prompt only where the package allows it and the user or operator chooses it |
| 5. Provenance: who authored a package, who vouches for it, and how a user can tell | Part 9 |
| 6. Whether more than one value system can be installed, and what happens when they conflict | Part 10 |
| 7. Where principled pluralism fits | Part 13: it is a value system like any other, and one of the examples |
| 8. The literal file name and discovery rules | Part 8 |

## Success Criteria

Criteria marked (tool) depend on an outside tool or service. Part 16 says what happens when one
cannot be run.

- [ ] `spec/` and `values/` contain the deliverables listed in Desired State part 14. Nothing
      else in the repository changes except Codev artifacts and, if the owner asks for one, a
      licence file at the root.
- [ ] The four example packages exist once, in `values/`. `spec/` holds no copy of any of them
      and refers to them by path.
- [ ] Applying the validity rules to `values/` as a collection, with no network access, finds
      every package valid.
- [ ] The specification text opens with the smallest valid `VALUES.md` in full, of no more
      than 12 lines, and with the two lists of what a first-time author and a Level 1 host can
      ignore. The file shown is identical to `values/plain-speaking/VALUES.md`.
- [ ] The specification text answers each of the issue's eight questions, listed in part 17, in
      an identifiable section, with the decisions recorded in parts 1 to 13.
- [ ] The specification text has a security section that makes the six points listed in part 8.
- [ ] Every frontmatter field in the specification text is in the schema with the same
      requiredness and limits, and the schema has no field the text lacks. The schema allows
      unknown keys at the top level and refuses them inside `steward`, `persistence`,
      `persistence.reinject` and a `models` entry.
- [ ] The schema is valid JSON Schema draft 2020-12.
- [ ] The specification lists validity rules V1 to V10 with stable identifiers, their scopes,
      and the three outcomes. `spec/` has at least one valid fixture and, for each rule, at
      least one invalid fixture labelled with the rule it breaks.
- [ ] The V3 fixtures cover at least: missing `name`, missing `steward`, a malformed `name`, a
      missing `steward.claim`, an `official` claim with no `url`, an unknown key inside
      `steward`, `every-tokens` below 1,000, and a `models` entry without `base` or without
      `access`. A fixture with an unknown top-level key is valid.
- [ ] The V5 fixtures cover at least: a long body with no core section, two matching headings,
      a core over the limit, a core heading inside a code fence, a Setext heading that does not
      count, and a CRLF file that is valid only after line endings are normalized.
- [ ] The V7 fixtures cover each branch: remote, local, both `url` and `command`, neither, an
      `http` address, `headers` present, and a bad server name.
- [ ] A fixture with `spec-version: "0.2"` gives the outcome "unsupported version" and not
      "invalid".
- [ ] Applying the rules to every fixture, with no network access, gives the labelled result.
- [ ] The wrapper, reminder and multiple-system preamble each exist as a standalone file, and
      every copy quoted elsewhere in `spec/` is identical to it.
- [ ] Each valid fixture has an expected rendered wrapper and reminder, and rendering the
      fixture by the specification's rules reproduces them exactly.
- [ ] Every example body is at most 7,500 characters and every example core is at most 1,500
      characters.
- [ ] A reader given only `spec/` and one package from `values/` can produce the rendered
      wrapper and reminder for it and state when the first reminder is due. Tested with an
      agent that has no other context.
- [ ] The specification includes a worked example of the exact messages a Level 2 host sends
      for a fixture that declares a remote tool, including the first reminder. It uses the
      default placement, at the start of the user message.
- [ ] (tool) `example-islam` declares the Ansari MCP server, and the review records the date on
      which that server answered `initialize` and listed its tool.
- [ ] Each of the three `example-` packages carries its "illustrative, not endorsed" notice in
      its description, body and README, and names the values.md project as steward.
- [ ] (tool) A temporary copy of each folder example, with only `.claude-plugin/plugin.json`
      added, passes
      `claude plugin validate` and loads in Claude Code with its skills and MCP servers
      available. The compatibility note states what Claude Code does not provide.
- [ ] (tool) A `marketplace.json` generated for `values/` by the mapping in part 12
      passes `claude plugin validate`, and an example installs from it in Claude Code with no
      `plugin.json` in its folder.
- [ ] (tool) Every skill inside an example passes `skills-ref validate`.
- [ ] The rationale covers the four options with their trade-offs, compares the format with
      AGENTS.md, Agent Skills, Claude Code plugins and Belief Protocol, and says why option 3.
      Every claim about another format links to its source and gives the date it was checked.
- [ ] No bundled reference text is under third-party copyright. Each one states its source and
      the basis for its public-domain or licence status.
- [ ] `example-principled-pluralism` is a valid package that cites the published essay as its
      source and carries the "illustrative, not endorsed by its author" notice. Outside that
      package and the places where the examples are listed, nothing in `spec/` mentions
      principled pluralism: not the wrapper, not the specification's rules, and not the
      rationale's account of where the wrapper's rules come from.
- [ ] The schema accepts `prompt` values `required`, `optional` and `omit` on a model entry and
      refuses any other. The specification's part on fine-tuned models states the three modes,
      who chooses, and what the user is shown in each.
- [ ] `example-islam` declares the stage 2 checkpoint with a confirmed `base` and `access`. No
      pushed commit says `access: public` before the architect has confirmed publication.
- [ ] The checker lives in its own directory under `spec/`, runs with one documented command,
      and needs no network access for the validity and rendering checks.
- [ ] `spec/` contains no loader or chatbot code.

## Constraints

Decided by the owner on 2026-11-20, copied from the issue. These are fixed.

1. **Scope:** value systems in general. Faith traditions are the first examples, not the limit.
2. **Shape ("option 3"):** a single `VALUES.md` file is the standard and is a complete, minimal
   value system on its own. The full package is a folder laid out like a Claude Code plugin,
   with `VALUES.md` as the one new file: `.mcp.json` for tools and sources, `skills/` for
   on-demand depth, `references/` for bundled texts. Adding `.claude-plugin/plugin.json` should
   make the same folder install in Claude Code unchanged.
3. **The standard includes the system prompt to be injected.** Architect's reading, to confirm
   at the spec gate: the standard fixes (a) which part of `VALUES.md` is the always-on prompt,
   (b) the exact wrapper text a host puts around it when a value system is installed, and
   (c) the exact form of the reinjected reminder.
4. **Fine-tuned models can be declared** by a package.
5. **Prompt fade** (a value-system prompt losing force as a conversation grows) must be
   addressable in two ways: (a) the host uses a declared fine-tuned model, or (b) the host
   reinjects the prompt, about every 5,000 tokens.
6. **Repo layout:** two parts, `spec/` (the standard declaration) and `reference/` (the
   reference implementation).
7. **Example value systems:** Islam, with **Ansari** as its tool, and Roman Catholic. Also look
   at The Gospel Coalition's "principled pluralism" (Michael Graham) and say where it fits.
8. **Document the choice of option 3**, including the alternatives and why they were not
   chosen.

Added by the architect on 2026-11-20, relaying the owner. Also fixed.

9. **The registry (issue #3).** Value systems will be collected in a separate registry
   repository with a browser, and people will submit their own. This project does not build the
   registry. The standard must give it what it needs: a unique package name, the fields a
   listing page shows (description, steward and what kind of claim of authority it makes,
   license, version, tags such as tradition and language), a rule for what is valid so that a
   pull request check can pass or fail a submission, and compatibility with a Claude Code
   `marketplace.json` entry.

10. **Lighter than Belief Protocol.** The owner's test for the format, relayed by the architect
    on 2026-11-20. The smallest valid package and what an author and a Level 1 host can ignore
    are shown at the top of this spec.

11. **The Claude Code prompt adapter belongs to issue #2.** Confirmed by the architect on
    2026-11-20. Adding `plugin.json` gives Claude Code a package's tools and skills and not its
    prompt. This project describes the adapter in the compatibility note and does not build it.

Decided by the owner on 2026-11-20 in answer to this spec's first open questions, copied from
his comment on the issue. Also fixed.

12. **The injected prompt.** The reading is right: the standard fixes which part of `VALUES.md`
    is the prompt, the wrapper text and the reminder text. The draft wrapper wording is
    accepted as the starting text.
13. **Principled pluralism is a value system like any other**, a minimal one. Add it as an
    example package alongside Islam, Roman Catholic and the plain-speaking example. Do not
    treat it specially anywhere:
    - Drop the separate "where principled pluralism fits" treatment and the plan to credit it
      as the source of the wrapper's structure.
    - The wrapper's rules stay only on their own merits, as what a host does for any installed
      value system. Anything that is specifically principled pluralism's position belongs in
      that package's body.
    - The package cites the published essay as its source, as any package cites its sources,
      and carries the same "illustrative, not endorsed by its author" notice as the other
      examples.
    - This replaces the earlier caution in this issue about publishing under that name.
14. **Validators.** Code that checks the fixtures and renderings may live in a directory under
    `spec/`.
15. **Reinjection.** Core only, as drafted.
16. **Models.** The fine-tuned checkpoints are to be made public. The Islam example declares
    them with `access: public`. The architect will confirm when publishing is done; do not mark
    them public in a pushed commit before that confirmation.
17. **Fine-tuned model and the prompt.** Make it flexible. The standard must allow a fine-tuned
    model to run with the prompt still injected and also to stand on its own without it, rather
    than fixing "replaces reinjection only". Design how that is declared and who chooses. What
    the user is shown about what is installed and who vouches for it must hold in both cases.
18. **Accepted without objection:** the 7,500-character body limit, hyphenated keys, the
    values.md project as steward of the examples with a "not endorsed" notice, a non-religious
    single-file example, CC BY 4.0 for the spec text, and local MCP servers allowed with
    consent.

Relayed by the architect on 2026-11-20:

19. The Islam example declares the stage 2 checkpoint, not stage 1.

Decided by the owner on 2026-11-20, copied from his later comment on the issue. Also fixed. It
replaces the "separate registry repository" of item 9.

20. **The collection lives in this repository, not a separate one.**
    - The repository has three parts: `spec/`, `reference/` and a collection directory. The
      architect's choice for its name is `values/` at the repository root.
    - The four example packages are the collection's first entries and live there once.
      `spec/` keeps the specification, schema, normative texts, fixtures, checker and
      compatibility note, and refers to the examples where they live, with no copies under
      `spec/`.
    - The reference implementation (#2) will load value systems from the collection directory,
      so the examples must be loadable from there by the standard's rules alone.
    - The browser, the submission check and the acceptance policy stay with #3.

Further constraints:

- Out of scope: the chatbot and any loader code (issue #2), the collection's browser, its
  submission check and its acceptance policy (issue #3), governance, funding, outreach to AI labs, and training a
  fine-tuned model.
- The collection's own questions stay with issue #3: what is accepted and who decides, what
  evidence a claim of authority needs, what review a declared tool gets, and name squatting.
  The standard supplies the fields and the validity rule those answers will use.
- Adoption cost decides reach. A Level 1 host should need no new dependency: read a file,
  substitute three placeholders, count tokens.
- A host other than Claude Code must not have to understand Claude Code's formats beyond
  `.mcp.json` and Agent Skills, which are already shared across products.
- Bundled texts must be redistributable. Most modern scripture translations and the Catechism
  of the Catholic Church are under copyright and cannot be bundled.
- The example packages speak about living religions without any religious authority's review.
  They must say so and must not overreach.

## Assumptions

- The architect's reading of decision 3 holds: the standard fixes the prompt part, the wrapper
  text and the reminder text. The whole design rests on this.
- Claude Code ignores unrecognised files at a plugin root, such as `VALUES.md` and
  `references/`. The documentation is silent, so this is tested during implementation. If it
  fails, decision 2's "install unchanged" is at risk and the architect is told at once.
- Claude Code accepts a plugin `.mcp.json` whose servers sit under an `mcpServers` key. The
  documentation describes the file as "an `mcpServers` map" without showing it. Tested during
  implementation.
- The Ansari MCP server stays available without a key. Its repository has been quiet since
  September 2025. Open question 6 asks the Ansari project to confirm its standing.
- Hosts can place text next to a user message that is distinguishable from what the user typed.
  This holds for the chat APIs in common use.
- Counting characters is an acceptable stand-in for counting tokens when setting limits and when
  a host has no tokenizer, because the reinjection interval is approximate by the owner's own
  wording ("about every 5,000 tokens").
- The 5,000-token interval is the owner's design parameter. The rationale cites evidence for
  prompt fade only where a source can be found and checked.
- Issue #2 builds the loader and the Claude Code hook adapter against this standard. Nothing
  here depends on that work being finished.
- A fine-tuned model still honours a system prompt. This is reported for Inkling 2 Small and
  the stage 1 checkpoint. How well a checkpoint behaves with a value-system prompt on top of it
  is untested, and issue #2 tests it. The result decides which `prompt` value the example
  declares.
- The outside tools the checks need can be run: Claude Code is installed here, `skills-ref`
  is not and has to be installed from the Agent Skills repository, and the Ansari server has
  to be reachable. Part 16 says what happens when one cannot be run.
- The Claude Code hook cap is 10,000 characters for each hook's output, measured separately.
  This was read through a summary and is re-checked before the compatibility note states it.
- Issue #3 writes its checker against the validity rules and fixtures delivered here. Where
  that checker's code lives is issue #3's question.

## Solution Approaches

### The shape of the standard

The owner chose option 3. The four options are recorded here because the rationale document
must set them out. They are not reopened.

#### Approach 1: A single file only

`VALUES.md` and nothing else, in the manner of AGENTS.md.

- For: the cheapest thing to adopt and the easiest to write.
- Against: no place for tools or bundled sources. A tradition's answers depend on citing its
  texts accurately, and a prompt alone leaves the model to recall them from memory.
- Risk: low to build, high that answers are unsourced.

#### Approach 2: A superset of an Agent Skill

A skill with extra frontmatter fields for values, models and persistence.

- For: reuses an existing loader and distribution path.
- Against: skills load on demand by description, and a value system has to be always on. The
  skill frontmatter is a closed list, so new fields would break validators and at least some
  upload paths. The extension map holds strings only, which cannot express a list of models.
- Risk: medium. The format would be at the mercy of another standard's validators.

#### Approach 3: A plugin-shaped folder with `VALUES.md` (chosen)

A single file that stands alone, and a folder around it that reuses `.mcp.json`, `skills/` and
`references/`.

- For: one new file. Every other part is a format hosts already read. The single file gives the
  low floor of approach 1, and the folder gives tools and depth. One added manifest file makes
  it a Claude Code plugin.
- Against: the layout follows one vendor's convention. A full implementation has three other
  formats to support, which the conformance levels soften.
- Risk: medium-low. The main one is that hosts stop at Level 1.

#### Approach 4: A new manifest from scratch

A purpose-built manifest that declares prompt, tools, skills and models in its own vocabulary.

- For: no inherited constraints, one coherent design.
- Against: every host needs a new loader for every part, and nothing existing can be reused.
  For a format whose purpose is reach, that cost defeats it.
- Risk: high that nobody adopts it.

### Decisions inside option 3

Each of these was open. The first alternative listed is the one adopted in Desired State.

**How the always-on prompt and the core are marked.**

- Adopted: the whole body is the prompt, and a named section is the core. An author writes
  ordinary Markdown, and a short file needs no marking at all. The section name is
  configurable, so a body written to Belief Protocol's structure can name its "Agent
  Orientations" section as the core, and a body in another language can use its own heading.
- Rejected: the core as a frontmatter string. It puts prose in YAML and takes it out of the
  document a person reads.
- Rejected: HTML comment markers around the core. They are invisible when rendered and easy to
  break.

**What is reinjected.**

- Adopted: a short core, capped at 1,500 characters. At the default interval that adds roughly
  6 to 8 percent to the conversation. This departs from the owner's wording in decision 5 for
  any body longer than the core limit. He was shown the costs below and confirmed core only.
- Rejected: the whole prompt. A 7,500-character body every 5,000 tokens would add about 38
  percent. The figures, at four characters to a token and the default interval:

  | What is reinjected | Tokens per reminder | Added to the conversation | Reminder tokens after 100,000 tokens of conversation, if every reminder is kept |
  |---|---|---|---|
  | A typical core of 1,000 characters | about 290 | about 6% | about 5,800 |
  | The largest core, 1,500 characters | about 415 | about 8% | about 8,300 |
  | A whole body of 4,000 characters | about 1,040 | about 21% | about 20,800 |
  | The largest body, 7,500 characters | about 1,915 | about 38% | about 38,300 |

- Rejected: a fixed one-line pointer with no content. It restates that a value system exists
  without restating what it says, which is the part that fades.

**Where the reminder goes and how tokens are counted.**

- Adopted: appended at the next user message, counting all tokens since the value system's
  text last appeared. Appending keeps the reminder next to the newest turn, where fade is
  worst, and leaves earlier context untouched, so prompt caches stay valid.
- Rejected: rewriting the system prompt periodically. Many APIs fix the system prompt for the
  conversation, and rewriting it invalidates caches.
- Rejected: counting user turns. Turn length varies too much to stand in for tokens.

**Whether a fine-tuned model replaces the prompt.**

- Adopted: the package declares it for each model, in a `prompt` field with three values, and
  the user or operator chooses within what is declared. Whether a model can stand alone
  depends on how it was trained and tested, and only the people who made it know that. The
  default is `required`, so that a model with no declaration keeps the prompt in context.
- Rejected: a fixed rule that a model replaces reinjection only. This was the first draft. The
  owner asked for a model to be able to stand on its own as well.
- Rejected: leaving it to the host. A host cannot tell from outside whether a set of weights
  was trained to carry the value system unaided.
- Rejected: a yes-or-no field. It cannot tell "works either way" from "must not have the
  prompt on top", and the second is a real case: a model trained with no system prompt, never
  tested with one.
- Rejected: a short fixed notice injected in place of the wrapper when the prompt is omitted,
  so the model could still say what is installed. It would mean the model never truly stands
  alone, which is what was asked for. The host's own display carries disclosure instead.

**How a host without a skill loader uses tools.**

- Adopted: MCP through `.mcp.json`, with conformance levels. MCP is the one tool mechanism
  shared by coding agents, desktop assistants and plain chat loops.
- Rejected: requiring every host to support skills. A plain chat loop has no file system or
  shell, and the Ansari skill itself needs `curl`.
- Rejected: declaring tools as inline function schemas in the frontmatter. That would be a
  second tool format, and it leaves nowhere to run the tool.

**How Ansari is carried in the Islam example.**

- Adopted: `.mcp.json` only. The server exists and answers. It works at Level 2 and above, and
  the model has one path to Ansari.
- Rejected: bundling the skill only. It fails on any host without a shell.
- Rejected: both. A Level 3 host would see two routes to the same service, and the bundled
  skill would be a copy that goes stale.

**Discovery.**

- Adopted: explicit installation only. A value system belongs to a person or an operator, not
  to a directory.
- Rejected: nearest-file discovery as in AGENTS.md. Any repository could then change an
  assistant's values by containing a file, which is a prompt-injection route.

**More than one value system.**

- Adopted: one is required, several are optional, and they are kept separate with conflicts
  named and attributed. A person can plausibly hold a faith and a professional code together.
- Rejected: exactly one, always. Simplest, and it rules out that case.
- Rejected: precedence declared by packages. Every package would rank itself first.

**Where principled pluralism fits.**

- Adopted, by the owner's decision: it is a value system like any other and one of the example
  packages. Its positions are in that package's body. The wrapper's rules stand on their own
  merits as what a host does for any installed value system.
- Rejected: treating it as the source of the wrapper's structure, or as guidance built into
  the wrapper. This was the first draft. It gave one value system a standing in the standard
  that no other has.
- Rejected: a default for hosts with nothing installed. A package format has no way to bind a
  host that has not installed a package.

**Required fields.**

- Adopted: `name`, `description` and `steward`. A value system that nobody vouches for is the
  one thing that should not install quietly, and the wrapper needs a steward to name.
- Rejected: `name` and `description` only, as in Agent Skills. The wrapper would then have two
  forms, one with a steward and one without.

**How a claim of authority is stated.**

- Adopted: a required `steward.claim` with three values, matching the three cases issue #3
  names. Requiring it means nobody acquires a claim by leaving a field out, and a listing never
  has to guess.
- Rejected: optional, defaulting to `individual`. It is the safe default, but a collection would
  still have to require the field, and two rules are worse than one.
- Rejected: a free-text statement. A listing cannot filter on it and a check cannot test it.

**How a listing finds tradition and language.**

- Adopted: separate `tradition`, `languages` and `tags` fields. A browser can build a filter
  from each, and `tradition` as a broad-to-narrow list handles several packages for one
  tradition: schools, denominations and so on.
- Rejected: one flat list of tags. A browser could not tell a tradition from a language from a
  keyword.
- Rejected: encoding them in the name, such as `islam-sunni-en`. Names would become the schema.

**What "valid" means.**

- Adopted: a numbered list of rules decided from the files alone, with fixtures. A host and a
  pull request check give the same answer, and the check can run without credentials.
- Rejected: the schema alone. It cannot see the body limits, the core section or the other
  files in the folder.
- Rejected: including reachability of tools and models. A check would then fail when a server
  is briefly down, and would need accounts to run.

**Whether a package may declare a model others cannot load.**

- Adopted: yes, with a required `access` field. A model can exist, and be useful to the people
  who trained it, before it is published.
- Rejected: public models only. It would force publishing a checkpoint before a package could
  mention it.
- Rejected: allowing it without saying so. A listing would then advertise something most
  visitors cannot use.

## Open Questions

The owner answered the first round of questions on 2026-11-20. His answers are in Constraints,
items 12 to 18, and the spec was revised to match. What remains:

**Critical** (the answer changes the deliverables)

1. **The design for running a fine-tuned model with or without the prompt.** The owner asked
   for both to be possible and for a design of how it is declared and who chooses. Part 6
   proposes a `prompt` field on each model entry (`required`, `optional` or `omit`, default
   `required`), with the package declaring what a model supports and the user or operator
   choosing within that. Is this the flexibility that was meant? Two points to confirm in
   particular: the default is `required`, so a model with no declaration always runs with the
   prompt, and running without the prompt is limited to the case where one value system is
   active.

**Important** (shapes the design, and has a recommended answer above)

2. `steward` as a required field and as an object, with a required `claim` of `individual`,
   `organization` or `official`, where the issue's sketch had a string.
3. Whether three kinds of claim are enough. The values come from issue #3. A fourth, for a
   package that states plainly it has no standing at all, would suit the examples better than
   `organization`, at the cost of a longer list.
4. Which `prompt` value `example-islam` declares for the checkpoints. They were trained with no
   system prompt, and running them with a value-system prompt on top is untested. Recommended:
   `optional` if issue #2's test of that combination goes well, and `omit` if it does not.
5. The `tradition` value for `example-islam`. The checkpoints are Sunni. Recommended:
   `[Islam, Sunni]` if that also describes Ansari's answers, and `[Islam]` otherwise.
6. Whether the Ansari MCP server is the endpoint the Ansari project wants a public example to
   point at, given that its repository has been quiet since September 2025.
7. The licence for everything that is not the specification text: the schema, the fixtures,
   the checker, and the example packages in `values/`. The text is CC BY 4.0 by the owner's decision.
   Recommended for the rest: MIT.
8. `metadata` holds any JSON value, where Agent Skills allows strings only. This is what lets
   a collection add structured fields of its own without a new version of the standard.

**Nice-to-know** (does not block v0.1)

9. Translations of the wrapper for value systems written in other languages.
10. A way to verify a steward: a well-known URL or a signature.
11. How a single package is distributed outside a collection: an archive, a URL.
12. Whether a Catholic source exists as an MCP server with clear standing, and which of the
    candidate texts in part 13 can be shown to be in the public domain. Both are researched
    during planning. The example cites and links whatever cannot be shown.

## Test Scenarios

### Checked in this project

Validity, each against a fixture and with no network access:

1. **Minimal file.** The `plain-speaking` file at the top of this spec is valid, and its core
   is the whole body.
2. **Long body without a core.** A body over 1,500 characters with no core section is invalid
   under V5.
3. **Custom core section.** `reinject.section` names a different heading. The core is the text
   under that heading, without the heading line, matched without regard to case.
4. **Short body with a core section.** The section is the core, not the whole body.
5. **Two matching headings.** Invalid under V5.
6. **Headings that do not count.** A `## Core` line inside a code fence and a Setext heading
   are not core headings.
7. **Line endings.** A CRLF file gives the same body, core and counts as its LF twin.
8. **Oversized body or core.** Invalid under V4 or V5. Nothing is truncated.
9. **Reserved text.** A body containing `</values>`, `</VALUES >` or an opening
   `<value-system-reminder` is invalid under V6.
10. **Unknown keys.** An unknown top-level key is valid. An unknown key inside `steward` is
    invalid under V3.
11. **Duplicate YAML key.** Invalid under V2.
12. **Later `spec-version`.** The outcome is "unsupported version".
13. **Interval below the minimum.** `every-tokens` of 500 is invalid under V3.
14. **Claim without a URL.** `claim: official` with no `steward.url` is invalid.
    `claim: individual` with no URL is valid.
15. **`.mcp.json` branches.** Remote and local servers are valid. Both keys, neither key, an
    `http` address, `headers` and a bad server name are each invalid under V7.
16. **Symbolic link.** A folder containing one is invalid under V9.
17. **Model entry.** `prompt: omit` is valid. `prompt: sometimes` and a model entry with an
    unknown key are invalid under V3.
18. **The four examples.** Each is valid where it lives in `values/`, including
    `example-principled-pluralism`, which is `VALUES.md` alone.
19. **Name and folder.** In a collection, a package whose folder name differs from its `name`
    is invalid under V10, and so is a second package with a name already taken.

Rendering and consistency:

20. **Rendering.** For each valid fixture, substituting the placeholders gives exactly the expected
    rendered wrapper and reminder. A body that contains the text `{name}` keeps it.
21. **Size budget.** A rendering with the longest name, steward name and body is 9,432
    characters.
22. **Consistency.** The field table and the schema agree, and quoted normative text is
    identical to the standalone files.
23. **Marketplace mapping.** The entry generated for each example matches the table in part 12,
    with absent optional fields left out.

With outside tools:

24. **Claude Code plugin.** Each folder example with `plugin.json` added validates and loads,
    with its skills and MCP servers available.
25. **Marketplace.** The generated `marketplace.json` validates, and an example with no
    `plugin.json` installs from it in Claude Code.
26. **Skills.** Every bundled skill passes the Agent Skills validator.
27. **Ansari.** The declared server answers `initialize` and lists its tool.

Non-functional:

28. **Implementable from the text.** An agent given only `spec/` and one package from `values/`
    produces the correct rendered prompt and reminder timing for it.
29. **Lightness.** The smallest valid file is no more than 12 lines, and the opening of the
    specification tells a first-time author what to ignore.
30. **Honesty of the examples.** Each `example-` package carries its notice in all three
    places, and no bundled text is under third-party copyright.

### Defined here, exercised by a host (issue #2)

The specification states each of these as a rule and shows it in the worked example. Running
them needs a host. They are conformance tests for hosts, and they are not pass or fail gates
for this project.

31. **Reminder timing.** The first reminder falls at the first user message after 5,000
    conversation tokens. A single large tool result produces one reminder, not several.
32. **Fine-tuned model with the prompt.** The host may skip reinjection for that package and
    still injects the wrapper. It shows that a fine-tuned model is in use.
33. **Different base model.** A host on a model that matches no entry ignores `models` and
    reinjects.
34. **Restricted model.** A host that cannot load a chosen `restricted` model tells the user
    and goes back to its own model with the prompt and reinjection.
35. **Level 2 host with a Level 3 package.** `skills/` and `references/` are ignored, the MCP
    tool works, and the prompt is complete without them.
36. **Two value systems.** The preamble is present, each package has its own wrapper and its
    own count, and each core is reinjected when due. Two packages with one name are refused.
37. **Consent.** The host asks before first connecting to a declared server and before
    starting a local command.
38. **Fine-tuned model without the prompt.** With `prompt: optional` and the user choosing to
    drop the prompt, or with `prompt: omit`, nothing from the package is injected. The host
    still shows the name, steward, kind of claim and source, and shows that the prompt is not
    injected.
39. **Prompt not droppable.** With `prompt: required`, or with the field absent, the host does
    not offer to run the model without the prompt.
40. **Two value systems and a standalone model.** With two packages active, the host does not
    run either one's model without its prompt.

## Risks and Mitigation

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| An example misstates a tradition and embarrasses the project. | Medium | High | Keep example statements to high-consensus basics, send specifics to tools and texts, mark the examples illustrative in three places, and recommend review by a knowledgeable person before publicity. |
| The wrapper wording proves weak or objectionable once tested on real models. | Medium | High | Treat the gate text as a draft, keep it short and rule-shaped, version it with the standard, and let issue #2 test it. A wording change is a version change. |
| Hosts stop at Level 1 and tool-backed packages lose their sources. | Medium | Medium | Wrapper rule 3 makes the model say when a tool is unreachable, and authors are told to keep essentials in the body. |
| Claude Code rejects or mishandles a folder with `VALUES.md` at its root. | Low | High | Test during implementation with `claude plugin validate` and a real load. Report to the architect at once if it fails. |
| A package carries harmful or manipulative values. | Medium | High | The standard is neutral on content and says so. The wrapper cannot override the host's rules, installation is explicit and shows the steward, the model discloses on request, and hosts keep their own policies. A security section says this. |
| A false steward claim. | Medium | Medium | The host shows where the package came from beside the claim. Verification is named as future work. |
| A declared model is used to swap in untrustworthy weights, or runs without the prompt and behaves in ways nobody can inspect. | Low | High | A host never switches models or drops the prompt on its own. The user or operator chooses, the host says what running without the prompt gives up, and the host's display of what is installed holds in every mode. |
| The Ansari MCP server changes or disappears. | Low | Medium | Record the check date. The example is marked illustrative, and the owner confirms the endpoint. |
| External formats change after the rationale is written. | High | Low | Every claim carries a link and a check date. |
| The 10,000-character hook cap is misread, since it was verified only from a summary. | Low | Low | The body limit stands on cost grounds without it. Re-check the page before the compatibility note cites the number. |
| The principled pluralism example misstates the essay it is drawn from. | Medium | Medium | The package cites the essay, keeps to what the essay says, carries the "not endorsed by its author" notice, and is treated like every other example. |
| The standard's fields turn out not to fit what the collection needs once issue #3 is specified. | Medium | Medium | Part 12 is written against issue #3's stated needs. A collection may require optional fields and extend under `metadata` without a new version of the standard. A real gap is a finding for v0.2. |
| A package states `official` falsely and a host shows it as fact. | Medium | High | The standard calls it a claim everywhere. A host shows it with the source and URL, and the collection decides what evidence it needs before listing. |
| A fine-tuned checkpoint behaves badly with a value-system prompt on top of it. | Medium | Medium | Untested today. Issue #2 tests it. The package then declares `prompt: omit` for that model, which the standard allows. |
| The Islam example says a checkpoint is public before it has been published. | Low | Medium | `access` is left unfilled until the architect confirms publication, and a success criterion checks that no pushed commit says otherwise. |

## References

Checked on 2026-11-20 unless noted.

- AGENTS.md: https://agents.md/
- Agent Skills specification: https://agentskills.io/specification
- Agent Skills client guide: https://agentskills.io/client-implementation/adding-skills-support
- Claude Code plugin manifest reference: https://code.claude.com/docs/en/plugins-reference.md
- Claude Code output styles: https://code.claude.com/docs/en/output-styles.md
- Claude Code hooks: https://code.claude.com/docs/en/hooks.md
- Belief Protocol: https://github.com/MikeyAnderson/belief-protocol
- Tinker checkpoints: https://tinker-docs.thinkingmachines.ai/tinker/howto/checkpoints/
- Tinker OpenAI-compatible inference: https://tinker-docs.thinkingmachines.ai/inference/openai/overview/
- Ansari MCP server: https://github.com/ansari-project/ansari-mcp (hosted at `https://mcp.ansari.chat/mcp`)
- Ansari skill: https://github.com/ansari-project/ansari-skill
- Michael Graham, "My Manifesto on AI and Religion", The Gospel Coalition, 21 May 2026:
  https://www.thegospelcoalition.org/article/my-manifesto-on-ai-and-religion/
- Model Context Protocol: https://modelcontextprotocol.io/
- RFC 2119 and RFC 8174, requirement-level keywords.
- Claude Code marketplaces: https://code.claude.com/docs/en/plugin-marketplaces.md and
  https://code.claude.com/docs/en/plugins/marketplace-reference.md
- BCP 47, language tags. SPDX licence list: https://spdx.org/licenses/
- Issue #1 (this work), issue #2 (reference implementation, with the checkpoint details in its
  first comment) and issue #3 (the values collection).
