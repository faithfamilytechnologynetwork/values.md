# arch-critical.md — Always-On System-Shape Facts (HOT tier)

<!-- HOT tier: capped facts + a bounded map of arch.md. Always injected into every porch
phase prompt and into CLAUDE.md/AGENTS.md. CAP: <=10 facts, <=12 map topics, <=35 lines.
To add a fact, DEMOTE a weaker one into arch.md (displacement). MAINTAIN polices the cap
and keeps the map in sync with arch.md's top-level sections. -->

## Critical facts (consult before deciding)
- The injected texts live once, in `spec/prompts/`; a quoted copy in a `spec/` document must match byte for byte.
- `spec/schema/values.schema.json` and the field table in `spec/specification.md` change together; `consistency` compares them word for word.
- Packages live once, in `values/`; `spec/` refers to them by path and never copies one.
- The fixtures are the test suite: a new rule, failure or schema constraint needs a fixture, or `fixtures` fails its audits.
- Fixture files are exact bytes (`spec/fixtures/.gitattributes`); never let a tool normalise their line endings or encoding.
- The checker makes no network call and loads no model; loader and chatbot code do not belong under `spec/`.
- The checker reads nothing through a symbolic link, and a crash is a bug to surface, not an "invalid" verdict.
- Tests are four commands (`fixtures`, `selftest`, `consistency`, `check values/`), in `.codev/config.json` for porch and in the GitHub workflow; there is no `npm`.
- `spec/`, `values/` and the root README are public-facing: no issue numbers, account details or private remarks.
- Three documents are CC BY 4.0, the rest is MIT, and a bundled public-domain text states its own source.

## Map of arch.md (consult when…)
- Repository layout — consult when deciding where a new file belongs.
- Single sources of truth — consult when quoting a normative text, a field or a package anywhere.
- The checker — consult when changing a validity or reading rule.
- Fixtures and audits — consult when adding, changing or regenerating a fixture.
- Document consistency — consult when editing a document under `spec/` or adding a marker.
- The collection in values/ — consult when adding or editing a package.
- Checks porch runs — consult when a porch or GitHub check fails or a command is added.
- Licences — consult when adding a file, a bundled text or a licence statement.
- Verified-Wrong Assumptions — consult when relying on how Claude Code, YAML or Agent Skills behave.
