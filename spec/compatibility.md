# Compatibility note for the values.md standard, version 0.1

A package is built from parts that existing products already read. This note says exactly
what three kinds of existing host get from a package today, with no support for the standard
itself: Claude Code, a host that only reads Agent Skills, and a host that only reads
AGENTS.md. It is not normative. The standard is [`specification.md`](specification.md).

This text is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## How to read this note

Every statement about Claude Code is marked with where it comes from:

- **Documented** means it is quoted or restated from the linked page of Claude Code's
  documentation, read on 2026-11-21 (UTC).
- **Observed** means it was seen on that date with Claude Code 2.1.330, on temporary copies of
  the packages in [`../values/`](../values/). No conversation with a model was started in
  those checks. A skill or a server described as available was listed by Claude Code, and the
  server was shown as connected. Neither was used by a model.

Nothing here was learned any other way. Where neither applies, the note says that the point
was not checked.

## Summary

| Host | What it gets from a package | What it does not get |
|---|---|---|
| A host that implements the standard | Everything its conformance level covers (specification, part 7) | |
| Claude Code, with the folder loaded as a plugin | The skills in `skills/` and the MCP servers in `.mcp.json` | The prompt, the reminder, the validity check, and the display of the steward and the claim |
| Claude Code, with a prompt adapter added | Also the wrapper and, through hooks, the reminder | Placement in the system prompt (hooks), or reinjection (output style) |
| A host that only reads Agent Skills | The skills in `skills/` | Anything always on |
| A host that only reads AGENTS.md | Nothing, unless the user pastes the body in by hand | The wrapper, the reminder and the tools |

## Claude Code

### A package folder as a plugin

A folder package is laid out like a Claude Code plugin: `skills/` and `.mcp.json` are where a
plugin keeps them.

