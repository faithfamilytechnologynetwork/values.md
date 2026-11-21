# example-roman-catholic

**An illustrative example. It is not endorsed by any religious authority.** The values.md
project wrote this package to show the format. No bishop, priest or Catholic body has
reviewed it, and it speaks for nobody.

## What it is

A value system that answers questions about the Catholic faith from within Roman Catholic
teaching. Its own statements are kept to basics. Detail comes from a bundled public-domain
catechism, and for the Church's present wording the package points to the current Catechism
of the Catholic Church, which is under copyright and is not bundled.

## What is in the package

| File | Purpose |
|---|---|
| `VALUES.md` | The value system. The section headed "Core" is what a host reinjects. |
| `skills/catechism-answers/SKILL.md` | A skill that answers basic questions from the bundled catechism. |
| `skills/catechism-answers/references/baltimore-catechism-no-2.md` | The Baltimore Catechism No. 2, approved in 1885. |
| `references/apostles-creed.md` | The Apostles' Creed, in the catechism's wording. |
| `references/sources.md` | Every source, its status, and how the package's statements were checked. |

There is no tool server and no model. A search on 2026-11-20 found no Catholic tool server
with clear standing, and no fine-tuned model exists.

The skill carries its own copy of the catechism, so it still works when its folder is copied
somewhere else on its own. A host that reads only `VALUES.md` gets the basics and is told
plainly where the detail lives.

## The bundled texts

Both bundled texts are in the public domain. Each file states its source and the basis for
that at its top or its foot, and `references/sources.md` gathers them.

The catechism is a text of 1885, taken from a transcription of a 1977 printing. Three
answers whose wording in that printing is later than 1885 are left out, and the file says
which. The package tells the model to treat the catechism as a text of its time: to use
today's names, and not to give an old rule of practice as the present one.

## Checking it

From the root of the repository:

```
uv run --project spec/checker python -m values_checker check values/example-roman-catholic
uv run --project spec/checker python -m values_checker render values/example-roman-catholic
```

## Licence

The package's own text is under the MIT licence (see `LICENSE` at the root of the
repository). The bundled catechism and creed are in the public domain.
