# Rationale for the values.md standard, version 0.1

This document records why the format in [`specification.md`](specification.md) has the shape
it has: what already existed, the four shapes that were considered, why one was chosen, and
the reasoning behind the main decisions inside it. It is not normative. Where it and the
specification differ, the specification is right.

This text is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Every statement here about another format gives a link to its source. Each of those pages was
read on 2026-11-21 (UTC), and the statements describe what the pages said on that day. The
other formats will change. The links are listed again under [Sources](#sources).

## The problem, and the test for a solution

Most questions about faith and values are put to general-purpose assistants, not to assistants
built for one tradition. A person who wants answers grounded in their own tradition can open a
separate, purpose-built assistant, or paste a prompt into a general one and hope it holds. The
first reaches few people. The second gives no sources, no statement of who vouches for the
text, and no protection against the prompt losing force as the conversation grows.

So the format has to be something a general assistant can adopt, and the cost of adopting it
decides how far it reaches. That gives one test, applied to every decision below: **can a host
support the simplest package by reading one file, substituting three placeholders and counting
tokens, with no new dependency?** A second test came with it: the smallest package an author
can write should be a few lines of frontmatter and ordinary prose.

## What already existed

Four existing formats each cover part of the need. None covers all of it.

| Format | What it carries | Always on? | Tools | Who vouches | What it lacks for this purpose |
|---|---|---|---|---|---|
| AGENTS.md | Free-form instructions for a code repository | Yes | No | Not stated | Metadata of any kind, tools, a way to stay in force, and any defence against a file that arrives with a repository |
| Agent Skills | A procedure, with files beside it | No. Loaded when a task calls for it | Scripts inside the skill | Not stated | An always-on part, and room for new fields |
| Claude Code plugins | Skills, MCP servers, hooks and more, for one product | Only through an output style or a hook | Yes, through `.mcp.json` | An `author` field | A prompt component that other hosts can read |
| Belief Protocol | The beliefs themselves, in a typed structure | Yes | No | An `author` field | Tools, models, a text for the host to put around the content, and reinjection |

### AGENTS.md

[AGENTS.md](https://agents.md/) is plain Markdown. Its page answers "Are there required
fields?" with "No. AGENTS.md is just standard Markdown." A file applies by position: "The
closest AGENTS.md to the edited file wins; explicit user chat prompts override everything."
The page says nothing about frontmatter, tools, models or versions.

Two things were taken from it: the upper-case file name at a known place, and the idea that
the simplest form of the format is a single file of prose. One thing was deliberately not
taken: discovery by position. A file that applies because it is nearby suits instructions for
a code repository. For a value system it would mean that cloning a repository could change an
assistant's values. See [Discovery](#discovery) below.

### Agent Skills

An [Agent Skill](https://agentskills.io/specification) is a folder with a `SKILL.md`. Its
frontmatter has six fields: `name`, `description`, `license`, `compatibility`, `metadata` ("a
map from string keys to string values") and `allowed-tools`, which is marked experimental. A
skill is loaded progressively: "The `name` and `description` fields are loaded at startup for
all skills", and "The full `SKILL.md` body is loaded when the skill is activated".

Three things were taken from it. The rules for `name` are the same, so a package name and a
skill name look alike. Multiword keys use hyphens. And `skills/` in a package holds Agent
Skills exactly as that standard defines them, with nothing added.

A value system could not simply be a skill, for the reasons given under
[option 2](#option-2-a-superset-of-an-agent-skill).

### Claude Code plugins

A [Claude Code plugin](https://code.claude.com/docs/en/plugins-reference.md) is a folder whose
components sit at known places under its root: `skills/`, `commands/`, `agents/`,
`hooks/hooks.json`, `.mcp.json`, `output-styles/` and others. The manifest,
`.claude-plugin/plugin.json`, is optional: "Without it, Claude Code loads the components it
finds in the standard layout."

The layout was taken from it. A package folder puts `skills/` and `.mcp.json` where a plugin
puts them, so the same folder can be loaded as a plugin. What a plugin does not have is a
place for an always-on prompt that another product can read. The page says that "A `CLAUDE.md`
at the plugin root isn't loaded as context", and the two routes that do reach the model's
context, an output style and a hook, are Claude Code's own.
[`compatibility.md`](compatibility.md) describes both.

### The Model Context Protocol

[MCP](https://modelcontextprotocol.io/) describes itself as "an open-source standard for
connecting AI applications to external systems". It is used here unchanged, as the way a
package declares its tools. See [Tools and conformance levels](#tools-and-conformance-levels).

### Belief Protocol

[Belief Protocol](https://github.com/MikeyAnderson/belief-protocol) (`BELIEF.md`, version 2.2,
Apache-2.0) is the nearest neighbour, and it solves a different problem. It is a schema for
the beliefs themselves. Its README defines ten structure types (`worldview`, `web`,
`decision-surface`, `plausibility`, `formation`, `narrative`, `dissonance`, `boundary`,
`tripwire` and `deep-structure`) and says that "Every individual belief inside any structure
carries `layer`, `grip` and `warrant`, and records a `source`." A belief file is "loaded at
session start and remain[s] active throughout", and its "Agent Orientations" section, of about
200 to 500 tokens, is "Held in active context throughout". The README calls the format
"complementary to Agent Skills".

It has nothing for tools or fine-tuned models, fixes no text for a host to put around the
content, and does not say how the content is kept in force over a long conversation. Those are
what this standard is about. This standard, in turn, says nothing about how beliefs are
structured: the body of a `VALUES.md` is ordinary prose.

The two fit together. A body may be written to Belief Protocol's structure, and because the
name of the core section is configurable, such a body can name its "Agent Orientations"
section as the part to be reinjected.

They differ most in what the smallest file asks of its author. The README's own list of
requirements for a `BELIEF.md` includes a `decision-surface` structure, "present as `## Agent
Orientations`, non-empty", and that "Every belief carries `layer`, `grip`, and `warrant`". The
smallest valid `VALUES.md` is three frontmatter fields and a paragraph, and it is shown in full
at the top of the specification. This is a difference of purpose and not a criticism. A typed
schema lets two belief files be compared belief by belief. This standard gives that up in
exchange for a file that anyone can write and any host can load.

## The four options

### Option 1: A single file only

`VALUES.md` and nothing else, in the manner of AGENTS.md.

- For: the cheapest thing to adopt and the easiest to write.
- Against: no place for tools or bundled sources. A tradition's answers depend on citing its
  texts accurately, and a prompt alone leaves the model to recall them from memory.
- Risk: low to build, and high that answers are unsourced.

### Option 2: A superset of an Agent Skill

A skill with extra frontmatter fields for values, models and persistence.

- For: it reuses an existing loader and an existing way of distributing packages.
- Against, first: a skill is loaded when a task calls for it, and a value system has to be in
  force all the time.
- Against, second: the frontmatter is a closed list. The Agent Skills project's reference
  validator
  [refuses any field outside the six](https://github.com/agentskills/agentskills/blob/83021e2/skills-ref/src/skills_ref/validator.py),
  with the message "Unexpected fields in frontmatter". The
  [guide for client authors](https://agentskills.io/client-implementation/adding-skills-support)
  recommends lenient loading for some faults and does not mention unknown fields, so what a
  given client does with one is not defined. New fields in `SKILL.md` would therefore fail the
  standard's own validator and behave unpredictably elsewhere.
- Against, third: the one extension point, `metadata`, holds strings only. A list of models,
  each with several fields, does not fit in it.
- Risk: medium. The format would be at the mercy of another standard's validators.

### Option 3: A plugin-shaped folder with `VALUES.md` (chosen)

A single file that stands alone, and an optional folder around it that reuses `.mcp.json`,
`skills/` and `references/`.

- For: one new file. Every other part is a format that hosts already read. The single file
  gives the low floor of option 1, and the folder gives the tools and depth that option 1
  lacks. Because the folder is laid out like a Claude Code plugin, it can be loaded as one.
- Against: the layout follows one vendor's convention. A full implementation has two other
  formats to support, MCP and Agent Skills.
- Risk: medium to low. The main one is that hosts stop at the simplest level.

### Option 4: A new manifest from scratch

A purpose-built manifest that declares prompt, tools, skills and models in its own vocabulary.

- For: no inherited constraints, and one coherent design.
- Against: every host needs a new loader for every part, and nothing that exists can be
  reused. For a format whose purpose is reach, that cost defeats it.
- Risk: high that nobody adopts it.

### Why option 3

Option 3 is the only one that passes the test at both ends. A host that wants the least work
supports the single file, which is option 1. A community that needs its sources adds a folder,
and each thing in the folder is something a host may already be able to load: an MCP client
reads `.mcp.json`, a skill loader reads `skills/`. Nothing in the folder is a new format.

The two points against it are met as follows. The vendor's layout is used only where it is
already shared between products: `.mcp.json` with an `mcpServers` key, and Agent Skills. A
host other than Claude Code never has to read a Claude Code manifest. And the cost of a full
implementation is spread over three conformance levels, so that supporting the single file is
a complete and conforming thing to do.

## Decisions inside option 3

### The prompt is the whole body, and the core is a named section

The whole Markdown body is the always-on prompt. The core, the part that is reinjected, is the
section under a second-level heading named `Core`, or under another heading the package names.
A body of 1,500 characters or fewer needs no core section and is its own core.

An author therefore writes an ordinary document, and a short one needs no marking at all.
Because the heading's name is configurable, a body in another language can use its own word
for it.

Two alternatives were set aside. A core given as a frontmatter string puts prose into YAML and
takes it out of the document a person reads. HTML comment markers around the core are
invisible when the file is rendered and easy to break when it is edited.

The specification fixes how the file is read in some detail: line endings, how characters are
counted, what counts as a heading, how a code fence closes. The detail is there so that two
hosts written independently get the same prompt and the same core from the same bytes. Without
it, "the same package behaves the same everywhere" would not hold.

### Only the core is reinjected

A reminder carries the core, capped at 1,500 characters, and never the whole body unless the
body is short enough to be its own core.

The reason is cost. The figures below take four characters to a token, the default interval of
5,000 tokens and a name of 13 characters, and they include the reminder's own fixed text of
149 characters.

| What a reminder would carry | Tokens in each reminder | Added to the conversation | Reminder tokens after 100,000 tokens of conversation, if every reminder is kept |
|---|---|---|---|
| A typical core of 1,000 characters | about 290 | about 6% | about 5,800 |
| The largest core, 1,500 characters | about 420 | about 8% | about 8,400 |
| A whole body of 4,000 characters | about 1,040 | about 21% | about 20,800 |
| The largest body, 7,500 characters | about 1,920 | about 38% | about 38,400 |

Reinjecting the whole prompt would cost a host between a fifth and two fifths more for every
long conversation. A host that will not pay that will not adopt the format. A core costs
between 6 and 8 percent, and a host may drop older reminders and keep the latest.

A reminder with no content, a fixed line saying only that a value system is installed, was
also set aside. It restates that a value system exists without restating what it says, and
what it says is the part that fades.

The interval of 5,000 tokens is a design parameter. It was chosen as a round figure that keeps
the cost above in single digits, and a package may change it. No measurement of how quickly a
prompt of this kind fades is cited here, because none was found that could be checked. A host
or an author with evidence for another figure can set one.

A package cannot turn reinjection off. On a model the package has no fine-tune for, the
reminder is the only thing that addresses prompt fade.

### The reminder goes with the next user message, and tokens are counted, not turns

The reminder is placed at the start of the next user message after the count reaches the
interval. Placing it there keeps it next to the newest turn, where fade is worst, and leaves
everything earlier in the conversation untouched, so a host's prompt cache stays valid.

Rewriting the system prompt from time to time was set aside: many APIs fix the system prompt
for the whole conversation, and changing it invalidates the cache. Counting user turns was set
aside because turns vary too much in length to stand in for tokens. One tool result can be
longer than fifty turns of chat.

The count is approximate by design. A host with no tokenizer counts characters and divides by
four. Two hosts that count a little differently both conform, because nothing depends on the
reminder falling at an exact token.

### The body limit and the size of a rendered wrapper

The body is at most 7,500 characters. The limit was set from the outside in. The wrapper's
fixed text is 1,504 characters. With the longest name, the longest steward name and the
longest body, a rendered wrapper is 9,432 characters. That is under 10,000 characters, which
is the cap Claude Code puts on a string a hook adds to the model's context:
"A hook's `additionalContext`, `systemMessage`, and `initialUserMessage` strings, and its
plain stdout, are capped at 10,000 characters"
([hooks reference](https://code.claude.com/docs/en/hooks.md)). A hook is one of the two ways
to supply the prompt in Claude Code, and the only one that can also place the reminder
([`compatibility.md`](compatibility.md)). A limit that let a valid package exceed the cap
would have made some valid packages unusable there. The 568 characters to spare leave room for
the wrapper's wording to change in a later version.

The limit also stands on its own. A prompt of 7,500 characters is roughly 1,900 tokens held in
every request for the length of every conversation, and a value system that needs more than
that has `skills/` and `references/` for the rest.

A file over a limit is refused and never truncated. A truncated value system is a different
value system, and nobody vouched for it.

### What the wrapper says, and why

The wrapper is the text a host puts around the body. It is fixed, word for word, so that the
same package is introduced to the model the same way in every host. Its rules are what a host
owes any installed value system, whatever that value system says. None of them is taken from a
particular value system, and none favours one.

The opening lines say that a value system is installed, who vouches for it, and that the text
which follows "was not written by the user or by the maker of this assistant". A model should
know whose words it is reading.

1. **Answer from inside the value system, and as fully as any other question.** This is what
   the user installed it for. Without the rule, the usual result is a short survey of every
   viewpoint, which serves nobody who asked from within a tradition.
2. **Where the value system holds more than one accepted position, present each.** Otherwise
   the model picks one, and a choice the tradition itself has not made is presented as the
   tradition's answer.
3. **Use the provided tools and texts for specifics, never invent a source, and say when a
   tool or text cannot be reached.** Quotations and rulings are where a model's memory is
   least reliable and where a mistake does most harm. The last clause matters on a host that
   supports only the prompt: the body may point at a tool the host never connected, and the
   user should be told so and not given a guess.
4. **The model is not an authority and does not speak for the steward.** A package describes
   a value system. It does not make the assistant a member of the clergy or of a profession.
5. **The user may always ask for another view, a comparison or a critique.** Installing a
   value system changes the default vantage point. It does not close off the others, and the
   model says which statements come from the value system and which do not.
6. **Say what is installed when asked.** A user must be able to find out what is shaping the
   answers. This backs up the host's own display.
7. **Elsewhere, behave as usual, and override nothing.** The wrapper comes after the host's
   own instructions and says that it does not outrank them. A package is third-party text and
   gets no standing above the host's rules.

The texts are in English in this version, whatever language the body is in. Translating them
is left for later, since each translation would have to be fixed word for word in the same
way.

The body may not contain the tags the three texts use. This keeps a body from closing its own
wrapper or forging a reminder by accident. It is not a defence against a hostile body, which
can say anything in plain prose. The security section of the specification deals with that.

### A fine-tuned model declares how it relates to the prompt

A package may declare fine-tuned models. Each entry carries a `prompt` field with three
values: `required`, `optional` and `omit`. The package says which the model supports, and the
user or operator chooses within that.

Whether a model can carry a value system with no prompt in context depends on how it was
trained and tested, and only the people who made it know. So the package declares it. The
default is `required`, so that a model about which nothing is said keeps the prompt.

The alternatives:

- A fixed rule that a model may replace reinjection and nothing else. It rules out a model
  trained to stand on its own.
- Leaving the choice to the host. A host cannot tell from outside whether a set of weights was
  trained to carry the value system unaided.
- A yes-or-no field. It cannot tell "works either way" from "must not have the prompt on
  top", and the second is a real case: a model trained with no system prompt and never tested
  with one.
- A short fixed notice injected in place of the wrapper when the prompt is left out, so that
  the model could still say what is installed. The model would then never truly stand alone.
  The host's own display carries disclosure instead, and the specification requires it in
  every mode.

A host never switches to a declared model on its own and never drops the prompt unasked. A
model's behaviour without the prompt rests on weights nobody can read, and that is a choice
for the person who bears the result.

An entry matches only when the host is using the same provider and exactly the named base
model. There is no nearest match, because weights trained from one base model are not known to
work on another.

A package may declare only a model that anyone with access to the provider can load. A field
marking a model as restricted was considered and dropped: it would let a package advertise
something most people who install it could not use.

### Tools and conformance levels

A package declares tools as MCP servers in `.mcp.json`. A host with no file system and no
shell can still be an MCP client, so this is the route by which a plain chat loop reaches a
package's tools.

Requiring every host to support skills was set aside, because a skill may need a file system
or a shell and a chat product has neither. Declaring tools as function schemas in the
frontmatter was set aside too: it would be a second tool format, and it leaves nowhere for the
tool to run.

The three levels (prompt; prompt and remote tools; the whole folder) let a host stop where its
abilities stop and still conform. The cost is that a host at the first level does not connect
the tools. Two things soften this. Authors are told to put anything essential in the body.
And rule 3 of the wrapper makes the model say when a tool it was pointed to is not there.

Installing a package authorises nothing it declares. A connection to a server sends the
user's questions to a third party, and a local command runs code, so each needs its own
consent. `headers` is not allowed in a package's `.mcp.json`, because the only use for it in a
published file is a credential.

### Discovery

A value system becomes active only when a user or operator installs it. A host that finds a
`VALUES.md` in a working directory may offer to install it and may not activate it.

This is the one place where the format deliberately departs from AGENTS.md. A value system
belongs to a person or an operator, not to a directory. If the nearest file applied
automatically, any repository, download or archive could change an assistant's values by
containing a file, which is a route for prompt injection.

### More than one value system

A host must support one active value system and may support several. When several are active
they are kept separate. Where they differ, the model says so and attributes each position.

Allowing exactly one, always, would be simpler, and it rules out a real case: a person can
hold a faith and a professional code together. Letting a package declare its own precedence
was set aside because every package would rank itself first. Only the user can say which
takes precedence.

### Three required fields, and a steward who states a claim

`name`, `description` and `steward` are required. Agent Skills requires the first two. The
third is added because a value system that nobody vouches for is the one thing that should
not install quietly, and because the wrapper names the steward. With `steward` optional, the
wrapper would need two forms.

`steward.claim` is required and has three values: `individual`, `organization` and `official`.
Making it required means that nobody acquires a claim by leaving a field out, and a listing
never has to guess. A free-text statement was set aside because a listing cannot filter on it
and a check cannot test it. Making it optional with a default of `individual` was set aside
because a collection would then have to require it anyway.

The standard cannot verify a claim in this version, and it says so wherever the claim appears.
What it does is make the claim visible: the host shows the steward, the kind of claim and
where the package came from. For the two stronger claims a URL is required, so that there is
somewhere to check. Mechanical verification, through a well-known URL or a signature, is left
for a later version.

### Fields for a listing

`tradition`, `languages` and `tags` are separate fields so that a browser of packages can
build a filter from each. `tradition` is a list from broad to narrow, which handles several
packages within one tradition: schools, denominations and so on. One flat list of tags could
not tell a tradition from a language from a keyword. Encoding them in the name, as in
`islam-sunni-en`, would make names into a schema.

`metadata` holds any JSON value, where Agent Skills allows strings only. That lets a
collection add structured fields of its own without a new version of the standard.

An unknown key at the top level is ignored, so that a later version can add a field without
breaking a host written for this one. An unknown key inside `steward`, `persistence` or a
model entry makes the file invalid, so that a misspelled `claim` or `prompt` does not pass
silently.

### What "valid" means

Validity is a numbered list of rules decided from the package's files alone, with a set of
fixtures that label the expected result for each. A host at install and a collection checking
a submission therefore reach the same answer, and the check runs with no network, no account
and no model.

The schema alone would not do. It cannot see the limits on the body, the core section, or the
other files in the folder. Whether a declared tool answers and whether a declared model loads
were left out on purpose. A check that depends on them fails when a server is briefly down,
and it needs credentials to run. A collection can add them as checks of its own.

## What is left for later versions

- Verifying a steward's claim mechanically.
- Translations of the wrapper, the reminder and the preamble.
- How a single package is distributed outside a collection: an archive, a URL.
- Evidence for the reinjection interval, and for how well the wrapper's wording holds on
  different models. Both need hosts that run the format.

## Sources

Each page was read on 2026-11-21 (UTC).

| Subject | Source |
|---|---|
| AGENTS.md | https://agents.md/ |
| Agent Skills specification | https://agentskills.io/specification |
| Agent Skills, guide for client authors | https://agentskills.io/client-implementation/adding-skills-support |
| Agent Skills reference validator, at commit `83021e2` | https://github.com/agentskills/agentskills/blob/83021e2/skills-ref/src/skills_ref/validator.py |
| Claude Code plugin manifest reference | https://code.claude.com/docs/en/plugins-reference.md |
| Claude Code hooks reference | https://code.claude.com/docs/en/hooks.md |
| Model Context Protocol | https://modelcontextprotocol.io/ |
| Belief Protocol, README at the default branch | https://github.com/MikeyAnderson/belief-protocol |