- **Documented.** The manifest is optional, and `name` is its only required key: "The
  manifest is optional. Without it, Claude Code loads the components it finds in the standard
  layout."
  ([plugin manifest reference](https://code.claude.com/docs/en/plugins-reference.md))
- **Documented.** The standard layout puts skills in `skills/`, "One `<name>/SKILL.md` per
  skill", and MCP servers in `.mcp.json` at the plugin root. (same page)
- **Observed.** A copy of `example-roman-catholic` and a copy of `example-islam`, each with
  only `.claude-plugin/plugin.json` added and holding only a `name`, pass
  `claude plugin validate`. It reports what each provides: the skill
  `example-roman-catholic:catechism-answers` for the first, and the server `ansari` at
  `https://mcp.ansari.chat/mcp` for the second. Its warnings are about what the bare manifest
  leaves out: a version, a description and an author. None is about `VALUES.md` or
  `references/`.
- **Observed.** Loaded with `--plugin-dir`, `claude plugin details` lists the skill
  `catechism-answers` for the first and the server `ansari` for the second, and
  `claude mcp list` shows `plugin:example-islam:ansari` as connected. So Claude Code accepts a
  package's `.mcp.json`, with its servers under an `mcpServers` key, as it stands.

So adding one file, `.claude-plugin/plugin.json`, makes a package folder load as a plugin with
nothing else changed. The specification lets that file be present: a host of the standard
ignores every entry it does not define (part 1).

### What Claude Code does not do

Claude Code knows nothing about `VALUES.md`. Loading a package as a plugin gives it the
package's tools and skills and nothing of the value system itself.

- **It does not inject the prompt.** A plugin has no component that corresponds to
  `VALUES.md`. **Documented:** the standard layout lists no such file, and "A `CLAUDE.md` at
  the plugin root isn't loaded as context". **Observed:** validation and loading passed
  `VALUES.md` over without comment.
- **It does not reinject the core.** Nothing counts tokens on a package's behalf.
- **It does not check the package.** `claude plugin validate` checks the plugin's own files.
  It does not apply validity rules V1 to V10. Run the checker first
  ([`README.md`](README.md)).
- **It does not show the steward or the kind of claim** as the standard asks of a host (part
  9). See [what the install screen shows](#what-the-install-screen-shows).
- **It does not use `models`.** A declared fine-tuned model is not offered or loaded.
- **It has no component for a root `references/` directory.** **Documented:** the standard
  layout does not list one. The files are in the installed folder, and nothing tells the model
  they are there. A skill's own `references/` directory, inside the skill's folder, is part of
  that skill and is read as Agent Skills describes.
- **It does not ask for consent in the standard's terms.** Whether and how Claude Code asks
  before it connects a plugin's MCP server was not checked for this note. The standard's rule
  (part 7) is consent for each package and each server, with the address shown.

A body that tells the model to use a tool still helps only if the body reaches the model. The
skills and servers are there. The text that says when to use them is not, until a prompt
adapter supplies it.

### Supplying the prompt

There are two ways to get the wrapper into a Claude Code session: hooks, and a forced output
style. Each needs something added beyond the manifest, and each falls short of the standard in
a different place. Neither was built or run for this note. This section is **documented**
only, from the [hooks reference](https://code.claude.com/docs/en/hooks.md) and the
[output styles page](https://code.claude.com/docs/en/output-styles.md). The adapter itself is
code. It is not part of the standard, and it is not in this directory.

| | Hooks | A forced output style |
|---|---|---|
| The wrapper reaches the model | Yes, as added context at the start of the conversation | Yes, as part of Claude Code's instructions |
| Where it sits | In the conversation, wrapped in a system reminder | With the instructions sent on every request |
| The reminder | Yes, on a later prompt, from an estimated count | No |
| More than one value system | One hook output for each | No. One forced style is used |
| What is added to the folder | Hook configuration and a program that renders the texts | A generated file under `output-styles/` |
| Side effects | None on Claude Code's own instructions | Replaces the user's chosen style, and drops Claude Code's coding instructions unless told to keep them |

#### Hooks

A `SessionStart` hook emits the rendered wrapper, and a `UserPromptSubmit` hook emits the
rendered reminder when it is due.

- `SessionStart` can add context: `additionalContext` is a "String added to Claude's context
  at the start of the conversation, before the first prompt", and a hook that only adds
  context can print it as plain text. The event fires when a session starts and again on
  `resume`, `clear`, `compact` and `fork`. So the wrapper is emitted again after compaction,
  when the earlier conversation has been replaced by a summary.
- `UserPromptSubmit` can add context too: `additionalContext` is a "String added to Claude's
  context alongside the submitted prompt". This is where the reminder goes.
- **What a hook is given.** The page's table of common input fields lists `session_id`,
  `prompt_id`, `transcript_path`, `cwd`, `scratchpad_dir`, `permission_mode`, `effort` and
  `hook_event_name`. `UserPromptSubmit` also receives `prompt`, the submitted text. There is
  no running count of tokens. The one token figure is `context_tokens`, which `SessionStart`
  receives only when the source is `resume` or `fork`. An adapter therefore estimates the
  count from the transcript file, at four characters to a token, which part 5 of the
  specification allows a host with no tokenizer to do. The page warns that the transcript "is
  written asynchronously and may lag the in-memory conversation", so the estimate can run a
  turn behind. The interval is approximate by design, and this is within it.
- When several hooks add context for one event, "Claude receives all of the values". The page
  does not say in what order.

Where this departs from the specification:

- **Placement.** Part 4 places the wrapper "in the system prompt, after the host's own
  instructions". A hook cannot do that. "Claude Code wraps the string in a system reminder and
  inserts it into the conversation at the point where the hook fired."
- **Exactness.** Part 4 has a host change nothing in the text. Claude Code adds its own
  framing around a hook's string, and if the string contains a `<system-reminder>` tag,
  "Claude receives the string with that tag's `<` replaced by `&lt;`". A body may contain that
  tag, since the standard reserves only its own.
- **A reminder can be lost.** A `UserPromptSubmit` hook that reaches its timeout "is canceled
  and its output, including any `additionalContext`, is discarded. The prompt still reaches
  Claude without that context."
- **`UserPromptSubmit` is not only the user.** It also fires for a scheduled task, a
  background subagent reporting back, and a message from another session. Part 5 defines the
  boundary as what the user sends.
- **Order with several value systems.** Part 10 puts the preamble first and then the wrappers
  in activation order. Since the order in which several hooks' outputs arrive is not
  documented, an adapter cannot promise it without testing.

#### A forced output style

A plugin can ship an output style in `output-styles/` and force it on. `force-for-plugin` is
"Plugin output styles only. Set to `true` to apply this style automatically whenever the
plugin is enabled, without requiring users to select it." An output style "changes the
instructions Claude Code gives Claude", and "Claude Code sends the active style's instructions
with every request." The style's text would be the rendered wrapper.

This puts the wrapper with Claude Code's instructions, which is nearer to part 4 than a hook
gets. The page does not say where in those instructions a style's text is placed. The costs:

- **No reminder.** A style is fixed text. Nothing is placed in the conversation as it grows.
  The style's text is sent with every request, and whether that is enough to prevent prompt
  fade was not tested.
- **One at a time.** "If multiple enabled plugins set this, Claude Code uses the first one
  loaded." Two value systems cannot both be active this way.
- **It overrides the user.** A forced style "Overrides the user's `outputStyle` setting."
- **It changes Claude Code.** A custom style leaves out "Claude Code's section of built-in
  software engineering instructions" unless `keep-coding-instructions` is `true`, and the page
  says that field has no effect on the shorter system prompt.
- **A generated file.** The style file holds the wrapper already rendered. It is made from
  `VALUES.md` and has to be made again whenever `VALUES.md` changes. A stale style file is a
  different value system from the one the package states.

The two can be combined: a style for the wrapper and a `UserPromptSubmit` hook for the
reminder.

### The hook size cap

**Documented**, from the hooks reference: "A hook's `additionalContext`, `systemMessage`, and
`initialUserMessage` strings, and its plain stdout, are capped at 10,000 characters". Two
details matter here.

- **Each string is measured alone.** "Claude Code measures each string on its own, even when
  several hooks run for the same event."
- **Over the cap, the text is replaced, not shortened in place.** "Claude Code saves the
  output to a file in the session directory. It replaces the output with the file path and a
  preview of up to the first 2,000 characters." And "Claude Code doesn't ask Claude to read
  the file".

The budget, from the limits in parts 2 and 3 of the specification and the three files in
[`prompts/`](prompts/):

| Text | Fixed characters | Largest variable part | Largest rendering |
|---|---|---|---|
| Wrapper | 1,504 | Name, 64, twice. Steward name, 100, three times. Body, 7,500. That is 7,928 | 9,432 |
| Reminder | 149 | Name, 64, twice. Core, 1,500. That is 1,628 | 1,777 |
| Preamble | 414 | The names, each at most 64, joined by a comma and a space | 544 for two names |

The largest wrapper any valid package can render to is 9,432 characters, which is 568 under
the cap. The body limit of 7,500 characters was set to make this so
([`rationale.md`](rationale.md)).

What an adapter does with this:

- **One hook output for each text.** Because each string is measured alone, an adapter emits
  each package's wrapper as its own hook output, and the preamble as one more. It does not
  join them into a single string. Three wrappers in one string could come to 28,296
  characters.
- **Refuse on overflow.** If a rendered text would still exceed the cap, the adapter stops
  with an error that names the package and the sizes. It does not truncate, and it does not
  let Claude Code replace the text. A replaced wrapper would give the model the first 2,000
  characters: the opening, the seven rules, and no more than the first few hundred characters
  of the value system's own words.

A rendered text can exceed the cap in two cases. The first is a preamble naming 146 or more
packages with names of full length. The second is a matter of units. The standard counts
characters as Unicode code points. The hooks reference does not say what it counts. If Claude
Code counts UTF-16 code units, a character outside the Basic Multilingual Plane counts as two,
and a long body written in such characters could be valid and still render to more than 10,000
units. This was not tested.

### A Claude Code marketplace

A Claude Code marketplace is a catalogue file, `.claude-plugin/marketplace.json`, that lists
plugins and says where each one is. Part 12 of the specification gives the mapping from a
package's frontmatter to a marketplace entry, and the checker's `marketplace` command applies
it to a collection.

- **Documented.** "`name`, `owner`, and `plugins` are required" in the file, and in each entry
  "`name` and `source` are required". A relative `source` "Must start with `./`" and is
  resolved from the marketplace root, the directory that contains `.claude-plugin/`.
  ([marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference.md))
- **Documented.** A listed folder needs no manifest of its own. With "No `plugin.json`: the
  entry is the manifest". (same page)
- **Observed.** A marketplace file built from the command's entries passes
  `claude plugin validate`, and `example-islam` and `example-roman-catholic` both installed
  from it, with no `plugin.json` in their folders.

This is the file for the four packages in [`../values/`](../values/), for a marketplace at the
root of this repository. Its `plugins` list is exactly what this command printed on
2026-11-21:

```
uv run --project spec/checker python -m values_checker marketplace values/ --root .
```

The `name` and `owner` are chosen by whoever publishes the marketplace. The ones here are
examples.

```json
{
  "name": "values-md",
  "owner": {
    "name": "The values.md project"
  },
  "plugins": [
    {
      "name": "example-islam",
      "source": "./values/example-islam",
      "description": "An illustrative example, not endorsed by any religious authority. It answers questions about Islam from within the Sunni tradition, keeps its own statements to the basics, and sends rulings, verses of the Qur'an and hadith to the Ansari tool. Vouched for by The values.md project (organization).",
      "version": "0.1.0",
      "author": {
        "name": "The values.md project",
        "url": "https://github.com/faithfamilytechnologynetwork/values.md"
      },
      "license": "MIT",
      "category": "Islam",
      "tags": [
        "Islam",
        "Sunni",
        "en",
        "example"
      ]
    },
    {
      "name": "example-principled-pluralism",
      "source": "./values/example-principled-pluralism",
      "description": "An illustrative example, not endorsed by its author. A way of answering questions about religion, taken from Michael Graham's essay \"My Manifesto on AI and Religion\". A basic question about a religion is answered from that religion's own vantage point, and other perspectives are offered at the close. Vouched for by The values.md project (organization).",
      "version": "0.1.0",
      "author": {
        "name": "The values.md project",
        "url": "https://github.com/faithfamilytechnologynetwork/values.md"
      },
      "license": "MIT",
      "tags": [
        "en",
        "example",
        "religion"
      ]
    },
    {
      "name": "example-roman-catholic",
      "source": "./values/example-roman-catholic",
      "description": "An illustrative example, not endorsed by any religious authority. It answers questions about the Catholic faith from within Roman Catholic teaching, keeps its own statements to the basics, and takes detail from a bundled public-domain catechism. Vouched for by The values.md project (organization).",
      "version": "0.1.0",
      "author": {
        "name": "The values.md project",
        "url": "https://github.com/faithfamilytechnologynetwork/values.md"
      },
      "license": "MIT",
      "category": "Christianity",
      "tags": [
        "Christianity",
        "Roman Catholic",
        "en",
        "example"
      ]
    },
    {
      "name": "plain-speaking",
      "source": "./values/plain-speaking",
      "description": "One person's rules for honest, direct advice. Vouched for by Sam Example (individual).",
      "author": {
        "name": "Sam Example"
      }
    }
  ]
}
```

**Observed:** this file, saved as `.claude-plugin/marketplace.json` beside a copy of
`values/`, passes `claude plugin validate` with one warning, that the marketplace has no
`description`. This repository does not ship the file. Publishing a marketplace belongs to
whoever runs the collection.

Two of the four packages are a `VALUES.md` and nothing Claude Code reads. Listed as plugins
they have no skills and no servers, so installing them gives Claude Code nothing until a
prompt adapter is present. Installing those two was not tried.

#### What the install screen shows

The standard asks a host to show the steward, the kind of claim and where the package came
from, at install and afterwards (part 9). A marketplace entry has no field for the kind of
claim. The mapping therefore ends each description with a fixed sentence, `Vouched for by
{steward.name} ({steward.claim}).`

- **Documented.** `description` is "Shown in `/plugin` listings and details", and
  `description`, `author` and `license` are among the display fields users see "in plugin
  listings and details, before and after install".
- **Not checked.** The install screen itself was not looked at. The installs observed above
  were made from the command line.

So in Claude Code a user sees the kind of claim only as words inside the description. The
steward's name also appears as the entry's `author`, a label that does not say the steward
vouches for anything. Nothing marks either as a claim that has not been verified. This is
weaker than what part 9 asks of a host, and an adapter cannot repair it, because the screen is
Claude Code's own.

#### Hooks in a marketplace entry

**Documented:** an entry "also accepts every `plugin.json` field", `hooks` among them, written
as "an inline object that maps hook event names to matcher arrays" (marketplace reference).
When the folder has no `plugin.json`, the entry's hooks load "only in the inline object form"
(plugin manifest reference).

This gives a collection one place to attach the prompt adapter for every package it lists:
the same two hooks, written inline in each entry, with no file added to any package. The hooks
reference documents a `${CLAUDE_PLUGIN_ROOT}` placeholder for a plugin's own folder, which is
how such a hook would find the package's `VALUES.md`. Hooks declared in a marketplace entry
were not tried for this note.

## A host that only reads Agent Skills

Such a host gets the folders under `skills/`. Validity rule V8 requires each to be a valid
Agent Skill by that standard's own rules, so they load as they are. A user copies them to
wherever the host looks for skills.

The host gets nothing always on. An
[Agent Skill](https://agentskills.io/specification) is loaded progressively: its name and
description at startup, and its body "when the skill is activated". So the model sees a
skill's description and opens the skill when a task matches. It never sees the body of
`VALUES.md`, the wrapper or a reminder, and it is not told that a value system is installed or
who vouches for it.

A package's skills are written as depth behind its prompt. The catechism skill in
`example-roman-catholic`, for instance, finds an answer in a bundled text. Without the body it
still does that, and nothing tells the model to answer from within the tradition or to use
the skill in preference to its own memory.

Copying the body into a skill of its own would not make it always on, for the same reason. It
would be read only when the model decided a task called for it.

## A host that only reads AGENTS.md

Such a host gets nothing from a package automatically. It does not look for `VALUES.md`, and
[AGENTS.md](https://agents.md/) has no way to refer to one.

A user can paste the body into an `AGENTS.md` file by hand. That gives the model the body
once, as part of the instructions, and none of the rest:

- no wrapper, so nothing tells the model that the text comes from a third party, who vouches
  for it, or that it does not override the host's rules;
- no reminder, so nothing addresses prompt fade;
- no tools, unless the host has its own way to connect an MCP server and the user sets that up
  separately;
- no display of the steward or the claim.

It also changes how the value system is activated. An `AGENTS.md` file applies by position:
"The closest AGENTS.md to the edited file wins". A body pasted into one applies to everyone
who opens that directory with such a host, which is the ambient discovery the standard rules
out (part 8). It is a reasonable thing for a person to do in their own directory, and not a
way to distribute a value system.

## Sources

Each page was read on 2026-11-21 (UTC).

| Subject | Source |
|---|---|
| Claude Code plugin manifest reference | https://code.claude.com/docs/en/plugins-reference.md |
| Claude Code marketplace reference | https://code.claude.com/docs/en/plugins/marketplace-reference.md |
| Claude Code hooks reference | https://code.claude.com/docs/en/hooks.md |
| Claude Code output styles | https://code.claude.com/docs/en/output-styles.md |
| Agent Skills specification | https://agentskills.io/specification |
| AGENTS.md | https://agents.md/ |
