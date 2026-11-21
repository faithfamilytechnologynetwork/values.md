# example-islam

**An illustrative example. It is not endorsed by any religious authority.** The values.md
project wrote this package to show the format. No scholar or Islamic body has reviewed it,
and it speaks for nobody. Ansari is a separate project and has not endorsed it either.

## What it is

A value system that answers questions about Islam from within the Sunni tradition. Its own
statements are kept to basics held across that tradition. Anything more specific, such as a
ruling, a verse of the Qur'an or a hadith, is sent to a tool.

## What is in the package

| File | Purpose |
|---|---|
| `VALUES.md` | The value system. The section headed "Core" is what a host reinjects. |
| `.mcp.json` | Declares one remote tool server, Ansari. |

There are no skills and no bundled texts, so the package works in full on a host that reads
`VALUES.md` and connects remote tools.

## The tool

`.mcp.json` declares the Ansari server at `https://mcp.ansari.chat/mcp`. It needs no key and
offers one tool, `answer_islamic_question`, which takes a question and returns an answer.

- When the tool is used, the user's question is sent to that address. A host asks for consent
  before it first connects, and shows the address when it asks.
- The server answered `initialize` and listed that tool on 2026-11-21 (UTC), which is when
  this package was written. Nothing in the package checks that it still does.
- Its repository is https://github.com/ansari-project/ansari-mcp.

## The model

`VALUES.md` declares one fine-tuned model, served by Tinker:

- It is a LoRA fine-tune of `thinkingmachines/Inkling-2-Small`, in English, trained to be
  good company for a practising Sunni Muslim and not to issue rulings.
- It is declared with `prompt: omit`. It was trained with no system prompt and has not been
  tested with this package's prompt on top of it. A host that runs it therefore runs it
  without the prompt, and only when the user or operator chooses that.
- A host is never required to use it. Without it, a host uses its own model with the prompt
  and reinjects the core.
- Loading the model from an account other than the one that trained it has not been tested
  by this project.

## How the statements were checked

Each statement under "The basics" in `VALUES.md` was put to the Ansari tool on 2026-11-21
(UTC), and the tool confirmed each one: the oneness of God and the finality of the Prophet
Muhammad's prophethood, the Qur'an and the Sunnah as sources, the six articles of faith, the
five pillars, the four Sunni schools of law, and the advice to take a personal question to a
qualified scholar. That is a check against one source. It is not a scholar's review.

## Checking it

From the root of the repository:

```
uv run --project spec/checker python -m values_checker check values/example-islam
uv run --project spec/checker python -m values_checker render values/example-islam
```

## Licence

The package's own text is under the MIT licence (see `LICENSE` at the root of the
repository). The Ansari service and the fine-tuned model are not part of the package and
are not covered by that licence.
