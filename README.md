# values.md

values.md is an open standard for handing an AI assistant a **value system**: a body of
values that a person or a community wants the assistant to answer from, such as a faith
tradition, a professional code or a family's house rules. A value system is written once, as a
`VALUES.md` file, and any assistant that follows the standard installs it the same way. The
standard fixes the text the assistant puts around the file in a conversation, how that text is
kept in force as the conversation grows, and how a user can see what is installed and who
vouches for it. A package can also carry tools, on-demand skills and bundled texts in a folder
around the file. This is version 0.1.

## The smallest valid file

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

Three frontmatter fields and a body in ordinary prose. Everything else in the standard is
optional for an author.

## Where things are

| Path | What it is |
|---|---|
| [`spec/specification.md`](spec/specification.md) | The standard. Start here. |
| [`spec/rationale.md`](spec/rationale.md) | Why the format has this shape, and how it compares with AGENTS.md, Agent Skills, Claude Code plugins and Belief Protocol. |
| [`spec/compatibility.md`](spec/compatibility.md) | What Claude Code, a host that only reads Agent Skills and a host that only reads AGENTS.md get from a package today. |
| [`spec/`](spec/) | Also the schemas, the three texts a host injects, and the fixtures. [`spec/README.md`](spec/README.md) is the index. |
| [`values/`](values/) | The collection of value systems, one folder each. The first four are examples: [`plain-speaking`](values/plain-speaking/), [`example-principled-pluralism`](values/example-principled-pluralism/), [`example-islam`](values/example-islam/) and [`example-roman-catholic`](values/example-roman-catholic/). The three whose names begin `example-` are illustrations, and each says that it is not endorsed. |
| [`spec/checker/`](spec/checker/) | A small Python program that applies the standard's validity rules to a package. |

## Checking a package

The checker needs [uv](https://docs.astral.sh/uv/). From the root of the repository, give it a
`VALUES.md` file, a package folder, or a collection of package folders:

```
uv run --project spec/checker python -m values_checker check values/
```

It prints `valid`, `invalid` with the rules that failed, or `unsupported version` for each
package. The first run installs the checker's environment, which uses the network. The check
itself does not. [`spec/README.md`](spec/README.md) lists the other commands.

## Licences

The specification, the rationale and the compatibility note are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Everything else in the repository,
including the schemas, the fixtures, the checker and the example packages, is under the MIT
licence. See [`LICENSE`](LICENSE).
