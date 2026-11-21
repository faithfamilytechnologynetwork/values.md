# Lessons Learned

Durable engineering lessons from work in this repository. Each one names what it rests on.

## Writing a standard

- Build the checker and fixtures before the prose. Writing the rules as code first exposed
  more than twenty places where the approved text was silent (what "whitespace" means, how a
  fence closes, which rules are reported after an earlier one fails). Each surfaced as a
  fixture that had to have an outcome.
- Where the text leaves an edge case open, take the simplest deterministic option, pin it with
  a fixture, and state it in the specification. Do not add rules the specification did not
  ask for. A rule every reader applies the same way beats a more permissive one that needs
  further definitions (refusing every explicit YAML tag, comparing case for A to Z only).
- Define ordinary words once when a rule depends on them. "Character", "whitespace", "without
  regard to case" and "on one line" each had two defensible readings until they were fixed.
- Give a second implementer the text and nothing else. Two agents with only the specification
  reproduced the renderings byte for byte, and the doubts they listed pointed at the passages
  that needed tightening.

## Tests that can fail

- A check that cannot fail proves nothing. Every command that reports "all agree" has a
  matching deliberate break in `selftest`.
- Audit coverage mechanically. A hand-written list of cases missed the `type` constraints. The
  audit that walks the schema found them, and found a real defect on its first run.
- Expected outputs must not be the program's own output. The renderings were made separately
  from the normative texts, and two were typed by hand first.
- An entry that is a directory where a file is expected, or the reverse, is a class of input
  to test for every file a rule reads. Two review rounds in a row each found another one.

## Outside tools and sources

- Re-read a cited page at the source on the day the claim is written. A summarising fetch gave
  the hook limit without its behaviour over the limit, and a second-hand note had one of
  another format's attribute names wrong.
- Mark each statement about an outside tool as documented, observed or inferred, with the tool
  version and date. Reviewers asked for exactly this wherever it was missing.
- Run outside-tool checks on temporary copies outside the repository. When a tool cannot be
  run, record the criterion as not verified. Do not work around the denial.
- A redistributed public-domain transcription may follow a later printing than its title page
  suggests. Compare the text against sibling editions before bundling it, and check the
  distributor's terms on using its name.

## Working with reviewers

- Do not commit while consultations are running. A reviewer that sees the branch move reports
  it, and its review covers an older tree.
- Reviewers read only tracked files and often cannot run commands. Evidence kept in an
  untracked log is invisible to them, so command results and outside-tool records belong in a
  tracked file or in the response they are given.
- A fix made after the last review round is unreviewed. List such commits in the review
  document so the pull request reviewer knows where to look.
- Read the whole of a tool's task output before running it again. A second request can
  acknowledge the first and its instructions are gone.

## Public repository hygiene

- The standard, the packages and the root README are written for public readers. They carry
  no issue numbers, no account details and no reference to parts of the repository that do
  not exist yet.
- State what a licence sentence excepts. "Everything else is MIT" was wrong twice, once for a
  README that covered itself and once for bundled public-domain texts.
