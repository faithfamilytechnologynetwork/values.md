# Specification: values.md standard v0.1 — the VALUES.md package format

<!--
SPEC vs PLAN BOUNDARY:
This spec defines WHAT and WHY. The plan defines HOW and WHEN.
Keep implementation phases, file paths, code, and "first we will… then we will…"
out of the spec — those belong in codev/plans/<id>-*.md.
-->

Issue: #1. Protocol: SPIR. Everything this project delivers lives under `spec/`. The reference
implementation is issue #2 and is not part of this work.

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
- **Collection**: a directory that holds many packages, one folder each. The values registry
  planned in issue #3 is a collection.

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
| The owner's checkpoint | Reported by the taqwabench architect in a comment on issue #2, checked there against the Tinker API on 2026-11-20. A LoRA fine-tune of Inkling 2 Small: Islamic (Sunni), English only, trained to be good company for a practising Muslim and not to issue rulings, with no system prompt in training. It exists as two saves of the same weights, one for a 64k window and one for a 256k window on a different base model ID. It is private to the training account. Both the base model and the checkpoint honour a system prompt on the OpenAI-compatible endpoint. A system prompt carrying a value system on top of the fine-tune is untested. There is no Roman Catholic checkpoint. | Reported, not re-checked here. |
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
what is installed and who vouches for it. A registry can check a submitted package against one
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
| `.mcp.json` | Tools and sources. | A JSON object with an `mcpServers` key, as MCP clients already use. |
| `skills/` | Depth that loads on demand. One folder per skill. | Agent Skills, unmodified. |
| `references/` | Bundled texts the model can read on demand. | Any text files. |

The standard defines nothing else in the folder. A host ignores every other entry. A host never
executes anything in a package because the package was installed. Files such as
`.claude-plugin/plugin.json` or `hooks/` may be present for one product's benefit, and other
hosts ignore them.

### 2. `VALUES.md` frontmatter

YAML frontmatter followed by a Markdown body. Multiword keys use hyphens, as Agent Skills and
Claude Code do.

| Field | Required | Type and limits | Purpose |
|---|---|---|---|
| `name` | Yes | 1 to 64 characters. Lowercase letters, digits and hyphens. No leading, trailing or doubled hyphen. | Identifier. Unique within a collection. Appears in the injected prompt. |
| `description` | Yes | 1 to 1,024 characters. | What the value system is and who it is for. Shown to the user at install and on a listing. |
| `steward` | Yes | Object. `name`: 1 to 100 characters on one line, without `<`, `>` or `"`. `claim`: one of `individual`, `organization`, `official`. `url`: an `https` URL, required unless `claim` is `individual`. | Who vouches for the package and what kind of authority they claim. See part 9. The name appears in the injected prompt. |
| `version` | Recommended | Semantic version string. | Version of the package. |
| `spec-version` | No | String. Default `"0.1"`. | Version of this standard the file targets. |
| `license` | No | String. An SPDX identifier where one exists. | Licence of the package's content. |
| `authors` | No | List of strings. | Who wrote the text, when different from the steward. |
| `tradition` | No | List of 1 to 4 strings, broadest first, for example `[Islam, Sunni]`. | The tradition, school or community the value system belongs to, in its adherents' own terms. A listing groups and filters by it. |
| `languages` | No | List of BCP 47 language tags. | The languages the package is written in and meant to answer in. |
| `tags` | No | List of up to 20 strings in the same form as `name`. | Free keywords for search. |
| `persistence` | No | Object. `reinject.every-tokens`: integer, at least 1,000, default 5,000. `reinject.section`: string, default `Core`. | Tunes reinjection. See part 5. |
| `models` | No | List of objects. Each has `provider`, `base`, `adapter` and `access`, and optionally `context-window`, `description` and `trained-on`. | Declares fine-tuned models. See part 6. |
| `metadata` | No | Map from string to string. | Extension space. |

A host ignores keys it does not know. A host refuses a file whose `spec-version` it does not
implement. A collection may require fields that are optional here, such as `version` and
`license`. It adds fields of its own only under `metadata`.

### 3. Body, prompt and core

- **The always-on prompt is the entire Markdown body**, everything after the frontmatter. The
  host injects it verbatim. It does not summarise, shorten or reorder it.
- **The core** is the short part that is reinjected. It is the second-level section whose
  heading matches `persistence.reinject.section` (default `Core`), compared without regard to
  case, running to the next first- or second-level heading or the end of the file.
