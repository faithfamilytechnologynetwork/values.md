# lessons-critical.md — Always-On Engineering Wisdom (HOT tier)

<!-- HOT tier: capped lessons + a bounded map of lessons-learned.md. Always injected into
every porch phase prompt and into CLAUDE.md/AGENTS.md. CAP: <=10 lessons, <=12 map topics,
<=35 lines. To add a lesson, DEMOTE a weaker one into lessons-learned.md (displacement).
MAINTAIN polices the cap and keeps the map in sync with lessons-learned.md's sections. -->

## Critical lessons (consult before deciding)
- Check for existing work (PRs, git history) before building from scratch.
- "It compiled" / "tests pass" is not "it works" — verify the real user path before calling it done.
- When stuck (2 failed hypotheses or ~30 min), get an outside perspective instead of guessing.
- Where the specification leaves an edge case open, take the simplest deterministic option, pin it with a fixture and state it in the text; add no rule it did not ask for.
- A check that cannot fail proves nothing: give every new check a deliberate break in `selftest`.
- Re-read a cited page at the source before stating what another format or tool does, and mark the claim documented, observed or inferred.
- Record a criterion you could not run as "not verified"; do not work around a denied tool.
- Do not commit while consultations are running, and list any commit made after the last review round as unreviewed.
- Reviewers see only tracked files and often cannot run commands; put the evidence where they can read it.

## Map of lessons-learned.md (consult when…)
- Writing a standard — consult when adding or changing a rule or its wording.
- Tests that can fail — consult when adding a check, a fixture or an expected output.
- Outside tools and sources — consult when citing another format, running an outside tool or bundling a text.
- Working with reviewers — consult when starting a consultation round or responding to one.
- Public repository hygiene — consult when writing anything a public reader will see.
