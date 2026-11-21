# The values.md standard

This directory holds version 0.1 of the standard and everything needed to check a package, or
the standard itself, against it.

## What is here

| Path | What it is |
|---|---|
| [`specification.md`](specification.md) | The standard. Start here. It opens with the smallest valid `VALUES.md` and says what a first-time author and a simple host can ignore. |
| [`rationale.md`](rationale.md) | Why the format has this shape: the four shapes considered, the comparison with AGENTS.md, Agent Skills, Claude Code plugins and Belief Protocol, and the reasoning behind the main decisions. Not normative. |
| [`compatibility.md`](compatibility.md) | What Claude Code, a host that only reads Agent Skills and a host that only reads AGENTS.md get from a package today, including the mapping to a Claude Code marketplace. Not normative. |
| [`schema/values.schema.json`](schema/values.schema.json) | JSON Schema (draft 2020-12) for the frontmatter of `VALUES.md`. Validity rule V3. |
| [`schema/mcp.schema.json`](schema/mcp.schema.json) | JSON Schema for the `.mcp.json` a package folder may carry. Validity rule V7. |
| [`prompts/`](prompts/) | The three texts a host injects, each as a file to copy: `wrapper.txt`, `reminder.txt` and `preamble.txt`. |
| [`fixtures/`](fixtures/) | Small packages made to test one thing each. [`fixtures/fixtures.json`](fixtures/fixtures.json) lists every one with the outcome a conforming checker gives. Each valid fixture has an `expected/` directory with the exact wrapper and reminder it renders to. |
| [`checker/`](checker/) | A small Python program that applies the validity and rendering rules. It is the standard testing itself. It is not a loader, it talks to no model, and it makes no network call. |

The example packages are not here. They live once, in the collection at
[`../values/`](../values/).

## Running the checks

The checker needs [uv](https://docs.astral.sh/uv/). Install its environment once, from the
root of the repository. This is the only step that uses the network:

```
uv sync --project spec/checker --locked
```

To check a package, give `check` a `VALUES.md` file, a package folder, or a collection of
package folders:

```
uv run --project spec/checker python -m values_checker check values/
```

It prints, for each package, `valid`, `invalid` with the rules that failed, or `unsupported
version`. Its exit code is 0 when every package is valid, 1 when any is invalid, and 3 when
nothing is invalid but a package targets a version of the standard this checker does not
implement.

To run every check on the standard itself:

```
uv run --project spec/checker python -m values_checker fixtures
uv run --project spec/checker python -m values_checker selftest
uv run --project spec/checker python -m values_checker consistency
uv run --project spec/checker python -m values_checker check values/
```

| Command | What it does |
|---|---|
| `check <path>` | Applies the validity rules to a file, a folder or a collection. |
| `render <package>` | Prints the wrapper and the reminder for a valid package. `--only wrapper` or `--only reminder` prints one of them, exactly as a host would inject it. |
| `marketplace <collection>` | Prints the Claude Code marketplace entries for a collection, by the mapping in part 12 of the specification. `--root` names the directory the marketplace file resolves paths from. |
| `fixtures` | Runs every fixture and compares the result with `fixtures.json`. It renders every valid fixture and compares the text with its `expected/` files. It then audits the fixtures: every rule, every failure the checker can report and every constraint in the two schemas must be the cause of some fixture's failure. The network is blocked while it runs. |
| `consistency` | Checks the documents in this directory against the machine-readable parts. See below. |
| `selftest` | Breaks copies of the fixtures and of the specification on purpose, one way at a time, and confirms that `fixtures` and `consistency` report each break. |

### What `consistency` checks

The documents are the Markdown files in this directory, outside `fixtures/` and `checker/`.
They carry markers, each an HTML comment alone on its line:

| Marker | Placed before | Checked against |
|---|---|---|
| `values-md:field-table` | The table of frontmatter fields | `schema/values.schema.json`, in both directions: every field, whether it is required, and its type and limits |
| `values-md:rule-table` | The table of validity rules | The rules the checker implements, by identifier |
| `values-md:smallest-file` | The fenced block showing the smallest valid file | `../values/plain-speaking/VALUES.md` |
| `values-md:rendering <path>` | A fenced block showing what a fixture renders to | The file at `<path>` under `fixtures/` |

The first three appear exactly once, in `specification.md`. A fenced block that opens with one
of the tags of the injected prompt, and carries no `rendering` marker, must be identical to
its file in `prompts/`. A marker that is missing, repeated or unknown is an error, and so is a
marked table with no rows.

### Limits of the checker

- Rule V8 applies the Agent Skills rules as that project's reference validator, `skills-ref`,
  applied them at commit `83021e2` of
  [agentskills/agentskills](https://github.com/agentskills/agentskills). There is one known
  difference: the reference refuses flow-style YAML lists and mappings in a `SKILL.md`, which
  the Agent Skills specification does not ask for, and this checker accepts them.
- A `.mcp.json` nested many thousands of levels deep ends the run with an error and no
  verdict. The exit code is not zero.

## Licences

Three documents are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/):
the specification (`specification.md`), the rationale (`rationale.md`) and the compatibility
note (`compatibility.md`). Everything else here, including this README, the schemas, the
prompt files, the fixtures and the checker, is under the MIT licence, as is the rest of the
repository. See [`../LICENSE`](../LICENSE).
