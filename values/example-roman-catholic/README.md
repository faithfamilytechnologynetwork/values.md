# example-roman-catholic

**An illustrative example. It is not endorsed by any religious authority.** The values.md
project wrote this package to show the format. No bishop, priest or Catholic body has
reviewed it, and it speaks for nobody.

## What it is

A value system that answers questions about the Catholic faith from within Roman Catholic
teaching. Its own statements are kept to basics. For detail it tells the model to search the
web, to prefer the Holy See's own site for the current Catechism of the Catholic Church, and
to give the paragraph number and the link. The Catechism is under copyright and is not
bundled.

## What is in the package

| File | Purpose |
|---|---|
| `VALUES.md` | The value system. The section headed "Core" is what a host reinjects. |
| `skills/catechism-answers/SKILL.md` | A skill that says how to look a point up in the current Catechism and how to answer from it. It carries no text of its own. |
| `references/apostles-creed.md` | The Apostles' Creed, in an older English wording that is in the public domain. |
| `references/sources.md` | Every source, its status, and how the package's statements were checked. |

There is no tool server and no model. A search on 2026-11-20 found no Catholic tool server
with clear standing, and no fine-tuned model exists.

## What it needs from a host

Web search, or a tool that can open a web page. The standard has no field for asking a host
for either, so the package asks in prose. Where the host has neither, the package tells the
model to say so and to keep to the basics. A host that reads only `VALUES.md` gets the
basics and the same instruction.

## The bundled text

One text is bundled, the Apostles' Creed. It is in the public domain, and its file states its
source and the basis for that. `references/sources.md` lists it with the texts that are
looked up and not bundled.

## Checking it

From the root of the repository:

```
uv run --project spec/checker python -m values_checker check values/example-roman-catholic
uv run --project spec/checker python -m values_checker render values/example-roman-catholic
```

## Licence

The package's own text is under the MIT licence (see `LICENSE` at the root of the
repository). The bundled creed is in the public domain.