- **Limits**, counted in Unicode characters because tokenizers differ between hosts: the body
  is at most 8,000 characters and the core is at most 1,500 characters.
- If the body is 1,500 characters or fewer and has no core section, the whole body is the core.
  If the body is longer, it must contain a core section.
- The body must not contain a closing tag used by the normative texts in part 4, such as
  `</values>`, since that would end the wrapper early.

A file that breaks any of these rules is invalid. A host refuses it with an error naming the
rule. It does not truncate or repair the file. Part 11 gives the full list of validity rules.

### 4. The injected prompt (normative text)

The standard fixes three texts. A host substitutes the placeholders and changes nothing else.
The wording below is the draft for the spec gate. The final wording is fixed in `spec/`, and any
change of meaning after the gate goes back to the architect.

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
several. Placeholder: `{names}`, the names separated by commas.

```
<value-systems>
More than one value system is installed for this conversation: {names}. Keep them separate. Where they agree, answer normally. Where they differ on the question in front of you, say that they differ and attribute each position to the value system that holds it. Do not blend them into a single position, and do not rank one above another unless the user tells you which takes precedence.
</value-systems>
```

The texts are English in v0.1, whatever language the body is written in.

### 5. Prompt fade and reinjection

A host addresses prompt fade in one of two ways: it reinjects the core, or it runs a fine-tuned
model the package declares. Every conforming host must be able to reinject, because it is the
only way that works on a model the package has no fine-tune for.

- **What is reinjected:** the reminder text with the core. Never the whole prompt.
- **Where:** as a system message if the model's API allows one mid-conversation. Otherwise
  attached to the next user message, outside the user's own text. It is placed at the next user
  message after the threshold is crossed. A host may also place it at a tool-result boundary
  during a long run with no user message. It never goes inside an assistant turn.
- **How "every N tokens" is counted:** the host counts every token added to the conversation,
  from the user, the model and tools, since the value system's text was last placed in context.
  The count starts at zero when the wrapper is injected and resets after each reminder. The
  host uses the model's tokenizer when it has one and otherwise estimates one token per four
  characters. At most one reminder is placed at a boundary, however large the count.
- A host may drop older reminders from context and keep the most recent.
- A package can change the interval and the section name. It cannot turn reinjection off.

### 6. Fine-tuned models

A `models` entry has four required fields:

- `provider`: the service that serves the weights, for example `tinker`.
- `base`: the base model the fine-tune was trained from, as the provider names it. The same
  weights saved for two context windows are two entries with two `base` values.
- `adapter`: the provider's own reference to the fine-tuned weights, for example a Tinker
  `tinker://<run_id>/sampler_weights/<name>` path.
- `access`: `public` if any account at the provider can load the weights, `restricted` if only
  accounts the owner has authorised can. A package may declare a restricted model. Saying so
  lets a host and a listing show the truth, which is that most people cannot use it.

Three are optional: `context-window` in tokens, a `description` of up to 500 characters saying
what the model was trained to do and on what, and `trained-on`, the package version it was
trained to embody.

- A host is never required to use a declared model. It may use one only when it can reach that
  provider and the user or operator has explicitly chosen to. It never switches models
  automatically.
- When the host's model is not the `base` of any entry, the entries are ignored and the host
  reinjects. There is no nearest-match and no conversion.
- When a chosen model fails to load, for example because it is restricted, the host tells the
  user and reinjects on its own model.
- **A declared model replaces reinjection only.** A host running one may skip reinjection. It
  still injects the wrapper and body, because the fine-tune may be older than the package, the
  host cannot inspect what the weights do, and the wrapper's rules on disclosure and user
  choice must be in context either way. Nothing replaces the prompt.

### 7. Tools, skills and conformance levels

A host claims one of three levels. Each includes the one before it.

| Level | The host does | Typical host |
|---|---|---|
| 1. Prompt | Reads `VALUES.md`, injects the wrapper, addresses prompt fade, discloses what is installed. | Any chat product. Enough for a single-file package. |
| 2. Tools | Also connects the MCP servers in `.mcp.json`, at least the remote ones. | A plain chat loop with an MCP client. |
| 3. Package | Also exposes `skills/` as Agent Skills and lets the model read `references/` on demand. | A coding agent or desktop assistant. |

