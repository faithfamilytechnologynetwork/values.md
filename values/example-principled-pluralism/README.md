# example-principled-pluralism

**An illustrative example. It is not endorsed by its author.** The values.md project wrote
this package to show the format. Michael Graham, whose essay it draws on, has not endorsed
it, and neither has The Gospel Coalition.

## What it is

A value system about one thing: how an assistant answers a question about a religion. It
puts into the form of instructions the approach set out in:

> Michael Graham, "My Manifesto on AI and Religion", The Gospel Coalition, 21 May 2026.
> https://www.thegospelcoalition.org/article/my-manifesto-on-ai-and-religion/

The essay calls the approach a "principled pluralist framework". In short: a basic question
about a religion, on a point where its adherents are in strong agreement, is answered from
that religion's own vantage point, and the answer says so at the start. The body of the
answer is given to that tradition alone. The close offers the user another tradition's
perspective or a skeptical one. Where the tradition itself holds a variety of views, each is
summarised.

The essay is the source. Where this package and the essay differ, the essay is right and the
package is wrong.

## What is in the package

`VALUES.md` is the whole package. This README is for people and is not read by a host. It
is the smallest kind of package: no tools, no skills, no bundled texts and no model.

The body has no section headed "Core". It is kept under 1,500 characters so that the whole
body is its own core, and the whole body is what a host reinjects. An edit that takes it
over that length needs a core section.

## How the statements were checked

Each instruction in the body was compared with the essay on 2026-11-21 (UTC):

| The body says | The essay says |
|---|---|
| It applies to a basic question on a point of strong agreement | The framework is for basic questions about each world religion where there is strong agreement |
| Open by saying the answer is given from the perspective of the religion's adherents | Its worked example opens that way, for a question about Christianity |
| Give the body of the answer to that tradition alone, at proper length | The body is given exclusively to that tradition, and the example runs to several hundred words |
| Include how the tradition answers skeptical objections | The example's body covers how the tradition addresses skeptical counterarguments |
| Do not rule on whether what the tradition holds is true | The essay sets aside a true-or-false framework, in which the model rules on the merits |
| Do not make a short survey that sets religions side by side as equals | The essay sets aside a plain pluralist framework as too brief and as presenting the options as roughly coequal |
| Close by offering another tradition's perspective or a skeptical one | The example closes with that offer, leaving the direction to the user |
| Where the tradition holds a variety of views, summarise each | The essay says so for questions on which a tradition holds a variety of views |
| Treat every religious tradition this way | The essay speaks of each world religion and of every religious tradition |

The essay was read through a tool that returns short quotations and a summary, not the full
text, so the right-hand column is a paraphrase.

## What it does not cover

The essay does not say what to do with a question that compares religions or that names no
religion. The package adds nothing of its own there.

## Checking it

From the root of the repository:

```
uv run --project spec/checker python -m values_checker check values/example-principled-pluralism
uv run --project spec/checker python -m values_checker render values/example-principled-pluralism
```

## Licence

The package's own text is under the MIT licence (see `LICENSE` at the root of the
repository). The essay is its author's and publisher's, and is cited here, not reproduced.
