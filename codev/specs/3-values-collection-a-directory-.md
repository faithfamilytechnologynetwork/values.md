# Specification: The values collection — a browser and a submission flow for `values/`

<!--
SPEC vs PLAN BOUNDARY:
This spec defines WHAT and WHY. The plan defines HOW and WHEN.
Keep implementation phases, file paths, code, and "first we will… then we will…"
out of the spec — those belong in codev/plans/<id>-*.md.
-->

Issue: #3. Protocol: SPIR. The repository has three parts: `spec/` (the standard, issue #1),
`reference/` (the reference chatbot, issue #2) and `values/` (the collection of value systems).
This project builds what surrounds `values/`: the rules for what is listed, the way to submit,
a website for looking through the collection, and the file that makes every listed value
system installable in Claude Code.

"The standard" below means the values.md standard v0.1 as built on pull request #4
(`spec/specification.md`). "Part N" means part N of that document. "V1" to "V10" are its
validity rules. Terms taken from the standard: value system, package, host, steward, claim,
collection.

Terms used here:

- **Browser**: the public website that lists the packages in `values/` and has a page for each.
- **Submission**: a pull request that adds one package folder to `values/`, or changes one
  that is already there.
- **Submitter**: the person who opens a submission.
- **Maintainer**: a person with the right to merge into this repository.
- **Policy**: the acceptance policy, the document that says what is listed and who decides.
- **Collection rules**: the few rules the policy adds that a program can check, numbered C1
  to C5 below. They are the collection's own. They are not part of the standard.

## Problem Statement

The standard lets a community write its values once, as a package. Nothing yet lets anyone
find a package, judge whether to trust it, or offer one of their own.

Three groups of people are affected:

- **A visitor** who wants an assistant to answer from their tradition has no place to look.
  Today the only way to see what exists is to read folders in a code repository. Nothing shows
  them, in plain words, who vouches for a package, what kind of claim that is, or where their
  questions will be sent if they install it.
- **A community or a person with a value system to offer** has no stated way to submit it and
  no stated rule for what will be accepted.
- **The maintainers** have no policy to apply. A public collection of value systems will
  receive submissions that are hateful, that are written to manipulate a model, that claim to
  speak for a body that never agreed to it, or that point at a server nobody has looked at.
  Without a written rule, each such case is decided from scratch and in public.

The standard is deliberately neutral on content, and it says so: whether a package is
acceptable, what evidence a claim of authority needs, and what review a declared tool gets
are each left to the collection that lists it. This project is where those are answered for
this collection.

## Current State

What exists on pull request #4, which the owner has approved for merging:

- `values/` holds four packages: `plain-speaking`, `example-principled-pluralism`,
  `example-islam` and `example-roman-catholic`. They are the standard's own examples.
- The checker under `spec/` applies V1 to V10 to a file, a folder or a whole collection. It
  also prints the Claude Code marketplace entries for a collection, by the mapping in part 12.
- A GitHub workflow runs the checker on every pull request, `values/` included. A submission
  that breaks a validity rule already fails.
- The repository is public. It has no website, no marketplace file, no contributing guide, no
  pull request template and no policy.

What is missing, and what that costs:

- Validity is about form. A package that is perfectly valid can still be hateful, deceptive,
  falsely `official`, or wired to a hostile server. Nothing checks any of that, and nothing
  says who would.
- A package folder can be read on GitHub, but only by someone who knows what `VALUES.md`,
  `.mcp.json` and `steward.claim` mean.
- A user of Claude Code cannot install a package from here, because the repository has no
  `.claude-plugin/marketplace.json`.

Facts checked for this spec:

| Subject | Finding | Status |
|---|---|---|
| The repository | Public. GitHub Pages is not enabled. | Checked on 2026-11-21 through the GitHub API. |
| Claude Code marketplaces | The file is `.claude-plugin/marketplace.json` at the marketplace root. `name`, `owner` and `plugins` are required, and `description` is optional, with a warning from `claude plugin validate` when it is missing. A user adds a marketplace kept in a GitHub repository with `/plugin marketplace add <owner>/<repo>` and installs with `/plugin install <plugin>@<marketplace>`. An entry whose `source` is a relative path works only when the marketplace is added from a git repository. Added as a bare URL to the file, such an entry fails at install. Automatic updating is off by default. An installed plugin is fetched again only when its `version` changes. | Documentation read on 2026-11-21. |
| The marketplace mapping | The checker's `marketplace` command, run on `values/`, prints four entries that follow part 12. A file built from them passed `claude plugin validate` in the standard's own project, and both folder packages installed from it. | Command run on 2026-11-21. The validation and installs are that project's report. |
| What Claude Code gets from a package | A package's skills and MCP servers. Not its prompt, because Claude Code does not read `VALUES.md`. Two of the four packages are a `VALUES.md` alone, so installing them gives Claude Code nothing until a prompt adapter exists. The adapter belongs to issue #2 and is not built. | From the standard's compatibility note. |
| The reference chatbot | The owner has decided it is hosted on the internet. Its spec is being revised, and it has no public address yet. | From issue #2. |

## Desired State

Three people, three experiences.

A **visitor** opens the browser. They see every value system in the collection, search for
their tradition and open a page. The page tells them what the value system is, who vouches for
it and what that claim amounts to, the exact prompt an assistant would be given, where their
questions would be sent, and how to install it or try it.

A **submitter** reads one short guide, adds one folder and opens a pull request. A check tells
them within minutes whether the package is well formed. A maintainer then reviews it against a
written policy and either merges it or says which rule it breaks.

A **maintainer** has a policy short enough to hold in mind, a checklist to go through, and
nothing to do after merging: the browser and the marketplace file bring themselves up to date.

The rest of this section states what is built and decided. The reasoning and the alternatives
are under Solution Approaches.

### 1. What is delivered

1. **The policy**: one short document saying what is listed, what is not, and who decides.
2. **The contributing guide** and **the pull request template**: how to submit, and the
   checklist a submission is reviewed against.
3. **The submission check**: the existing check on a pull request, extended with the
   collection rules and a trial build of the browser.
4. **The browser**: a static website generated from `values/` and published from the
   repository.
5. **The marketplace file**: `.claude-plugin/marketplace.json` at the root of the repository,
   generated from `values/`.
6. **The generator**: the program that does 3, 4 and 5, in a directory of its own, `browser/`,
   at the root of the repository.

The collection directory itself, `values/`, and its first four packages already exist. This
project does not move or change them.

### 2. The policy

The policy is the owner's to decide. What follows is the recommended text, kept short on
purpose. Open question 1 puts it to him.

**What the collection is.** A list of value systems that anyone may install. Listing a
package is not endorsing it. The collection lists value systems its maintainers disagree with,
and the browser says so on every page.

**Who decides.** A submission is merged by a maintainer. The owner names the maintainers and
settles any dispute. A submission that is declined is told which rule it breaks, and may be
revised and resubmitted.

**What is listed.** A package is listed when all of these hold:

1. **It is valid** by the standard and meets the collection rules (part 4).
2. **It says what it is.** Its name, description and tradition describe what the body
   actually says. A reader of the listing is not surprised by the prompt.
3. **Its claim is supported** (part 3).
4. **It is on the side of the person using it.** It does not tell the model to deceive the
   user, to work against the user's interests, to hide that a value system is installed, to
   collect personal details, or to sell or advertise.
5. **It is written for people to read.** It has no hidden, encoded or obfuscated text, no
   text addressed to a reviewer or a checker, and no instruction to disregard the host's rules
   or the standard's wrapper.
6. **It does not direct harm at people.** A value system may say that a belief or a way of
   living is wrong. It may not call for or praise violence against people or harassment of
   them, or treat a group of people as less than human.
7. **Its tools pass review** (part 5).
8. **Its content may be redistributed** (part 6).
9. **A maintainer can read it.** A package in a language no maintainer reads waits until a
   reviewer who reads that language is found. It is not merged on a machine translation.

**Disagreement is not a ground for removal.** A package is its steward's statement. Someone
who holds that it gets their tradition wrong can submit their own, and both are listed. A
package is removed when it turns out to break the policy, when its steward withdraws the
statement that supports its claim, or when a server it declares has become unsafe.

**Changes.** A change to a listed package is reviewed like a new one, comes from its steward
or with the steward's agreement, and carries a new `version`.

### 3. Claims of authority

The standard has three kinds of claim and verifies none of them. The collection asks for this
before listing:

| Claim | What the collection needs before listing |
|---|---|
| `individual` | Nothing further. The steward's name must not be the name of an organization, or of a well-known person other than the submitter. |
| `organization` | The address in `steward.url` belongs to the organization, and a page there names the package and says the organization stands behind it. |
| `official` | The same public statement, on the address of the body that holds the authority, saying that the package is its official statement. The package's description says whose official statement it is. |

- A maintainer opens the address and reads the statement before merging. The pull request
  records the date.
- The collection needs no new field for this. The standard requires `steward.url` for both
  kinds "so that there is somewhere to check the claim", and the collection holds it to that
  purpose.
- **`official` is for a body's statement about itself.** It is accepted for an institution
  with a defined membership or jurisdiction, speaking of its own teaching or rules: a
  denomination, a bishops' conference, a professional body, a company. It is not accepted as a
  claim to speak for a whole tradition that has no single authority. Such a package is listed
  as `organization` or not at all.
- The collection checks the statement once, at merge. It does not watch the page afterwards.

How the browser shows the difference. Every listing and every page carries the steward's name
and the kind of claim, in words, and the page says what was and was not checked:

| Claim | What the page says |
|---|---|
| `individual` | One person's own statement of this value system. They speak for nobody else. The collection has not checked who they are. |
| `organization` | An organization that stands behind this package as its own work. It does not claim to be the authority over the value system. When the package was listed, the organization's own site said so. A link to `steward.url` follows, for the visitor to check. |
| `official` | The steward says it is the body with authority here, or is authorised by it, and that this is its official statement. When the package was listed, that body's own site said so. A link to `steward.url` follows, for the visitor to check. |

On every page the claim is called a claim made by the package. No badge, tick or colour
suggests that the collection vouches for it.

### 4. The collection rules

These are the rules a program can check. The submission check applies them after V1 to V10.

| Rule | A package is accepted only if |
|---|---|
| C1 | It is a folder that the standard's checker finds valid. A package the checker cannot judge, because it targets a later version of the standard, is not accepted. |
| C2 | Its `VALUES.md` has a `version`, and a `license` that is on the collection's list (part 6). |
| C3 | Its `.mcp.json`, if it has one, declares no local server. |
| C4 | Every file in it is UTF-8 text, and its files come to no more than 2 MB together. |
| C5 | Its name does not begin `example-`. |

The four packages already in `values/` are the standard's own examples. The generator's
settings list them by name, the collection rules are not applied to them, and the browser
labels each as an example from the standard. One of them, `plain-speaking`, is the smallest
valid file and so has neither `version` nor `license`.

A failed rule is reported by its identifier with a sentence saying what is wrong, in the same
manner as the checker's own output.

### 5. Tools and declared models

Installing a package with a declared server sends the user's questions to that server. The
standard makes a host ask for consent. The collection does its own part before listing.

- **No local servers** (C3). A local server is a command run on the user's machine. The
  standard lets a collection refuse them, and this one does.
- **A remote server is reviewed once, by a maintainer, before merging:**
  1. The package's README says who runs the server and what is sent to it.
  2. The server answers and lists its tools.
  3. The names and descriptions of its tools are read. They match what the package says the
     server is for, and they contain no instructions aimed at the model beyond describing the
     tool.
  4. The pull request records the date and the tools listed.
- A change to a package's `.mcp.json` gets the same review.
- The collection does not monitor a server after listing, and the browser says so. A server
  reported as unsafe is a ground for removal.
- **The browser shows each declared server** by name and address, with one plain sentence:
  installing this value system lets an assistant send your questions to that address, and the
  collection looked at the server when the package was listed and does not watch it.
- **Skills and bundled texts** are read by the reviewer as the body is. Rule C4 keeps them to
  text.

**Declared models.** The standard allows a package to declare only a model that anyone with
access to the provider can load.

- A maintainer loads a declared model once before merging. If no maintainer has access to the
  provider, the package is merged without that model entry.
- The browser shows each declared model with its provider, base model, adapter, context
  window and description, and what its `prompt` value means in plain words: that it is meant
  to run with this prompt, with or without it, or on its own without it. It says that using
  the model needs an account with the provider, and that a model run without the prompt
  behaves as its weights dictate.

### 6. Licensing

- Every submission states a licence (C2). The accepted licences are those that let anyone
  copy and redistribute the package unchanged, for any purpose including a commercial one:
  `CC0-1.0`, `CC-BY-4.0`, `CC-BY-SA-4.0`, `CC-BY-ND-4.0`, `MIT` and `Apache-2.0`. A
  no-derivatives licence is on the list because a body may reasonably not want altered copies
  of its statement in circulation. A non-commercial licence is not, because it would stop a
  commercial assistant from installing the package. The list is a setting, and the owner can
  add to it.
- By submitting, the submitter states that they have the right to offer the content under
  that licence. The pull request template has them say so.
- **Bundled texts.** A package may bundle a text only if it is in the public domain, or the
  submitter holds the rights to it, or it is under an accepted licence. Each bundled text
  states its source and the basis of its status, as the standard's own examples do. A text
  under someone else's copyright is cited and linked, not bundled.
- The repository's licence index currently says every package in `values/` is under the MIT
  licence. It is changed to say that each package is under the licence its own `VALUES.md`
  names, and that the four examples are MIT.

### 7. Names

The standard already makes names unique: V10 requires the folder name to equal the package's
`name`, with no two alike. The policy adds:

- **First come, with a complete package.** A name is taken by a package that is accepted.
  There are no reservations and no placeholders.
- **A name claims no more than the package does.** A bare name of a tradition, such as
  `islam` or `christianity`, is not given to anyone. A package takes a name that says which
  school, community or steward it is, such as a tradition followed by a denomination or by
  the steward's own name. The name of an institution goes only to a package that institution
  stands behind.
- **Several packages for one tradition are welcome.** Schools, denominations and different
  stewards each get their own package and their own name. The `tradition` field groups them
  in the browser.
- **One spelling per tradition.** The standard leaves any vocabulary for `tradition` to the
  collection. This collection keeps none. A reviewer asks a submitter to use the spelling
  already in the collection for the same tradition, so that the browser groups them.
- **Languages.** One package may list several languages. A translation maintained separately
  is its own package, with the language tag at the end of its name.
- **A listed name does not change.** Installs refer to it. A package that needs another name
  is submitted anew and the old one removed.
- **`example-`** is kept for the standard's own examples (C5).

### 8. Submitting

- A submission is a pull request that adds or changes one folder under `values/` and touches
  nothing else. The submitter does not edit the marketplace file or anything the browser is
  built from.
- The contributing guide says, in order: what a package is, with a link to the smallest valid
  file; what the policy asks; how to choose a name; what evidence a claim needs; what a
  declared server or model needs; how to run the check before submitting; and what happens
  after the pull request is opened.
- The pull request template is the reviewer's checklist in the submitter's words: the name,
  the kind of claim and where the steward's statement is, the licence and the statement of
  rights, who runs any declared server, and the source of any bundled text.
- **The submission check** runs on every pull request, without write access to the repository
  and without secrets. It runs the standard's checks as today, then the collection rules,
  then a trial build of the browser and the marketplace file. It fails if any of these fails.
  It publishes nothing.
- Everything the policy asks that a program cannot judge is checked by a maintainer, using the
  template.

### 9. The browser

**Form.** A static website: plain pages generated from `values/`, with no server, no accounts
and no database. It is published with GitHub Pages from this repository.

**The list page** shows every package: its name, its description, its steward and kind of
claim, its tradition and its languages, and marks for "connects to a tool", "declares a
fine-tuned model" and "example from the standard".

- A search box narrows the list by name, description, steward, tradition and tags.
- Filters narrow it by tradition, by language and by kind of claim. Traditions are grouped by
  the first item of `tradition`, compared without regard to case, as part 12 says.
- With scripts turned off in the visitor's browser, the whole list is still there. Only
  search and filters need scripts.

**A page for each package**, at an address made from its name, shows:

1. The name, the description and the label "example from the standard" where it applies.
2. The steward, the kind of claim and what was checked, as part 3 sets out.
3. The version, the licence, the authors where given, the tradition, the languages and the
   tags.
4. **The prompt**: the body of `VALUES.md`, in full, as plain text. The page says that this is
   the text an assistant is given, and which part of it is the core that is repeated as a
   conversation grows.
5. **Tools**: each declared server, as part 5 sets out. Where there are none, the page says
   that this value system connects to nothing.
6. **Skills and bundled texts**: each skill by name and description, and each bundled text by
   file name, with a link to the file in the repository.
7. **Fine-tuned models**, as part 5 sets out.
8. **How to install it**:
   - In an assistant that follows the standard: a link to the package folder in the
     repository, and a link to the `VALUES.md` file itself.
   - In Claude Code: the two commands, to add this repository as a marketplace and to install
     this package from it. The page says plainly what Claude Code gets: the package's tools
     and skills and not its prompt. For a package that is a `VALUES.md` alone, it says that
     installing it in Claude Code does nothing yet.
   - **Try it**: a link to the reference chatbot with this value system chosen, shown when the
     chatbot's address is set (part 11).
9. A link to the package's folder and to its history in the repository.

**Every page** carries a line saying that listing is not endorsement, and links to the policy,
to the standard and to the contributing guide.

**Untrusted text.** Everything that comes from a package is shown as text. A package's
Markdown is not rendered, and none of its content is run or treated as markup. A link taken
from a package is shown with its full address visible.

**Staying current.** The browser is rebuilt and published whenever `values/` changes on the
main branch. Nobody edits a page by hand, and no built page is kept in the repository. If a
build fails, the site that was published before stays up.

The browser is in English in this version.

### 10. The marketplace file

- `.claude-plugin/marketplace.json` at the root of the repository lists every package in
  `values/`. Each entry is exactly what the mapping in part 12 gives, as the standard's
  checker prints it. This project writes no second mapping.
- The file's own name is `values-md`, its owner is the values.md project, and it has a
  one-line description. These are settings.
- The file is kept in the repository, because Claude Code resolves an entry's relative path
  only for a marketplace added from a git repository.
- It is regenerated and committed by the same automatic step that publishes the browser,
  whenever `values/` changes on the main branch. A submitter never edits it, so two
  submissions open at once do not collide over it.
- It carries no hooks. Getting a package's prompt into Claude Code needs the adapter of issue
  #2. Attaching that adapter to the marketplace entries is later work (open question 5).

### 11. The link to the reference chatbot

The question of how a newly merged value system reaches the running chatbot now belongs to
issue #2. What this project provides:

- The browser is the one catalogue. The chatbot lists what a visitor needs to pick panes and
  links here for the rest.
- Each package page links to the chatbot with that value system chosen. The form of that
  link is a single setting, a pattern with the package's name in it. Until the chatbot has a
  public address the setting is empty and no link is shown.

### 12. Where the generator lives

In `browser/`, a directory of its own at the root of the repository. It holds the program
that applies the collection rules, builds the site and writes the marketplace file, with its
templates, its settings and its tests.

- It uses the standard's checker as a library for reading a package, deciding validity and
  producing marketplace entries. It contains no second reader of `VALUES.md`.
- It is written in Python and run with uv, as the checker is, so the repository keeps one
  toolchain. The pages it produces need no build step of their own.
- It makes no network call. Building the site needs only the working tree.

### 13. Where the issue's eight questions are answered

| The issue asks | Answered in |
|---|---|
| 1. Acceptance policy: what is accepted and who decides | Part 2 |
| 2. Claims of authority: the evidence each needs and how the browser shows the difference | Part 3 |
| 3. Tool safety: what review a declared tool gets | Part 5, and rule C3 |
| 4. Model declarations | Part 5. The question as asked is out of date: the standard now allows only public models. |
| 5. Licensing, and bundled copyrighted texts | Part 6 |
| 6. Names: uniqueness, squatting, several packages for one tradition | Part 7 |
| 7. The live link | Part 11. The question now belongs to issue #2. |
| 8. Where the browser's generator code lives | Part 12 |

## Success Criteria

Criteria marked (owner) need an action only someone with administrative rights on the
repository can take. If one has not been taken, it is reported as not verified in the review
and to the architect. It is never ticked on trust.

Documents

- [ ] The policy exists as one document, states parts 2, 3, 5, 6 and 7 as the owner approved
      them, and is linked from the root README, the contributing guide and every page of the
      browser.
- [ ] The contributing guide covers the seven points of part 8 in order. A reader given only
      the guide, the policy and the standard can produce a package that passes the submission
      check. Tested with an agent that has no other context.
- [ ] A new pull request opens with the template of part 8.
- [ ] The repository's licence index says each package is under the licence its own
      `VALUES.md` names.

The submission check

- [ ] On a pull request, the check runs the standard's four commands, the collection rules
      and a trial build, and fails when any of them fails.
- [ ] For each of C1 to C5 there is a test package that breaks that rule alone, and the check
      reports it by its identifier. A package that meets all five passes.
- [ ] The four examples pass, although `plain-speaking` has neither `version` nor `license`.
- [ ] The workflow that runs on a pull request has no write permission and uses no secret.
- [ ] The collection rules and the build run with the network blocked.

The browser

- [ ] Building from `values/` produces a list page and one page for each package, and nothing
      else needs to be running to view them.
- [ ] The list page shows, for every package, the fields of part 9. Search narrows the list by
      name, description, steward, tradition and tags. The filters narrow it by tradition,
      language and kind of claim. Two packages whose `tradition` differs only in case fall in
      one group.
- [ ] With scripts turned off, the list page shows every package and every package page shows
      everything in part 9.
- [ ] Each package page shows the nine items of part 9. The prompt shown is, character for
      character, the body the standard's checker reads from the file.
- [ ] For each kind of claim, the page carries the wording of part 3. A page for an
      `individual` package shows no link presented as evidence. No page shows a mark that
      presents a claim as verified by the collection.
- [ ] A package with a declared server shows the server's name and address and the sentence
      of part 5. A package with none says that it connects to nothing.
- [ ] A package with a declared model shows the fields of part 5 and the plain-words meaning
      of its `prompt` value, for each of `required`, `optional` and `omit`.
- [ ] The Claude Code instructions on a page name this repository and the package, and say
      what Claude Code does and does not get. For a package that is a `VALUES.md` alone the
      page says installing it in Claude Code does nothing yet.
- [ ] A package whose name, description, steward, body, tags, tool names and file names
      contain HTML and script markup is built into pages on which all of it appears as text.
      A built page loads no script, style, image or frame from an address a package supplied.
- [ ] Every link from a built page to another built page works when the site is served from a
      subdirectory, as GitHub Pages serves a project site.
- [ ] Every page carries the line that listing is not endorsement and the three links of
      part 9.
- [ ] With the chatbot setting empty, no page shows a "try it" link. With it set, every
      package page links to the pattern with its own name filled in.
- [ ] No built page is in the repository.

The marketplace file

- [ ] `.claude-plugin/marketplace.json` exists at the root, and its `plugins` list is, value
      for value, what the standard's `marketplace` command prints for `values/`.
- [ ] `claude plugin validate` passes on the file with no warning about a missing description.
      If the tool cannot be run, this is reported as not verified.
- [ ] A package folder added to a copy of `values/` appears in the file and in the browser
      after one run of the generator, with no other change.

Publishing

- [ ] A change to `values/` on the main branch rebuilds the browser, regenerates the
      marketplace file and commits it if it changed, with no person involved.
- [ ] (owner) GitHub Pages is enabled for the repository, the browser is reachable at its
      public address, and the review records that address and the date it was opened.
- [ ] (owner) After a merge that adds a package, that package appears in the published
      browser and in the marketplace file on the main branch. Until a real submission
      arrives, this is shown with a test package that is then removed, or reported as not
      verified.

Scope

- [ ] Outside `browser/`, this project adds or changes only: the policy, the contributing
      guide, the pull request template, the workflows, the marketplace file, the root README,
      the licence index and Codev artifacts. It changes no package in `values/` and nothing
      else under `spec/`.
- [ ] `browser/` holds no reader of `VALUES.md` and no marketplace mapping of its own.
- [ ] The generator's tests pass with the network blocked.

## Constraints

Decided by the owner on 2026-11-20, copied from the issue. These are fixed.

- The collection is a directory in this repository. An earlier plan for a separate repository
  is dropped.
- It has a browser for the value systems in it.
- People can submit their own value systems.
- The reference implementation (#2) keeps a live link to the collection: it loads its value
  systems from this directory, so a value system added here appears in the chatbot without
  being copied.

From the issue. Also fixed.

- The repository has three parts: `spec/`, `reference/` and the collection directory.
- Depends on #1: the browser renders packages in the format the standard defines, and
  submissions are checked against its validity rules.
- Out of scope: hosted accounts, ratings, comments or any server-side database, and
  governance and funding beyond the acceptance policy.

From the architect's starting notes on the issue (2026-11-21). Also fixed.

- The standard is read from pull request #4's branch until it merges, and from `main` after.
- `values/`, its four packages, the checker, its `marketplace` command and the workflow that
  runs the checks already exist. This issue adds what is missing around them: the acceptance
  policy, the pull request template, the contributing guide, the browser and the generated
  marketplace file.
- Question 4 is out of date. The standard now allows a package to declare only public models.
  The browser shows a declared model as the standard's disclosure rules say.
- Question 7 belongs to #2. The owner has decided that the reference chatbot is hosted on the
  internet. What this issue owes it: the browser links each value system to the chatbot so a
  visitor can try it, and the two do not each build a catalogue.
- Keep it light. Prefer a static site and plain files, the fewest moving parts, and no new
  rule in the standard. Where something is open, take the simplest option and say so.
- The acceptance policy (questions 1 to 3 and 5) is the owner's to decide. He is given a
  short recommended policy, not a survey.
- The repository is public. Review records and builder notes are not committed here.

Further constraints:

- The standard is not changed. The collection rules are the collection's own, and the
  collection adds no field to `VALUES.md`.
- Every package in `values/` stays a package exactly as the standard defines it. Nothing is
  added to a package folder for the browser's or the marketplace's benefit.
- A folder directly inside `values/` is a package, by the checker's reading of a collection.
  So nothing that is not a package can be a folder there.
- A pull request from outside must not be able to publish, to write to the repository or to
  read a secret.
- The browser is served from a project's public address and shows text written by strangers.
  It must not let that text act as anything but text.

## Assumptions

- Pull request #4 merges, or its branch is otherwise made available to this project's branch,
  before the implementation needs `spec/` and `values/` in the working tree. If it has not
  when implementation starts, the architect decides how this branch gets them.
- The checker can be used as a library, as issue #2's spec also assumes, and gives a caller
  the frontmatter, the body, the core and the marketplace entries of a valid package.
- GitHub Pages can be enabled for this repository, and a workflow on the main branch may
  commit the regenerated marketplace file. Both depend on settings only the owner controls. If
  the main branch is protected against such a commit, open question 3 is reopened.
- The owner names the maintainers. Until he does, he is the only one.
- A maintainer can reach a declared server and read what it lists. Loading a declared model
  needs access to its provider, which a maintainer may not have (part 5).
- Submissions arrive slowly enough for a person to review each one. Nothing here is designed
  for hundreds a week.
- The reference chatbot will accept a link that names one value system. The form of that link
  is its own project's to decide, which is why it is a setting here.
- A collection of a few hundred packages is small enough to list on one page and search in
  the visitor's browser. Beyond that the list page needs rethinking, and nothing else does.

## Solution Approaches

### The form of the browser

The owner decided that the collection has a browser. What kind of thing it is was open.

### Approach 1: Static pages generated by a small Python program (recommended)

A program in the repository reads `values/` through the standard's checker and writes plain
HTML pages: a list and a page for each package. A short script on the list page does search
and filtering. GitHub Pages serves the result.

- For: one toolchain in the repository, the one the checker already uses. Reading and
  validity come from the checker, so the browser cannot disagree with the standard about what
  a file says. Pages are whole without scripts, can be linked to and can be read by anything.
  No server to run, pay for or secure.
- Against: the program is this project's to write and keep, where a ready-made site builder
  would bring templates and themes.
- Risk: low.

### Approach 2: A single page that builds itself in the visitor's browser

The build step writes one data file. A page loads it and draws the list and each package.

- For: the least generated output.
- Against: nothing is readable without scripts, a package has no real page of its own to link
  to, and the code that turns untrusted text into a page runs in every visitor's browser,
  where a mistake is an open door.
- Risk: medium.

### Approach 3: A ready-made static site builder

A general tool such as Jekyll, Eleventy or Astro, with the packages as its content.

- For: themes, templates and a familiar way of working.
- Against: a second toolchain. These tools read frontmatter with their own YAML reader and by
  their own rules, which differ from the standard's reading rules (YAML 1.2, no duplicate
  keys, no aliases), so the site could show something other than what a host installs. They
  also expect to render Markdown, which is the opposite of what untrusted bodies need.
- Risk: medium. Two readings of the same file can drift.

### Approach 4: No website

A generated table in a README, read on GitHub.

- For: nothing to host.
- Against: the owner decided there is a browser. A README table cannot be searched or
  filtered, and cannot show a prompt, a claim and a tool warning with the care they need.
- Risk: low to build. It does not meet the decision.

Approach 1 is recommended.

### Decisions inside that approach

The first alternative listed in each is the one adopted in Desired State.

**Where the generator lives.**

- Adopted: `browser/`, a fourth directory at the root. The issue names three parts and asks
  where this code goes, since each existing part is spoken for.
- Rejected: inside `values/`. Every folder there is a package, and code among the packages
  would be reviewed as one.
- Rejected: inside `spec/`, beside the checker. The checker is the standard testing itself. A
  site builder, with one collection's policy in it, is not part of a standard.
- Rejected: inside `reference/`. That is the chatbot, a different program with a different
  owner in this repository.

**How the prompt is shown.**

- Adopted: as plain text, exactly as written. It is what the model is given, and showing it
  unrendered is both the honest view and the safe one.
- Rejected: rendered as Markdown. It reads more pleasantly, and it lets a stranger's text put
  links, images and layout on the project's own site.

**How the evidence for a claim is recorded.**

- Adopted: the steward's statement is at `steward.url`, which the standard already requires
  for these claims and for this purpose. The browser links to it, and the visitor can check
  it themselves.
- Rejected: a field of the collection's own under `metadata`, pointing at the evidence. It
  lets `steward.url` stay a home page, at the cost of a field every submitter has to learn.
- Rejected: evidence kept only in the pull request. A visitor cannot see it, and the browser
  could say nothing about what was checked.

**How the marketplace file stays current.**

- Adopted: an automatic step on the main branch regenerates and commits it.
- Rejected: the submitter regenerates it and the check refuses a stale one. A steward
  submitting through GitHub's web pages cannot run a command, and two open submissions would
  each change the same file and collide.
- Rejected: not keeping the file in the repository and publishing it with the browser.
  Claude Code resolves relative paths only for a marketplace added from a git repository.

**What is checked by a program and what by a person.**

- Adopted: a program checks form, the five collection rules and that the site builds. A
  person checks everything that needs judgement.
- Rejected: automatic screening of content by a model or a word list. It would be wrong often
  enough, in both directions, to need the person anyway, and a collection of value systems
  should not have its listings decided by a model's values.
- Rejected: checking declared servers automatically on every pull request. It would send
  requests to an address a stranger chose, from the project's own workflow.

**Where a visitor gets a package from.**

- Adopted: links to the folder and to `VALUES.md` in the repository. The standard defines no
  archive format for a package, and this project does not invent one.
- Rejected: a downloadable archive for each package. Convenient, and one more thing to build
  and keep right. It can be added without changing anything else.

## Open Questions

**Critical** (blocks progress)

None for writing the plan.

**Important** (shapes the design, and the owner decides)

Desired State is written on the recommended answer to each, so that the spec states one
design. If the owner decides otherwise at the gate, the spec is revised before the plan is
written.

1. **The policy.** Parts 2, 3, 5, 6 and 7 are the recommended policy. The calls in it that a
   submitter or a visitor would notice:
   - The line on content: a value system may say a belief or a way of living is wrong, and
     may not direct harm at people or treat a group as less than human.
   - Evidence for `organization` and `official`: a statement on the steward's own site, at
     `steward.url`.
   - `official` only for a body speaking of its own teaching or rules, never for a whole
     tradition that has no single authority.
   - No local servers. A remote server reviewed once and not watched.
   - The six accepted licences, with no-derivatives in and non-commercial out.
   - A bare tradition name is given to nobody.
2. **Who the maintainers are.** Recommended: the owner alone to begin with, adding others by
   name as submissions arrive.
3. **An automatic commit on the main branch.** The marketplace file is regenerated and
   committed by a workflow after each merge that changes `values/`. Recommended: yes. The
   alternative puts the work on submitters.
4. **Publishing.** Recommended: GitHub Pages at the repository's default address, with
   Pages enabled by the owner. Whether the browser gets a domain of its own is his to choose
   and changes nothing built here.
5. **Claude Code and the prompt.** Installing from the marketplace gives Claude Code a
   package's tools and skills and not its prompt, and for two of the four packages that is
   nothing. Recommended: publish the marketplace file now, as the issue asks, with each page
   saying plainly what Claude Code gets, and attach issue #2's prompt adapter to the entries
   as later work once it exists. The alternative is to leave single-file packages out of the
   marketplace until then.

**Nice-to-know** (does not block)

6. The form of the link to the reference chatbot. It is a setting, filled in when issue #2
   has an address.
7. Whether the standard's compatibility note should change. It says this repository does not
   ship a marketplace file. After this project it does. Reported to the architect, since the
   note belongs to the standard.
8. Whether the browser should also publish the list as a data file for other programs to
   read. Not built now. Nothing needs it yet.

## Test Scenarios

Without a network:

1. **The four examples.** The generator builds a list page and four package pages from
   `values/`. Each page shows the nine items of part 9 for its package.
2. **The standard's valid fixtures.** A collection made from the valid fixtures builds without
   error once given the fields C2 asks for, and each page's prompt equals the body the
   checker reads.
3. **Each collection rule.** A package breaking only C1, only C2 (no `version`, no `license`,
   a licence not on the list), only C3, only C4 (a file that is not UTF-8, a folder over the
   size limit) and only C5 is reported with that rule's identifier and the build stops.
4. **The examples are exempt.** `plain-speaking` builds with no `version` or `license`. A
   package of the same shape that is not on the examples list fails C2.
5. **Kinds of claim.** One package of each kind gives the wording of part 3. The `individual`
   page has no evidence link.
6. **Tools.** A package with a remote server shows its name, its address and the warning. A
   package with no `.mcp.json` says that it connects to nothing.
7. **Models.** Entries with `prompt` of `required`, `optional`, `omit` and absent each show the
   right plain-words meaning. The absent case reads as `required`, the standard's default.
8. **Skills and texts.** A package with a skill and bundled texts lists each with a working
   link into the repository.
9. **Hostile text.** A package whose every free-text field carries a script tag, an image
   tag, an event handler and a Markdown link builds into pages where all of it is visible as
   text, and the page's own markup is unchanged around it.
10. **Search and filters.** With packages of several traditions, languages and claims, each
    filter and the search box narrow the list to the expected names. `Islam` and `islam` are
    one group.
11. **No scripts.** The list and package pages hold all their content in the page as
    delivered.
12. **Served from a subdirectory.** Every link between built pages resolves.
13. **The chatbot link.** Absent when the setting is empty. Present, with the package's name,
    when it is set.
14. **The marketplace file.** The generated `plugins` list equals the checker's output for the
    same collection. Adding a package folder and building again adds its entry.
15. **Nothing else changes.** A build writes only the site's output and the marketplace file.
    It changes nothing in `values/`.
16. **The pull request workflow.** It asks for no write permission and names no secret.
17. **Cold reader.** An agent given the contributing guide, the policy and the standard, and
    nothing else, writes a package that passes the submission check.

With GitHub, and so with the owner's help:

18. **Publishing.** After a merge to the main branch that changes `values/`, the browser at
    its public address shows the change and the marketplace file on the main branch matches.
19. **A submission from outside.** A pull request from a fork runs the check and can neither
    publish nor write.
20. **Claude Code.** The marketplace is added from the repository and a folder package
    installs from it. Reported as not verified if it cannot be run.

Non-functional:

21. **No second reading.** `browser/` contains no parser of `VALUES.md` and no marketplace
    mapping.
22. **Honesty of the display.** No page presents a claim as verified by the collection, and no
    page omits the line that listing is not endorsement.

## Risks and Mitigation

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| A package passes review and is later found to be hateful or manipulative. | Medium | High | The policy states removal as the remedy and who decides. Every page says listing is not endorsement. The full prompt is on the page for anyone to read. |
| A package claims `official` falsely. | Medium | High | The statement must be on the body's own address, a maintainer reads it before merging, and the browser links to it and calls it a claim. `official` is refused for traditions with no single authority. |
| A steward's statement disappears after listing. | Medium | Medium | The browser says the statement was checked when the package was listed. A withdrawn statement is a ground for removal when reported. |
| A declared server turns hostile after listing. | Low | High | Hosts must ask consent before connecting, by the standard. The browser shows the address and says the collection does not watch it. Local servers are refused outright. A report leads to removal. |
| A stranger's text runs as markup on the project's site. | Medium | High | Everything from a package is shown as text and nothing is rendered. A hostile test package is part of the tests. |
| A pull request from outside abuses the workflow. | Low | High | The workflow on a pull request has no write access and no secret. Publishing happens only from the main branch. |
| The policy is seen as taking sides between traditions. | Medium | Medium | The content rule is about harm to people, not about doctrine. Disagreement is not a ground for removal, and rival statements are both listed. The owner decides the wording. |
| The automatic commit of the marketplace file is blocked by a repository setting. | Low | Low | Raised with the owner at the gate. The fallback is a maintainer running one command at merge. |
| Review does not keep up with submissions. | Low | Medium | The check removes malformed submissions before a person looks. The owner can name more maintainers. |
| A user installs a single-file package in Claude Code and nothing happens. | High | Low | Each page says so before they try. Open question 5 covers what comes after. |
| Pull request #4 changes after this spec is approved. | Low | Medium | The generator takes reading, validity and the mapping from the checker and holds no copy, so most changes arrive without work here. |
| The project grows into a site builder with features nobody asked for. | Medium | Medium | The spec lists what a page shows and stops. Archives, a data file and monitoring are named as not built. |

## References

- Issue #3 (this work), with the architect's starting notes in its first comment. Issue #1
  (the standard) and issue #2 (the reference chatbot).
- The standard on pull request #4: `spec/specification.md`, parts 2 (frontmatter), 7 (tools
  and consent), 9 (provenance), 11 (validity), 12 (collections, listings and the marketplace
  mapping) and 13 (security considerations). `spec/compatibility.md`, the section "A Claude
  Code marketplace". `spec/README.md` for the checker's commands. `spec/LICENSE.md`, the
  licence index.
- The standard's approved spec: `codev/specs/1-values-md-standard-v0-1-the-va.md`.
- The reference chatbot's spec: `codev/specs/2-reference-implementation-inkli.md`.
- Claude Code plugin marketplaces: https://code.claude.com/docs/en/plugin-marketplaces.md and
  https://code.claude.com/docs/en/plugins/marketplace-reference.md (read on 2026-11-21).
- GitHub Pages: https://docs.github.com/en/pages
- SPDX licence list: https://spdx.org/licenses/