MCP is how a host with no skill or plugin loader uses declared tools. Consequences for authors:
anything essential goes in the body, any essential tool goes in `.mcp.json`, and `skills/` and
`references/` are for depth a lower-level host can do without. A package should prefer remote
MCP servers that need no user secret. A host may decline to run a local server command.

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
and never tell the model to conceal the installed value system. The wrapper makes the model
state the name and steward when asked. `authors` records who wrote the text when that differs
from who vouches for it. Verifying a steward mechanically, for example through a well-known URL
on the steward's domain or a signature, is left to a later version.

### 10. More than one value system

A host must support one active value system per conversation. It may let a user keep several
installed and choose between them. It may activate several at once, and then it must use the
preamble in part 4, wrap each package separately, and reinject each one's core. Value systems
are never merged. A package cannot declare precedence over another. Only the user can.

### 11. Validity

The standard gives one definition of a valid package, so that a host at install and a
collection's pull request check reach the same answer. Validity is decided from the package's
files alone. It needs no network call and no model. Each rule has a stable identifier, and a
checker reports the identifiers of the rules that failed.

| Rule | A package is valid only if |
|---|---|
| V1 | The file is named exactly `VALUES.md`, is UTF-8, and opens with YAML frontmatter between `---` lines. |
| V2 | The frontmatter validates against the schema. The schema carries every field rule in part 2, including the `steward.url` condition. |
| V3 | `spec-version`, if present, is `"0.1"`. |
| V4 | The body is not empty and is at most 8,000 characters. |
| V5 | The core resolves to exactly one non-empty text of at most 1,500 characters, by the rules in part 3. Two sections that both match the core heading make the file invalid. |
| V6 | The body contains no closing tag used by the normative texts. |
| V7 | In a folder package, `.mcp.json`, if present, is a JSON object with an `mcpServers` object. Each server is either remote, with an `https` URL, or local, with a command. |
| V8 | In a folder package, every folder under `skills/` is a valid Agent Skill by that standard's own rules. |
| V9 | In a collection, the package's folder name equals its `name`, and no other package in the collection has that name. |

Things validity does not cover: whether a declared tool answers, whether a declared model
loads, whether a steward's claim is true, and whether the content is acceptable. Those need a
network, an account or a human, and a collection adds them as its own checks.

`spec/` carries a set of fixtures: valid packages, and one invalid package for each rule,
labelled with the rule it breaks. A checker written for a collection can be tested against
them.

### 12. Collections and listings

A collection is a directory with one folder per package, each named for its package. The
standard defines this much so that a registry and a Claude Code marketplace can be generated
from the same folders.

A listing page has what it needs from the frontmatter: `name`, `description`, the steward with
the kind of claim, `version`, `license`, `tradition`, `languages`, `tags`, the declared models
with their `access`, and from `.mcp.json` the tools a package connects to.

Every valid package maps to a Claude Code marketplace entry with no information invented:

| Marketplace entry | Taken from |
|---|---|
| `name` | `name`. Every valid package name is a valid entry name. |
| `source` | `./` followed by the folder name. |
| `description` | `description` |
| `version` | `version` |
| `author` | `steward.name` and `steward.url` |
| `license` | `license` |
| `category` | The first item of `tradition` |
| `tags` | `tradition`, `languages` and `tags` together |

A package folder needs no `.claude-plugin/plugin.json` to be listed this way, because Claude
Code treats the marketplace entry as the manifest when the folder has none.

### 13. Example packages

- **`example-islam`**: a folder package. `.mcp.json` declares the Ansari MCP server. The body
  tells the model to use it for rulings, verses and hadith. The Ansari skill is not bundled, so
  that the model has one path to Ansari and the package works at Level 2. It declares the
  owner's checkpoint from issue #2 as two `restricted` model entries, one per context window,
  so that the reference implementation can load a fine-tuned model from the package with no
  private extension. This needs the owner's agreement to print the checkpoint paths. See Open
  Questions.
- **`example-roman-catholic`**: a folder package built around bundled texts and a skill, so
  that between them the two examples exercise every part of the layout. It declares an MCP
  server only if research during planning finds one with clear standing.
- **A minimal single-file example** of a non-religious value system, to show the smallest valid
  package and that the format is not limited to faith. This is an addition to the issue's
  deliverable list. See Open Questions.

Both tradition examples name the values.md project as steward with the claim `organization`,
carry an "illustrative, not endorsed by any religious authority" notice in the description, the
body and their README, and keep their own statements to high-consensus basics. The Roman
Catholic example declares no fine-tuned model, because none exists and a placeholder would be a
false claim. The examples are laid out as a collection, so they are also the seed content issue
#3 asks for.

