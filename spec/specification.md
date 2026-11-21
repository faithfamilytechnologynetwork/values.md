# The values.md standard, version 0.1

A `VALUES.md` file hands an AI assistant a **value system**: a body of values that a person or
a community wants the assistant to answer from, such as a faith tradition, a professional code
or a family's house rules. This document defines the file, the optional folder around it, the
exact text a host puts around it in a conversation, how that text is kept in force as the
conversation grows, and what makes a package valid.

This text is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The
schemas, fixtures, checker and examples that accompany it are under the MIT licence.

## The format at a glance

This is the smallest valid `VALUES.md`, in full:

<!-- values-md:smallest-file -->
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
and no required structure inside the body.

**A first-time author can ignore** everything else in this document:

- Every other frontmatter field. `version`, `spec-version`, `license`, `authors`, `tradition`,
  `languages`, `tags`, `persistence`, `models` and `metadata` are all optional.
- The core section. A body of 1,500 characters or fewer is its own core.
- The folder and everything in it: `.mcp.json`, `skills/` and `references/`.
- The wrapper and reminder texts. The host supplies them.
- Conformance levels, collections and marketplaces.

**A Level 1 host can ignore:**

- `.mcp.json`, `skills/` and `references/`. Those are Levels 2 and 3.
- `models`, apart from showing the user that the package declares them. Using a declared model
  is always optional.
- `tradition`, `languages`, `tags`, `license`, `authors` and `metadata`. They are for listings
  and display.
- Collections, marketplaces and activating more than one value system at a time.

What a Level 1 host does do: read one file, check it against validity rules V1 to V6, put the
body inside the wrapper text, count tokens, add the reminder when the count reaches the
interval, and show the user the name, the steward and the kind of claim.

## Conventions

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be read as RFC 2119 and RFC
8174 describe them, and only when they are in capitals.

Terms:

- **Value system**: a body of values that a person or community wants an AI model to answer
  from.
- **Package**: the files that carry one value system. Either a single `VALUES.md` file or a
  folder with `VALUES.md` at its root.
- **Host**: the application that runs a model and installs a package: a chat product, a coding
  agent, a plain chat loop.
- **Steward**: the person or body that vouches for a package being a faithful statement of its
  value system.
- **Prompt fade**: a value-system prompt losing force as a conversation grows.
- **Collection**: a directory that holds many packages, one folder each.
- **Operator**: whoever configures a host on behalf of its users, where that is not the user.

Four words are used with one fixed meaning everywhere in this document, so that two readers
written in different languages reach the same answer:

- **Character** means a Unicode code point. Lengths are counted in code points, after the file
  has been read by the rules of part 3. No Unicode normalization is applied.
- **Whitespace** means the space (U+0020), the tab (U+0009) and the line feed (U+000A), and no
  other character. A no-break space is not whitespace. **Trimming** removes whitespace from
  both ends of a text and nothing from inside it.
- **Without regard to case** means that the letters `A` to `Z` equal `a` to `z`. Every other
  character has to match exactly.
- **On one line** means the text holds no line feed and no carriage return.

"Part N" refers to the numbered sections below.

## 1. Package shape

A package is one of two things:

- **A single file** named exactly `VALUES.md`. This is a complete value system on its own.
- **A folder** with `VALUES.md` at its root and any of these beside it:

| Entry | Purpose | Format |
|---|---|---|
| `VALUES.md` | The value system: metadata and the always-on prompt. Required. | Defined by this standard. |
| `.mcp.json` | Tools and sources. | A JSON object with an `mcpServers` key, as MCP clients already use. See part 7. |
| `skills/` | Depth that loads on demand. One folder per skill. | [Agent Skills](https://agentskills.io/specification), unmodified. |
| `references/` | Bundled texts the model can read on demand. | Any text files. |

The standard defines nothing else in the folder. A host MUST ignore every other entry. Files
such as `.claude-plugin/plugin.json` or `hooks/` may be present for one product's benefit, and
other hosts ignore them.

A folder package MUST NOT contain a symbolic link, at any depth. A host MUST NOT read anything
outside the folder on a package's behalf.

Installing a package runs nothing. The only thing in a package a host may ever execute is a
local MCP server command, and only under the consent rule in part 7.

## 2. `VALUES.md` frontmatter

A `VALUES.md` file is YAML frontmatter followed by a Markdown body. Multiword keys use hyphens.

In the table, a field inside an object is written with a dot (`steward.name`), and a field of
each entry in a list is written with `[]` (`models[].base`). "Required" for such a field means
required whenever the object that holds it is present.

<!-- values-md:field-table -->
| Field | Required | Type and limits | Purpose |
|---|---|---|---|
| `name` | Yes | String of at most 64 characters, in name form | Identifier. Unique within a collection. Appears in the injected prompt. |
| `description` | Yes | String of 1 to 1,024 characters | What the value system is and who it is for. Shown to the user at install and on a listing. It may run over more than one line. |
| `steward` | Yes | Object with no other keys | Who vouches for the package and what kind of authority they claim. See part 9. |
| `steward.name` | Yes | String of 1 to 100 characters, on one line without `<`, `>` or `"` | The steward's name. Appears in the injected prompt. |
| `steward.claim` | Yes | One of `individual`, `organization`, `official` | The kind of authority the steward claims. See part 9. |
| `steward.url` | When `claim` is `organization` or `official` | String of at most 500 characters, in the form of an `https` URL | Where the claim can be checked. Optional when `claim` is `individual`. |
| `version` | No | String in Semantic Versioning 2.0.0 form | Version of the package. Recommended. |
| `spec-version` | No | String in the form of two numbers joined by a dot | Version of this standard the file targets. Default `"0.1"`. See part 11. |
| `license` | No | String of 1 to 100 characters | Licence of the package's content. An SPDX identifier where one exists. |
| `authors` | No | List of 1 to 20 items, each a string of 1 to 100 characters | Who wrote the text, when different from the steward. |
| `tradition` | No | List of 1 to 4 items, each a string of 1 to 64 characters | The tradition, school or community the value system belongs to, in its adherents' own terms, broadest first, for example `[Islam, Sunni]`. |
| `languages` | No | List of 1 to 20 items, each a string in the form of a BCP 47 language tag | The languages the package is written in and meant to answer in. |
| `tags` | No | List of 1 to 20 items, each a string of at most 64 characters, in name form | Free keywords for search. |
| `persistence` | No | Object with no other keys | Tunes reinjection. See part 5. |
| `persistence.reinject` | No | Object with no other keys | Holds the two settings below. |
| `persistence.reinject.every-tokens` | No | Integer from 1,000 to 1,000,000 | The reinjection interval, in tokens. Default 5,000. |
| `persistence.reinject.section` | No | String of 1 to 100 characters, on one line | The heading text of the core section. Default `Core`. See part 3. |
| `models` | No | List of 1 to 20 items, each an object with no other keys | Declares fine-tuned models. See part 6. |
| `models[].provider` | Yes | String of at most 64 characters, in name form | The service that serves the weights, for example `tinker`. |
| `models[].base` | Yes | String of 1 to 200 characters | The base model the fine-tune was trained from, exactly as the provider names it. |
| `models[].adapter` | Yes | String of 1 to 500 characters | The provider's own reference to the fine-tuned weights. |
| `models[].prompt` | No | One of `required`, `optional`, `omit` | How the model relates to the package's prompt. Default `required`. See part 6. |
| `models[].context-window` | No | Integer from 1 to 100,000,000 | The model's context window, in tokens. |
| `models[].description` | No | String of at most 500 characters | What the model was trained to do and on what. |
| `models[].trained-on` | No | String in Semantic Versioning 2.0.0 form | The package version the model was trained to embody. |
| `metadata` | No | Object with any keys and any JSON values | Extension space. The standard gives it no meaning. |

The forms the table names:

- **Name form**: one or more runs of the lowercase letters `a` to `z` and the digits `0` to
  `9`, joined by single hyphens. So there is no leading, trailing or doubled hyphen, and no
  capital letter.
- **The form of an `https` URL**: `https://`, then a host name, then optionally a colon and a
  port, then optionally a path, a query and a fragment. The host name is one or more labels of
  letters, digits and hyphens joined by dots, and no label begins or ends with a hyphen. The
  URL holds no user name, no password and no whitespace.
- **Semantic Versioning 2.0.0 form**: a version as [Semantic Versioning
  2.0.0](https://semver.org/spec/v2.0.0.html) defines it, such as `1.0.0` or `0.3.0-draft.1`.
- **The form of a BCP 47 language tag**: a tag that is well formed by the grammar of RFC 5646,
  section 2.1, such as `en`, `ar` or `zh-Hant`. Whether its subtags are registered is not
  checked.

The frontmatter schema, [`schema/values.schema.json`](schema/values.schema.json) (JSON Schema,
draft 2020-12), carries every rule in this table, with each form as a regular expression.
Rule V3 is decided by the schema, so where the words above leave a detail open, such as which
characters a URL's path may hold, the schema's expression settles it. The `consistency` check
described in [`README.md`](README.md) fails if the table and the schema disagree.

Types are the types the YAML reader of part 3 gives. Three consequences catch authors out:

- `spec-version` MUST be quoted. An unquoted `0.1` is a number, not a string.
- `version: 1.0.0` is a string and needs no quotes. `version: 1.0` is a number, and is not a
  Semantic Versioning string either way.
- `every-tokens` and `context-window` are whole numbers. A quoted `"5000"` is a string.

Unknown keys:

- At the top level, an unknown key is allowed, and a host MUST ignore it. This is what lets a
  later version add a field without breaking a v0.1 host.
- Inside `steward`, `persistence`, `persistence.reinject` and each `models` entry, an unknown
  key makes the file invalid. A misspelled `claim` or `prompt` must not pass silently.

Every key inside `persistence` and `persistence.reinject` is optional. An absent key takes its
default, so `persistence: {}` is valid and changes nothing.

A collection MAY require fields that are optional here, such as `version` and `license`. It
adds fields of its own only under `metadata`.

## 3. Reading the file: body, prompt and core

The always-on prompt is the entire Markdown body. The **core** is the short part of it that is
reinjected. So that two independent readers get the same text from the same bytes, the
standard fixes how the file is read. A reader MUST apply these rules in this order.

1. **Encoding.** The file is UTF-8. A leading byte-order mark is dropped. Every CRLF pair and
   then every remaining lone CR is turned into LF, before anything else is done.
2. **Frontmatter.** The first line is exactly `---`, with nothing after it, not even a space.
   The frontmatter runs to the next line that is exactly `---`. The frontmatter text is the
   lines between those two lines, joined by line feeds, and it is at most 8,000 characters.
   Neither `---` line is counted.

   The frontmatter text is parsed as YAML 1.2 with the core schema. It MUST be a single YAML
   document that is a mapping. It MUST NOT contain, at any depth:

   - a key that appears twice in one mapping;
   - an anchor or an alias;
   - an explicit tag, including the core schema's own, such as `!!str`;
   - a mapping key that is not a string;
   - a number that is infinite or not a number.

   The last three keep the frontmatter within what JSON can hold. Under the core schema a
   date-like value such as `2026-01-01` is a string, the words `yes`, `no`, `on` and `off` are
   strings, and `<<` is an ordinary key that merges nothing. A reader built on a YAML 1.1
   library has to switch those behaviours off.
3. **Body.** Everything after the closing `---` line, trimmed.
4. **Characters** are counted after rules 1 to 3 have been applied, as Unicode code points,
   with no normalization.
5. **Headings.** The body is split into lines at line feeds. A **fenced code block** follows
   the CommonMark rule:

   - It opens on a line that is indented by at most three spaces and then starts with three or
     more backticks, or three or more tildes. Anything may follow on that line, except that a
     line opened with backticks holds no further backtick, so a line that is one span of
     inline code between triple backticks opens nothing.
   - It closes on the next line that is indented by at most three spaces and then holds only
     the same character, at least as many times as the opening line had, followed by nothing
     but spaces.
   - A block that is never closed runs to the end of the body.

   A **heading** is a line outside any fenced code block that starts, at the first column,
   with one or two `#` characters and then a space. One `#` makes a first-level heading and
   two a second-level heading. Nothing else is a heading: not a line that starts with three or
   more `#` characters, not an indented line, not `##Core` with no space, and not a Setext
   heading (a line underlined with `---` or `===`).
6. **Heading text** is the rest of the line after the `#` characters and the space, trimmed,
   then with any run of `#` characters removed from its end, then trimmed again. So `## Core`,
   `##   Core  `, `## Core ##` and `## Core#` all have the text `Core`. Inline formatting is
   not stripped, so `## **Core**` has the text `**Core**`.
7. **The core section** is the second-level heading whose text equals the core section name,
   compared without regard to case. The core section name is `persistence.reinject.section`
   when that is given and `Core` when it is not. **The core** is the text after that heading
   line, up to the next first- or second-level heading or the end of the body, trimmed. The
   heading line itself is not part of the core. A line that starts with `###` is not a
   heading, so it does not end the core.
8. **No core section.** If no heading matches and the body is 1,500 characters or fewer, the
   whole body is the core. If no heading matches and the body is longer, the file is invalid.
   If one heading matches, that section is the core, whatever the body's length. If two or
   more headings match, the file is invalid.

Limits: the body is at most 7,500 characters and is not empty. The core is at most 1,500
characters and is not empty. A body that is only whitespace is empty.

**Reserved text.** The body MUST NOT contain a tag that belongs to the texts of part 4,
whether opening or closing. Precisely, it must not contain, anywhere, a `<`, then any amount
of whitespace or none, then an optional `/`, then any amount of whitespace or none, then
`values` or `value-system`, compared without regard to case. That covers all four elements
the texts use: `<value-system>`, `<values>`, `<value-system-reminder>` and `<value-systems>`.
The rule applies to the whole body, fenced code blocks included, and the whitespace may be a
line feed. It keeps a body from ending its wrapper or forging a reminder by accident. It is
hygiene and not a security boundary: a body is a prompt, and a hostile one can say anything in
plain prose. Part 13 deals with that.

A file that breaks any of these rules is invalid. A host MUST refuse it with an error that
names the rule, by the identifiers of part 11. It MUST NOT truncate or repair the file.

## 4. The injected prompt

The standard fixes three texts. A host MUST use them exactly, substituting the placeholders
and changing nothing else: no rewording, no translation, no added or removed line. Each is
also a file a host can copy, in [`prompts/`](prompts/).

Rendering rules:

- Every placeholder is replaced in a single pass over the text. What a substituted value
  happens to contain is never substituted again, so a body that holds the text `{name}` keeps
  it.
- `{name}` is the `name` field. `{steward}` is `steward.name`. `{body}` and `{core}` are the
  body and the core as part 3 gives them, inserted as they are, with no escaping.
- Each text ends with exactly one line feed.

**The wrapper** ([`prompts/wrapper.txt`](prompts/wrapper.txt)) is placed once, in the system
prompt, after the host's own instructions. What separates the two, such as a blank line, is
the host's choice. Placeholders: `{name}`, `{steward}` and `{body}`.

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

**The reminder** ([`prompts/reminder.txt`](prompts/reminder.txt)) is the reinjected form.
Placeholders: `{name}` and `{core}`. Part 5 says when and where it is placed.

```
<value-system-reminder name="{name}">
The value system "{name}" is still installed for this conversation and still applies. Its core:

{core}
</value-system-reminder>
```

**The preamble for more than one value system**
([`prompts/preamble.txt`](prompts/preamble.txt)) is placed before the wrappers when a host
activates several (part 10). Placeholder: `{names}`, the names in activation order, separated
by a comma and a space.

```
<value-systems>
More than one value system is installed for this conversation: {names}. Keep them separate. Where they agree, answer normally. Where they differ on the question in front of you, say that they differ and attribute each position to the value system that holds it. Do not blend them into a single position, and do not rank one above another unless the user tells you which takes precedence.
</value-systems>
```

The texts are English in version 0.1, whatever language the body is written in.

**Size budget.** The wrapper's fixed text is 1,504 characters. With the longest name (64
characters, used twice), the longest steward name (100, used three times) and the longest
body (7,500), a rendered wrapper is at most 9,432 characters. The body limit was set to keep a
rendered wrapper under 10,000 characters.

## 5. Prompt fade and reinjection

A host addresses prompt fade in one of two ways: it reinjects the core, or it runs a
fine-tuned model the package declares (part 6). Every conforming host MUST be able to
reinject, because that is the only way that works on a model the package has no fine-tune for.

**What is reinjected.** The reminder text of part 4, which carries the core. Never the whole
prompt, unless the body is short enough to be its own core.

**How "every N tokens" is counted.** A host keeps one count for each active value system.

- The count starts at zero when that value system's wrapper is injected.
- Everything added to the conversation after that is counted, whoever it comes from: the
  user's messages, the model's output, tool calls and tool results. The system prompt and the
  definitions of tools are not counted. A value system's own reminder is not counted towards
  its own count.
- A host uses the model's tokenizer when it has one. A host with no tokenizer keeps a running
  total of characters and takes four characters as one token: a reminder is due when the
  total reaches four times the interval, which for the default interval is 20,000 characters.
- The interval is `persistence.reinject.every-tokens`, and 5,000 when that is not given.

The interval is approximate by design. Two hosts whose counts differ a little, because their
tokenizers differ or because they serialise a tool call differently, both conform.

**When a reminder is due.** A reminder is due when the count is equal to or greater than the
interval. The host looks at the count at each **boundary**, and a boundary is:

- the moment a user message is about to be added to the conversation, before that message's
  own text is counted. Every host MUST treat this as a boundary. A user message here means
  what the user sends. A message that only carries a tool result is not one, whatever role
  the API gives it;
- the moment after a tool result has been added and counted, during a run with no user
  message. A host MAY treat this as a boundary.

When a reminder is due at a boundary, the host places it there and sets the count back to
zero. A value system gets at most one reminder at a boundary, however large its count. A
single tool result of 30,000 tokens produces one reminder, not six.

So in a conversation with the default interval, the first reminder falls at the start of the
first user message that arrives after 5,000 tokens have been added since the wrapper.

**Where the reminder goes.** At the start of the user message, before the user's own text and
separate from it:

- where the API has content blocks, the reminder is a block of its own and the first block of
  the message;
- otherwise the message is the reminder, then one line feed, then the user's text. Since the
  reminder ends with a line feed, this leaves one blank line between them.

A host whose model accepts a system message in the middle of a conversation MAY use one
instead, placed immediately before the user message. At a tool-result boundary the reminder
goes after the tool result. A reminder MUST NOT be placed inside an assistant turn.

A host MAY drop older reminders from context and keep the most recent.

A package can change the interval and the section name. It cannot turn reinjection off.

## 6. Fine-tuned models

A package MAY declare fine-tuned models in `models`. Each entry has three required fields:

- `provider`: the service that serves the weights, in name form, for example `tinker`.
- `base`: the base model the fine-tune was trained from, exactly as the provider names it.
  The same weights saved for two context windows are two entries with two `base` values.
- `adapter`: the provider's own reference to the fine-tuned weights, for example a Tinker
  `tinker://<run_id>/sampler_weights/<name>` path.

and four optional ones: `prompt`, `context-window`, `description` and `trained-on`. The table
in part 2 gives the limits of each.

**Public models only.** A package MUST declare only a model that anyone with access to the
provider can load. There is no field for access and no notion of a restricted model. Whether a
declared model really is loadable cannot be told from the files, so it is not a validity rule
(part 11). A collection can check it when a package is submitted, and a host finds out when it
tries.

**Matching.** An entry matches when the host is using that `provider` and the model it would
otherwise run is named by exactly the `base` string. There is no nearest match and no
conversion between providers or between base models. When nothing matches, the host ignores
`models` and reinjects.

**With or without the prompt.** A fine-tuned model can run with the package's prompt still
injected, or stand on its own without it. Which of these a model supports is a fact about how
it was trained and tested, so the package declares it, in `prompt`:

| `prompt` | The package is saying | What a host may do |
|---|---|---|
| `required` (the default) | This model is meant to run with the wrapper and body in context. | Run it with the prompt. |
| `optional` | This model works with the prompt and also on its own. | Run it either way. With the prompt unless the user or operator chooses otherwise. |
| `omit` | This model is meant to stand on its own. Putting the prompt on top of it is untested or unwanted. | Run it without the prompt. |

That gives a package three ways to be active:

| Mode | Model | Wrapper and body | Reinjection |
|---|---|---|---|
| A | The host's own | Injected | Yes |
| B | A declared model whose `prompt` is `required` or `optional` | Injected | The host MAY skip it |
| C | A declared model whose `prompt` is `optional` or `omit` | Not injected | None |

A host MUST offer mode A. It is never required to offer mode B or C.

**Who chooses.** The package says which modes a model supports. The user or operator chooses
whether to use a declared model at all, and, where `prompt` is `optional`, whether to run it
with the prompt. A host MUST NOT switch to a declared model on its own, and MUST NOT drop the
prompt unasked. Where `prompt` is `required` or absent, a host MUST NOT offer to run that
model without the prompt. Where `prompt` is `omit`, a host MUST NOT run that model with the
prompt.

**What the user is shown holds in every mode.** The host shows the name, the steward, the
kind of claim and where the package came from, at install and for as long as the value system
is active (part 9). In modes B and C it MUST also show that a fine-tuned model is in use, and
name it. In mode C the model has nothing in context that tells it what is installed, so the
wrapper's rule that the model says so when asked cannot be relied on. The host's own display
carries that duty, and the host MUST show that the prompt is not injected.

**What mode C gives up.** Without the wrapper and body, none of the wrapper's rules are in
context, nor are any instructions the body gives about tools. How the model behaves rests on
its weights, which neither the host nor the user can read. A host MUST say this when the user
chooses mode C. Tools from `.mcp.json` stay connected in every mode.

**When a declared model fails to load**, the host MUST tell the user which model failed and
go back to mode A: its own model, with the prompt and reinjection. It MUST NOT go on in mode C
without the model, and it MUST NOT try another entry unless the user chooses one. A package
that declares a model the public cannot load is breaking the rule above, and a host MAY say
so.

**Mode C needs the package to be alone.** Mode C is available only when that package is the
only active value system. With several active, every package has its wrapper in context
(part 10).

## 7. Tools, skills and conformance levels

A host claims one of three levels. Each includes the one before it.

| Level | The host does | Typical host |
|---|---|---|
| 1. Prompt | Reads `VALUES.md`, checks it, injects the wrapper, addresses prompt fade, shows what is installed. | Any chat product. Enough for a single-file package. |
| 2. Tools | Also connects the remote MCP servers in `.mcp.json`. | A plain chat loop with an MCP client. |
| 3. Package | Also exposes `skills/` as Agent Skills and lets the model read `references/` on demand. MAY run local MCP servers. | A coding agent or desktop assistant. |

MCP is how a host with no skill or plugin loader uses a package's tools: a Level 2 host
connects to each remote server as any MCP client does and offers the server's tools to the
model. It needs no file system, no shell and no skill loader.

A host that is given a package above its level uses the parts it understands and ignores the
rest. A Level 2 host given a package with `skills/` and `references/` ignores both, and the
prompt and the remote tools still work.

Consequences for authors: anything essential goes in the body, any essential tool goes in
`.mcp.json` as a remote server, and `skills/` and `references/` are for depth a lower-level
host can do without.

### The shape of `.mcp.json`

`.mcp.json` is a JSON document in UTF-8. JSON here means RFC 8259: the words `NaN` and
`Infinity`, which some parsers accept, are not JSON.

The document is an object with an `mcpServers` key whose value is an object. Other top-level
keys are ignored. An empty `mcpServers` object is valid and declares no servers.

Each key of `mcpServers` is a server's name: 1 to 64 characters, each a letter `A` to `Z` or
`a` to `z`, a digit, a hyphen or an underscore. Each value is an object that is exactly one
of:

- **Remote:** it has `url`, a string beginning `https://`. It MAY have `type`, which is then
  `http` or `sse`. An `http://` address is invalid, loopback included. Nothing more is asked
  of the address than that beginning.
- **Local:** it has `command`, a string of at least one character. It MAY have `args`, a list
  of strings, and `env`, an object whose values are strings.

An object with both `url` and `command`, or with neither, is invalid. The rules for a remote
server apply when `url` is present, and those for a local server when `command` is present.
So `type` on a local server is one more ignored key, and the common `"type": "stdio"` is
valid there.

`headers` MUST NOT be present on any server, because the only use for it in a published
package is a credential. A server that needs a credential gets it from the host, through MCP's
own authorisation or the host's settings. Every other key inside a server is ignored.

[`schema/mcp.schema.json`](schema/mcp.schema.json) restates this shape as a JSON Schema.

### Consent and trust

Installing a package does not authorise what it declares.

- A host MUST have the user's or operator's consent, given for that package and that server,
  before it first connects to a remote server, and it MUST show the address when it asks. A
  user's questions go to that address.
- A host MUST NOT start a local server without the same consent, shown with the full command,
  its arguments included. A host MAY refuse all local servers, and a collection MAY refuse to
  list packages that have them.
- What comes back from a tool, and what is in a skill or a reference text, is untrusted
  content like any other tool output. It does not gain the standing of the wrapper or of the
  host's own instructions.

## 8. Discovery and installation

- The file name is exactly `VALUES.md`, in upper case, matched case-sensitively, including on
  a file system that does not distinguish case.
- There is no ambient discovery. A value system becomes active only when a user or operator
  explicitly installs it. A host that finds a `VALUES.md` in a working directory MAY offer to
  install it and MUST NOT activate it unprompted. This is deliberate: cloning a repository
  must not change an assistant's values.
- A folder is a package if and only if `VALUES.md` is at its root.
- A host MUST check a package before it installs it, and install it only when the outcome is
  valid (part 11). A Level 1 host, which reads only `VALUES.md`, checks rules V1 to V6. Handed
  a folder, it reads the `VALUES.md` at the folder's root, and it does not read one that is a
  symbolic link, since that may point outside the folder (part 1). A host that reads the
  folder checks V1 to V9. When the outcome is "unsupported version", the host says that the
  package targets a version of the standard it does not implement.
- Before activating a package, a host MUST show the user its name, description, steward and
  kind of claim, version, where the package came from, and the tools and models it declares.
- Where a host keeps installed packages is its own business. The suggested shared location
  for file-based hosts is `~/.agents/values/<name>/`.

## 9. Provenance

`steward` says who vouches for the package, and `steward.claim` says what kind of authority
that is:

| `claim` | Meaning |
|---|---|
| `individual` | A person offering their own statement of the value system. They speak for nobody else. |
| `organization` | An organization that stands behind the package as its own work. It does not claim to be the authority over the value system. |
| `official` | The steward says it is the body with authority over this value system, or is authorised by that body, and that this package is its official statement. |

`authors` records who wrote the text when that differs from who vouches for it.

Both the steward and the claim are statements made by the package. The standard cannot verify
them in version 0.1. For `organization` and `official`, `steward.url` is required, so that
there is somewhere to check the claim. What evidence a claim needs before a package is listed
is for the collection that lists it to decide.

How a user can tell: the host shows them. A host MUST

- show the steward, the kind of claim and where the package came from when it is installed;
- keep them available for as long as the value system is active;
- never instruct the model to conceal the installed value system.

This holds in every mode of part 6, including a fine-tuned model running without the prompt,
where the host's display is the only thing that tells the user what is installed. When the
wrapper is in context, its rule 6 also makes the model state the name and the steward when
asked.

Verifying a steward mechanically, for example through a well-known URL on the steward's
domain or a signature, is left to a later version.

## 10. More than one value system

A host MUST support one active value system per conversation. It MAY let a user keep several
installed and choose between them. It MAY activate several at once, under these rules:

- The preamble of part 4 comes first, then one wrapper for each package, in the order the
  user activated them. All of it goes in the system prompt after the host's own instructions.
- Two packages with the same `name` are never active together. The host MUST refuse the
  second.
- Each package has its own count and its own interval. At a boundary, every package whose
  reminder is due gets it, in activation order. One package's reminder counts towards the
  other packages' counts like anything else added to the conversation.
- A fine-tuned model belongs to the package that declares it. Running it lets the host skip
  reinjection for that package only. The others are reinjected as usual.
- With several value systems active, every package's wrapper is in context, so no model runs
  without its prompt (part 6, mode C).
- Value systems are never merged. When they conflict on a question, the preamble tells the
  model to say that they differ and to attribute each position to the value system that holds
  it. A package cannot declare precedence over another. Only the user can.

## 11. Validity

The standard gives one definition of a valid package, so that a host at install and a
collection's submission check reach the same answer. Validity is decided from the package's
files alone. It needs no network call and no model.

A check has three possible outcomes:

- **Valid.**
- **Invalid**, with the identifier of every rule that failed.
- **Unsupported version**, when `spec-version` names a version the checker does not
  implement. This is not a rule failure. A package written for a later version is not
  malformed, and a v0.1 checker says only that it cannot judge it.

The rules apply in three scopes. A single file is checked against the file rules. A folder is
checked against the file rules and the folder rules. A collection checks every package in it
against all of them.

<!-- values-md:rule-table -->
| Rule | Scope | A package is valid only if |
|---|---|---|
| V1 | File | The file is named exactly `VALUES.md`, is UTF-8, and opens with frontmatter between two `---` lines, of at most 8,000 characters. |
| V2 | File | The frontmatter is a single YAML 1.2 document that is a mapping, with nothing in it that reading rule 2 of part 3 forbids. |
| V3 | File | The frontmatter validates against the schema, which carries every field rule of part 2, including the `steward.url` condition and the rules on unknown keys. |
| V4 | File | The body is not empty and is at most 7,500 characters. |
| V5 | File | The core resolves to exactly one non-empty text of at most 1,500 characters, by the rules of part 3. |
| V6 | File | The body contains no reserved text, as part 3 defines it. |
| V7 | Folder | `.mcp.json`, if present, has the shape part 7 defines. |
| V8 | Folder | Every folder directly inside `skills/` is a valid Agent Skill by that standard's own rules. |
| V9 | Folder | The folder contains no symbolic link, at any depth. |
| V10 | Collection | The package's folder name equals its `name`, and no other package in the collection has that name. |

### Order of evaluation

An invalid package is reported with every rule that failed. Some rules cannot be judged once
an earlier one has failed, so the order is fixed. A rule that could not be judged is not
reported at all.

1. **V1.** If it fails, no other file rule is judged.
2. **V2.** If it fails, the rules that need the frontmatter are not judged: the version gate,
   V3, V5 and V10. V4 and V6 need only the body and still are.
3. **The version gate.** If `spec-version` is present, is a string in the form of two numbers
   joined by a dot, and is not exactly `0.1`, the outcome is "unsupported version". No further
   rule is judged for that package at any scope, and nothing else about it is reported.
4. **V3.** A `spec-version` that is not a string, or not in that form, fails here. An unquoted
   `spec-version: 0.2` is a number, so it is a V3 failure and not an unsupported version.
5. **V4 and V6**, on the body.
6. **V5**, unless the body is empty, or `persistence.reinject.section` is given and is not a
   valid value. In both cases another rule has already reported the cause.
7. **V7, V8 and V9**, each on its own, at folder scope. They are judged whatever the file
   rules found, a failure of V1 included.
8. **V10**, at collection scope, whenever `name` could be read as a string, even one that is
   not in name form.

### Notes on the rules

- **A directory where a file belongs.** An entry named `VALUES.md` that is a directory fails
  V1. A directory named `.mcp.json` fails V7. A directory named `SKILL.md` inside a skill
  folder fails V8.
- **A folder with no `VALUES.md`** is not a package. Checked as one, it fails V1.
- **V8** applies the Agent Skills rules as that project's reference validator applies them:
  the skill folder holds a `SKILL.md` (or, when there is none, a `skill.md`) that opens with
  YAML frontmatter that is a mapping; the frontmatter has no field Agent Skills does not
  define; `name` is present, is at most 64 characters of lowercase letters, digits and single
  hyphens, and equals the folder's name; `description` is present and at most 1,024
  characters; and `compatibility`, if present, is a string of at most 500 characters. These
  are that format's rules, not this one's, and they differ from name form in one respect: a
  skill's name may hold letters and digits of any script. V8 looks only at the folders
  directly inside `skills/`. A file there is ignored, and so is a file named `skills`.
- **V9 and symbolic links.** Nothing is read through a symbolic link, because what it points
  at may lie outside the package. V9 reports the link, and a rule that would have needed the
  link's content is not judged. So a package whose `VALUES.md` is a link fails V9 alone. In a
  collection, a package folder that is itself a link fails V9 and is not read. When a single
  folder is checked on its own, how that folder was reached is not judged.
- **V10 and collections.** Every folder directly inside a collection is a package, and a file
  there is ignored. When two packages share a name, both fail V10. A package whose outcome is
  "unsupported version" takes no part in V10, even when it claims a name another package has.

### What validity does not cover

Whether a declared tool answers, whether a declared model loads, whether a steward's claim is
true, and whether the content is acceptable. Those need a network, an account or a human, and
a collection adds them as its own checks.

### Fixtures

[`fixtures/`](fixtures/) holds a set of small, purpose-made packages: valid ones, each with
the exact wrapper and reminder it renders to, and for every rule at least one invalid one,
labelled with the rule it breaks. [`fixtures/fixtures.json`](fixtures/fixtures.json) lists
them with the outcome a conforming checker gives for each. A checker written for a host or a
collection can be tested against them.

## 12. Collections, listings and the marketplace mapping

A collection is a directory with one folder for each package, each folder named for its
package. The standard defines this much so that a browser and a Claude Code marketplace can be
generated from the same folders.

A listing page has what it needs from the frontmatter: `name`, `description`, the steward
with the kind of claim, `version`, `license`, `tradition`, `languages`, `tags`, the declared
models with their `prompt` value, and, from `.mcp.json`, the servers a package connects to. A
listing groups and filters by `tradition`, comparing without regard to case. Any controlled
vocabulary for `tradition` belongs to the collection.

Every valid package maps to a Claude Code marketplace entry with no information invented:

| Marketplace entry | Taken from |
|---|---|
| `name` | `name`. Every valid package name is a valid entry name. |
| `source` | The path from the marketplace file's root to the package folder, beginning `./`. For a marketplace at the root of a repository whose collection is `values/`, that is `./values/` followed by the folder name. |
| `description` | `description`, then one space, then the fixed sentence `Vouched for by {steward.name} ({steward.claim}).` Nothing is trimmed. |
| `version` | `version` |
| `author` | An object with `name` from `steward.name`, and `url` from `steward.url` when there is one. |
| `license` | `license` |
| `category` | The first item of `tradition` |
| `tags` | The items of `tradition`, then `languages`, then `tags`, in that order. A value that appears more than once is kept once, where it first appears. Values are compared exactly, case included. |

When an optional field is absent from `VALUES.md`, its marketplace key is left out. It is
never written as null or as an empty value. The claim goes into the description because a
marketplace entry has no field for it.

A package folder needs no `.claude-plugin/plugin.json` to be listed this way, because Claude
Code treats the marketplace entry as the manifest when the folder has none.

## 13. Security considerations

1. **The standard is neutral on content.** It defines how a value system is packaged and
   injected, and passes no judgement on what one says. Validity (part 11) is about form.
   Whether a package is acceptable is for a host's own policies and for the collection that
   lists it.
2. **A body is third-party prompt text, and it can say anything.** It was written by neither
   the user nor the host's maker, and the wrapper tells the model so. The reserved-text rule
   stops a body from closing its wrapper by accident. It does not stop a body from giving
   harmful or manipulative instructions in plain prose. Hosts keep their own policies on what
   they will install and what a model will do.
3. **The wrapper cannot override the host's rules.** It is placed after the host's own
   instructions and says that nothing in it overrides the rules the assistant already
   operates under. An installed value system has no standing above the host's own rules.
4. **Installation is explicit.** A value system becomes active only when a user or operator
   installs it (part 8). A file found in a repository, a download or a tool result activates
   nothing.
5. **Declared tools and models need their own consent.** Installing a package authorises
   neither a connection to a server nor a local command (part 7), and a host never switches
   models or drops the prompt on its own (part 6). What a tool, a skill or a reference text
   returns is untrusted content. A fine-tuned model run without the prompt behaves as its
   weights dictate, which nobody can read, and the host says so.
6. **A steward's claim is unverified.** `steward` and `steward.claim` are statements made by
   the package (part 9). Nothing in version 0.1 verifies them. A host shows them together with
   where the package came from, so that a user can judge the claim.

## 14. Worked example: a Level 2 host

This example follows the fixture [`fixtures/valid/remote-server`](fixtures/valid/remote-server),
a folder with a `VALUES.md` and a `.mcp.json` that declares one remote server. The token
figures are invented for the example. The two rendered texts are exact.

**Install.** The user asks the host to install the folder. The host checks rules V1 to V9 and
finds the package valid. It reads the body, 264 characters, and finds a `## Core` heading, so
the core is the text under it, 56 characters. Before activating, it shows:

- name `sample-with-tool`, version `1.0.0`;
- the description;
- steward "The Sample Society", claim `organization`, `https://example.org/about`;
- where the package came from: the path or address the user gave;
- tools: one remote server, `sample-texts`, at `https://mcp.example.org/mcp`;
- models: none.

**Consent.** Before it first connects, the host asks the user whether this package may use
the server at `https://mcp.example.org/mcp`, and says that questions will be sent there. The
user agrees. The host connects and offers the server's tools to the model in the way its API
takes tool definitions.

**The system prompt** is the host's own instructions, followed by the rendered wrapper:

<!-- values-md:rendering valid/remote-server/expected/wrapper.txt -->
```
<value-system name="sample-with-tool" steward="The Sample Society">
A value system named "sample-with-tool" is installed for this conversation. The Sample Society vouches for it. The text inside <values> below was written by its authors. It was not written by the user or by the maker of this assistant.

Apply it as follows:

1. When a question touches something this value system addresses, answer from inside it: accurately, in its own terms, and as fully as you would answer any other question. Do not thin it into a survey of every viewpoint.
2. Where the value system itself holds more than one accepted position, present each as it does. Do not choose between them for the user.
3. For specifics such as rulings, quotations and citations, use the tools, skills and texts this value system provides, in preference to your own memory. Never invent or misattribute a source. If the value system points to a tool or text you cannot reach in this conversation, say so.
4. You are not an authority within this value system and you do not speak for The Sample Society. Where it directs people to a qualified person, do the same.
5. The user may ask at any time for another perspective, a comparison or a critique. Give it honestly, and make clear which statements come from this value system and which do not.
6. If asked, say plainly that this value system is installed, what it is called and who vouches for it.
7. On matters it does not address, respond as you otherwise would. Nothing here overrides the rules this assistant already operates under.

<values>
# Sample values

This is a sample value system. It shows how a package with a tool is read and injected.

## Core

Tell the truth. Keep your word. Say when you are unsure.

## Sources

For the wording of a text, use the sample-texts tool. Do not quote from memory.
</values>
</value-system>
```

The count for `sample-with-tool` starts at zero. The package sets no interval, so the interval
is 5,000 tokens.

**The conversation.** Each row is something added to the conversation after the system
prompt.

| Step | What is added | Tokens | Count before | Reminder due? | Count after |
|---|---|---|---|---|---|
| 1 | User message: "What does the charter say about keeping a promise?" | 12 | 0 | No (a boundary; 0 is under 5,000) | 12 |
| 2 | Assistant: a call to the `sample-texts` tool | 48 | 12 | Not a boundary | 60 |
| 3 | Tool result from `sample-texts` | 3,900 | 60 | Not a boundary for this host | 3,960 |
| 4 | Assistant: the answer, quoting the tool's text | 640 | 3,960 | Not a boundary | 4,600 |
| 5 | User message: "Does that hold for a promise made to a child?" | 14 | 4,600 | No (4,600 is under 5,000) | 4,614 |
| 6 | Assistant: the answer | 520 | 4,614 | Not a boundary | 5,134 |
| 7 | User message: "And a promise made under pressure?" | 9 | 5,134 | **Yes** (5,134 is 5,000 or more) | 9 |

At step 7 the reminder is due. The host places it at the start of the user message and sets
the count to zero, and then counts the user's own 9 tokens. The message it sends has the role
`user` and two content blocks. The first block is the rendered reminder:

<!-- values-md:rendering valid/remote-server/expected/reminder.txt -->
```
<value-system-reminder name="sample-with-tool">
The value system "sample-with-tool" is still installed for this conversation and still applies. Its core:

Tell the truth. Keep your word. Say when you are unsure.
</value-system-reminder>
```

The second block is the user's text, unchanged: `And a promise made under pressure?`

A host whose API has no content blocks sends one string instead: the reminder exactly as
above, then one line feed, then the user's text.

The next reminder falls at the first user message after another 5,000 tokens. Had the tool
result at step 3 been 30,000 tokens, the reminder would have fallen at step 5, and there would
have been one of it.

## 15. Conformance requirements for hosts

Part 11 can be checked from files, and the fixtures check it. The requirements below can only
be checked by running a host. Each restates a rule from the part named, in a form a test can
observe.

- **H1. Reminder timing** (part 5). With the default interval, the first reminder is placed at
  the start of the first user message added after the count reaches 5,000 tokens, and not
  before. A single tool result of many times the interval produces one reminder.
- **H2. Fine-tuned model with the prompt** (part 6, mode B). When the user or operator
  chooses a declared model and keeps the prompt, the wrapper is injected, the host MAY skip
  reinjection for that package, and the host shows that a fine-tuned model is in use and names
  it.
- **H3. Different base model** (part 6). A host whose provider and model match no entry
  ignores `models`, injects the wrapper and reinjects.
- **H4. Model that fails to load** (part 6). A host that cannot load a chosen model tells the
  user which model failed and continues on its own model with the wrapper and reinjection.
- **H5. A package above the host's level** (part 7). A Level 2 host given a package with
  `skills/` and `references/` ignores them, connects the remote servers under the consent
  rule, and injects the complete wrapper.
- **H6. Two value systems** (part 10). With two active, the preamble comes first and names
  both in activation order, each package has its own wrapper, each has its own count, and each
  reminder is placed when its own count is due. A second package with a name already active is
  refused.
- **H7. Consent** (part 7). The host asks before it first connects to each declared remote
  server, showing the address, and before it starts each local command, showing the full
  command. Without consent it does neither.
- **H8. Fine-tuned model without the prompt** (part 6, mode C). With `prompt: optional` and
  the user choosing to drop the prompt, or with `prompt: omit`, nothing from the package is
  injected and no reminder is placed. The host still shows the name, the steward, the kind of
  claim and the source, names the model, shows that the prompt is not injected, and says what
  that gives up.
- **H9. Prompt not droppable** (part 6). With `prompt: required`, or with the field absent,
  the host does not offer to run the model without the prompt.
- **H10. Two value systems and a standalone model** (parts 6 and 10). With two packages
  active, the host does not run either one's model without its prompt.

## 16. Examples

Four example packages live in the collection at [`../values/`](../values/), one folder each.
They are listed here by path and are not copied anywhere under `spec/`. Each is valid where it
lives, by the rules of this document alone.

| Package | What it shows |
|---|---|
| [`values/plain-speaking`](../values/plain-speaking/) | The smallest valid package: the single file shown at the top of this document. A non-religious value system whose whole body is its core. |
| [`values/example-principled-pluralism`](../values/example-principled-pluralism/) | A minimal package: a `VALUES.md` with no core section, short enough to be reinjected whole. Its value system is a way of answering questions about religion, principled pluralism, taken from a published essay that the package cites. |
| [`values/example-islam`](../values/example-islam/) | A folder package that works at Level 2. Its `.mcp.json` declares a remote MCP server, its body sends specifics to that tool, and it declares a fine-tuned model with `prompt: omit`. |
| [`values/example-roman-catholic`](../values/example-roman-catholic/) | A folder package with Level 3 depth: a bundled public-domain text in `references/` and a skill in `skills/`. It declares no tool and no model. |

The three packages whose names begin `example-` are illustrations. Each describes someone
else's tradition or work, names the values.md project as its steward with the claim
`organization`, and says in its description, its body and its README that it is not endorsed:
by any religious authority for the two faith examples, and by the essay's author for the
third. The standard treats no example specially. The wrapper, the validity rules and this
document are the same for all four.

## 17. Questions this standard answers

| Question | Answered in |
|---|---|
| 1. How does a host with no skill or plugin loader use a package's tools? | Part 7: through MCP, by connecting the remote servers in `.mcp.json`. |
| 2. What is reinjected, where does it go, and how is "every N tokens" counted? | Part 5, with the core defined in part 3 and the reminder text in part 4. |
| 3. How do model declarations work across providers, and what does a host do on a base model the package has no fine-tune for? | Part 6, under "Matching": an exact match on `provider` and `base`, or the host ignores `models` and reinjects. |
| 4. Does a fine-tuned model replace reinjection, the prompt, both or neither? | Part 6: it may always replace reinjection, and it replaces the prompt only where the package allows it and the user or operator chooses it. |
| 5. Who wrote a package, who vouches for it, and how can a user tell? | Part 9. |
| 6. Can more than one value system be installed, and what happens when they conflict? | Part 10. |
| 7. Where does a framework for how to answer questions about religion fit? | Part 16: it is a value system like any other, and one of the examples. |
| 8. What is the file called, and how is it discovered? | Part 8. |

## References

- RFC 2119 and RFC 8174, key words for requirement levels.
- RFC 3629, UTF-8. RFC 8259, JSON. RFC 5646 (BCP 47), language tags.
- YAML 1.2.2, and its core schema: https://yaml.org/spec/1.2.2/
- CommonMark, for the fenced code block rule: https://spec.commonmark.org/
- JSON Schema, draft 2020-12: https://json-schema.org/draft/2020-12
- Semantic Versioning 2.0.0: https://semver.org/spec/v2.0.0.html
- SPDX licence list: https://spdx.org/licenses/
- Agent Skills: https://agentskills.io/specification
- Model Context Protocol: https://modelcontextprotocol.io/
- Claude Code plugin marketplaces: https://code.claude.com/docs/en/plugin-marketplaces.md
