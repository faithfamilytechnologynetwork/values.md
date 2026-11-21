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

`VALUES.md` and nothing else. It is the smallest kind of package: no tools, no skills, no
bundled texts and no model. Its body is short enough to be its own core, so the whole body
is what a host reinjects.

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