### 14. Deliverables under `spec/`

1. The specification text, in RFC 2119 language, covering parts 1 to 12.
2. The rationale document.
3. A JSON Schema (draft 2020-12) for the frontmatter.
4. The three normative prompt texts, each available as a standalone file a host can copy.
5. The example packages, with the expected rendered wrapper and reminder for each.
6. The compatibility note.
7. The validity fixtures described in part 11.

### 15. Compatibility note: what it must say

- **Claude Code.** Adding `.claude-plugin/plugin.json` makes a package folder load as a plugin.
  Claude Code then provides the package's skills and MCP servers. It does not read `VALUES.md`,
  so it does not inject the prompt or reinject the core. Getting those needs one adapter beyond
  the manifest: hooks that emit the wrapper at session start and the reminder as the transcript
  grows, or a forced output style that carries the wrapped prompt without reinjection. The note
  describes both. The hook adapter is code and belongs to issue #2.
- **A Claude Code marketplace.** The mapping in part 12, with a worked `marketplace.json` for
  the examples. The note also records that a marketplace entry can declare hooks inline, which
  gives a registry one place to attach the prompt adapter for every package it lists.
- **A host that only understands skills** gets the skills in `skills/`, each a valid Agent
  Skill, and nothing always-on.
- **A host that only understands AGENTS.md** gets nothing automatically. A user can paste the
  body in by hand and gets the prompt once, with no wrapper, reminder or tools.

### 16. Where principled pluralism fits

It is guidance in the wrapper, not a package and not a default. Its two structural rules are in
the wrapper: answer from the tradition's own vantage point with the body given to that
tradition (rule 1), and present each view where the tradition is divided (rule 2). Its closing
offer of other perspectives becomes a standing right of the user (rule 5), since a user who
installed a value system has already chosen the perspective and does not need the offer
repeated on every answer. The rationale credits the article as the source of that structure.
The standard publishes nothing under the name: no package and no mode. A package by that name,
and its use as a host's default when nothing is installed, are recorded as future work that
needs Michael Graham's agreement. What a host does when nothing is installed is outside the
standard.

## Success Criteria

- [ ] `spec/` contains the seven deliverables listed in Desired State part 14, and nothing in
      the repository outside `spec/` changes except Codev artifacts.
- [ ] The specification text opens with the smallest valid `VALUES.md` in full, of no more
      than 12 lines, and with the two lists of what a first-time author and a Level 1 host can
      ignore. That file is one of the valid fixtures.
- [ ] The specification text answers each of the issue's eight questions in an identifiable
      section, with the decisions recorded in Desired State parts 1 to 12 and 16.
- [ ] Every frontmatter field in the specification text is in the schema with the same
      requiredness and limits, and the schema has no field the text lacks.
- [ ] The schema is valid JSON Schema draft 2020-12, and every example's frontmatter validates
      against it.
- [ ] The specification lists validity rules V1 to V9 with stable identifiers. `spec/` has at
      least one valid fixture and, for each rule, at least one invalid fixture labelled with the
      rule it breaks. The schema fixtures cover at least: missing `name`, missing `steward`, a
      malformed `name`, a missing `steward.claim`, an `official` claim with no `url`,
      `every-tokens` below 1,000, and a `models` entry without `base` or without `access`.
- [ ] Applying the rules to every fixture, with no network access, gives the labelled result.
- [ ] A `marketplace.json` generated from the examples by the mapping in part 12 passes
      `claude plugin validate`, and an example installs from it in Claude Code with no
      `plugin.json` in its folder.
- [ ] The wrapper, reminder and multiple-system preamble each exist as a standalone file, and
      every copy quoted elsewhere in `spec/` is identical to it.
- [ ] Every example body is at most 8,000 characters and every example core is at most 1,500
      characters.
- [ ] Each example has an expected rendered wrapper and reminder in `spec/`, and rendering the
      example by the specification's rules reproduces them exactly.
- [ ] A reader given only `spec/` can produce the rendered wrapper and reminder for an example
      and state when the first reminder is due. Tested with an agent that has no other context.
- [ ] The specification includes a worked example of the exact messages a Level 2 host sends
      for `example-islam`, including the first reminder.
- [ ] `example-islam` declares the Ansari MCP server, and the review records the date on which
      that server answered `initialize` and listed its tool.
- [ ] Each tradition example carries the illustrative notice in its description, body and
      README, names the values.md project as steward, and has a name beginning `example-`.
- [ ] Each example folder, with only `.claude-plugin/plugin.json` added, passes
      `claude plugin validate` and loads in Claude Code with its skills and MCP servers
      available. The compatibility note states what Claude Code does not provide.
- [ ] Every skill inside an example passes `skills-ref validate`.
- [ ] The rationale covers the four options with their trade-offs, compares the format with
      AGENTS.md, Agent Skills, Claude Code plugins and Belief Protocol, and says why option 3.
      Every claim about another format links to its source and gives the date it was checked.
- [ ] No bundled reference text is under third-party copyright. Each one states its source and
      its public-domain or licence status.
- [ ] No package, mode or file is published under the name "principled pluralism".
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

Further constraints:

- Out of scope: the chatbot and any loader code (issue #2), the registry, its browser and its
  submission check (issue #3), governance, funding, outreach to AI labs, and training a
  fine-tuned model.
- The registry's own questions stay with issue #3: what is accepted and who decides, what
  evidence a claim of authority needs, what review a declared tool gets, and name squatting.
  The standard supplies the fields and the validity rule those answers will use.
- Anything published under the name "principled pluralism" needs Michael Graham's agreement
  first.
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
  September 2025. The owner is close to the Ansari project and can confirm its standing.
- Hosts can place text next to a user message that is distinguishable from what the user typed.
  This holds for the chat APIs in common use.
- Counting characters is an acceptable stand-in for counting tokens when setting limits and when
  a host has no tokenizer, because the reinjection interval is approximate by the owner's own
  wording ("about every 5,000 tokens").
- The 5,000-token interval is the owner's design parameter. The rationale cites evidence for
  prompt fade only where a source can be found and checked.
- Issue #2 builds the loader and the Claude Code hook adapter against this standard. Nothing
  here depends on that work being finished.
- A fine-tuned model still honours a system prompt. This is confirmed for Inkling 2 Small and
  the owner's checkpoint. How well the checkpoint behaves with a value-system prompt on top of
  it is untested, and issue #2 tests it. The rule that a declared model never replaces the
  prompt depends on this.
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
  any body longer than the core limit. Open question 4 puts the choice to him with the costs.
- Rejected: the whole prompt. An 8,000-character body every 5,000 tokens would add about 40
  percent.
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

- Adopted: it replaces reinjection only. Reasons are in Desired State part 6.
- Rejected: replacing the prompt as well. The value system would then live in weights nobody
  can read, the user could not be told what is installed from anything in context, and a stale
  fine-tune would silently override a newer package.
- Rejected: replacing nothing. That would make the fine-tune pointless for prompt fade, against
  decision 5.

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

- Adopted: guidance in the wrapper. Reasons are in Desired State part 16.
- Rejected: a third example package. It would be published under the name and needs agreement
  first. It remains a good candidate once that agreement exists.
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
- Rejected: optional, defaulting to `individual`. It is the safe default, but a registry would
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

- Adopted: yes, with a required `access` field. The owner's checkpoint is private today, and
  the reference implementation needs to load it from a package.
- Rejected: public models only. It would force publishing a checkpoint before a package could
  mention it.
- Rejected: allowing it without saying so. A listing would then advertise something most
  visitors cannot use.

## Open Questions

**Critical** (the owner's answer at the spec gate changes the deliverables)

1. **Decision 3.** Is the reading correct that the standard fixes the prompt part, the exact
   wrapper and the exact reminder? Is the draft wording in Desired State part 4 acceptable as
   the starting text?
2. **Principled pluralism.** May the rationale cite the article by name and credit it as the
   source of the wrapper's structure, with no package or mode under that name? If any mention
   needs Michael Graham's agreement first, the rationale describes the structure without the
   name until that agreement exists.
3. **The Claude Code gap.** Adding `plugin.json` gives Claude Code the tools and skills and not
   the prompt. Is it acceptable that the prompt adapter (hooks) is delivered by issue #2 and
   only described here?

4. **Reinjecting a core, not the prompt.** The owner's decision 5 says the host "reinjects the
   prompt". This spec reinjects only the core, a section of at most 1,500 characters. For a
   package whose body is 1,500 characters or fewer, the core is the whole body, so the owner's
   words hold exactly. For a longer body they do not, and the owner should choose. Costs, at
   four characters to a token and the default interval of 5,000 tokens:

   | What is reinjected | Tokens per reminder | Added to the conversation | Reminder tokens after 100,000 tokens of conversation |
   |---|---|---|---|
   | A typical core of 1,000 characters | about 290 | about 6% | about 5,800 |
   | The largest core, 1,500 characters | about 415 | about 8% | about 8,300 |
   | A whole body of 4,000 characters | about 1,040 | about 21% | about 20,800 |
   | The largest body, 8,000 characters | about 2,040 | about 41% | about 40,800 |

   The last column assumes the host keeps every reminder in context. A host that keeps only
   the newest one holds a single reminder at a time, and pays the full figure once per
   interval on a provider that does not cache. The choices:

   - **(a) Core only**, as drafted. Recommended. The cost is bounded and small, and the author
     decides what must not fade.
   - **(b) The whole body, always**, as the owner's words say. Simplest to state, with no core
     section to define. To keep the cost tolerable the body limit would have to come down,
     probably to about 2,000 characters, which pushes more into skills and references.
   - **(c) The package chooses**: core by default, with a frontmatter switch to reinject the
     whole body. Flexible, at the cost of one more field and a cost the host does not control.

5. **The checkpoint in a public example.** May `example-islam` print the two `tinker://` paths
   from the comment on issue #2, marked `restricted`? If not, the example declares no model and
   the reference implementation needs its own package to show the fine-tuned path.

**Important** (shapes the design, and has a recommended answer above)

6. `steward` as a required field and as an object, with a required `claim` of `individual`,
   `organization` or `official`, where the issue's sketch had a string.
7. The limits: body at most 8,000 characters, core at most 1,500. The body limit keeps the
   wrapped prompt under Claude Code's 10,000-character hook cap and pushes depth into skills
   and references.
8. Hyphenated keys (`every-tokens`), where the issue's sketch had `every_tokens`.
9. Example names (`example-islam`, `example-roman-catholic`) and the values.md project as their
   steward, with the claim `organization`. The owner may prefer to arrange a knowledgeable
   reviewer for each before v0.1 is publicised.
10. The `tradition` value for `example-islam`. The checkpoint is Sunni. Recommended:
   `[Islam, Sunni]` if the owner confirms that also describes Ansari's answers, and `[Islam]`
   otherwise.
11. Whether to include the minimal non-religious single-file example, which the issue did not
    list.
12. The licence for `spec/`. Recommended: CC BY 4.0 for the text, and a permissive code licence
    for the schema and examples. The repository has no licence file yet. The registry's own
    licensing question (issue #3) will lean on this answer.
13. Whether the Ansari MCP server is the endpoint the Ansari project wants a public example to
    point at, given that its repository has been quiet since September 2025.
14. Whether three kinds of claim are enough. The values come from issue #3. A fourth, for a
    package that states plainly it has no standing at all, would suit the examples better than
    `organization`, at the cost of a longer list.

**Nice-to-know** (does not block v0.1)

15. Translations of the wrapper for value systems written in other languages.
16. A way to verify a steward: a well-known URL or a signature.
17. How a single package is distributed outside a collection: an archive, a URL.
18. Whether a Catholic source exists as an MCP server with clear standing. Researched during
    planning. The example is text-backed if none is found.

## Test Scenarios

Functional:

1. **Minimal file.** A `VALUES.md` with the three required fields and a short body with no core
   section validates, and its core is the whole body.
2. **Long body without a core.** A body over 1,500 characters with no core section is invalid.
3. **Custom core section.** `reinject.section` names a different heading, and the core is that
   section's content, matched without regard to case.
4. **Oversized body or core.** Each is invalid. Nothing is truncated.
5. **Wrapper break-out.** A body containing `</values>` is invalid.
6. **Unknown key.** A frontmatter key the standard does not define is ignored and the file
   still validates.
7. **Unknown `spec-version`.** The file is refused.
8. **Interval below the minimum.** `every-tokens` of 500 is invalid.
9. **Rendering.** For each example, substituting the placeholders gives exactly the expected
   rendered wrapper and reminder.
10. **Reminder timing.** In the worked example, the first reminder falls at the first user
    message after 5,000 conversation tokens. A single large tool result produces one reminder,
    not several.
11. **Fine-tuned model in use.** The host skips reinjection and still injects the wrapper.
12. **Different base model.** A host on a model that matches no entry ignores `models` and
    reinjects.
13. **Level 2 host with a Level 3 package.** `skills/` and `references/` are ignored, the MCP
    tool works, and the prompt is complete without them.
14. **Two value systems.** The preamble is present, each package has its own wrapper, and each
    core is reinjected.
15. **Claude Code.** Each example with `plugin.json` added validates and loads, with its skills
    and MCP servers available.
16. **Skills.** Every bundled skill passes the Agent Skills validator.
17. **Ansari.** The declared server answers `initialize` and lists its tool.
18. **Claim without a URL.** `claim: official` with no `steward.url` is invalid. `claim:
    individual` with no URL is valid.
19. **Each validity rule.** For each of V1 to V9, the fixture that breaks it is reported
    invalid with that rule's identifier, and with no network access.
20. **Duplicate core heading.** Two sections matching the core heading make the file invalid.
21. **Name and folder.** In a collection, a package whose folder name differs from its `name`
    is invalid, and so is a second package with a name already taken.
22. **Insecure tool URL.** A remote server in `.mcp.json` with an `http` URL is invalid.
23. **Restricted model.** A host that cannot load a chosen `restricted` model tells the user
    and reinjects.
24. **Marketplace.** The `marketplace.json` generated from the examples validates, and an
    example with no `plugin.json` installs from it in Claude Code.

Non-functional:

25. **Implementable from the text.** An agent given only `spec/` produces the correct rendered
    prompt and reminder timing for an example.
26. **Consistency.** The field table and the schema agree, and quoted normative text is
    identical to the standalone files.
27. **Honesty of the examples.** The illustrative notice appears in all three places, and no
    bundled text is under third-party copyright.

## Risks and Mitigation

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| An example misstates a tradition and embarrasses the project. | Medium | High | Keep example statements to high-consensus basics, send specifics to tools and texts, mark the examples illustrative in three places, and recommend review by a knowledgeable person before publicity. |
| The wrapper wording proves weak or objectionable once tested on real models. | Medium | High | Treat the gate text as a draft, keep it short and rule-shaped, version it with the standard, and let issue #2 test it. A wording change is a version change. |
| Hosts stop at Level 1 and tool-backed packages lose their sources. | Medium | Medium | Wrapper rule 3 makes the model say when a tool is unreachable, and authors are told to keep essentials in the body. |
| Claude Code rejects or mishandles a folder with `VALUES.md` at its root. | Low | High | Test during implementation with `claude plugin validate` and a real load. Report to the architect at once if it fails. |
| A package carries harmful or manipulative values. | Medium | High | The standard is neutral on content and says so. The wrapper cannot override the host's rules, installation is explicit and shows the steward, the model discloses on request, and hosts keep their own policies. A security section says this. |
| A false steward claim. | Medium | Medium | The host shows where the package came from beside the claim. Verification is named as future work. |
| A declared model is used to swap in untrustworthy weights. | Low | High | A host never switches automatically, and the prompt is still injected. |
| The Ansari MCP server changes or disappears. | Low | Medium | Record the check date. The example is marked illustrative, and the owner confirms the endpoint. |
| External formats change after the rationale is written. | High | Low | Every claim carries a link and a check date. |
| The 10,000-character hook cap is misread, since it was verified only from a summary. | Low | Low | The body limit stands on cost grounds without it. Re-check the page before the compatibility note cites the number. |
| Mentioning principled pluralism is taken as publishing under the name. | Low | Medium | Open question 2 puts the choice to the owner before anything is written. |
| The standard's fields turn out not to fit what the registry needs once issue #3 is specified. | Medium | Medium | Part 12 is written against issue #3's stated needs. A collection may require optional fields and extend under `metadata` without a new version of the standard. A real gap is a finding for v0.2. |
| A package states `official` falsely and a host shows it as fact. | Medium | High | The standard calls it a claim everywhere. A host shows it with the source and URL, and the registry decides what evidence it needs before listing. |
| The fine-tuned checkpoint behaves badly with a value-system prompt on top of it. | Medium | Medium | Untested today. Issue #2 tests it. If it fails, the finding comes back to the standard before v0.1 is called final. |
| Printing private checkpoint paths in a public example exposes something the owner did not intend. | Low | Medium | Open question 5. Nothing is printed until the owner agrees. This spec refers to the paths by pointing at the issue comment. |

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
  first comment) and issue #3 (the values registry).
