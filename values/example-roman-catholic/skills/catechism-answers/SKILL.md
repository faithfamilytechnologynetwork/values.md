---
name: catechism-answers
description: Looks up what the Roman Catholic Church teaches in the current Catechism of the Catholic Church through web search, preferring the Holy See's own site, and answers with the paragraph number and a link. Use when the user asks what the Catholic Church teaches about God, Jesus Christ, the Church, the sacraments, the commandments, prayer, or death and judgment.
license: MIT
compatibility: Needs a web search tool, or a tool that can open a web page. Without either, it says so and keeps to the basics in the package's VALUES.md.
metadata:
  status: Illustrative example. Not endorsed by any religious authority.
---

# Catechism answers

This skill is part of `example-roman-catholic`, an illustrative example package. No religious
authority has reviewed or endorsed it.

It says how to look up a point of Catholic teaching in the current Catechism of the Catholic
Church and how to answer from what you find. It carries no text of its own. The Catechism is
under copyright, so it is not bundled.

## Where the Catechism is

The Holy See publishes the Catechism in English on its own site:

https://www.vatican.va/archive/ENG0015/_INDEX.HTM

That page is the table of contents. Each section is a page of its own, linked from it. The
paragraphs are numbered from 1 to 2865, and the number is how the Catechism is cited.

| Part | Subject | Paragraphs |
|---|---|---|
| Prologue and Part One | The profession of faith: the creed, article by article | 1 to 1065 |
| Part Two | The celebration of the Christian mystery: the liturgy and the seven sacraments | 1066 to 1690 |
| Part Three | Life in Christ: conscience, virtue, sin, and the Ten Commandments | 1691 to 2557 |
| Part Four | Christian prayer, and the Lord's Prayer | 2558 to 2865 |

## How to look a point up

1. Search the web for the point together with the words "Catechism of the Catholic Church".
   Prefer a result on `vatican.va`. If the search tool can be limited to one site, limit it to
   that one.
2. If you can open a page, open the table of contents above, find the section by its heading
   and open that section.
3. Read the paragraphs that answer the question. Note their numbers and the address of the
   page.
4. If the Holy See's site cannot be reached, another site that gives the Catechism with its
   paragraph numbers will do. Say which site you used.

## How to answer

1. Give the Catechism's teaching, the paragraph number and the link to the page you read.
2. Quote only words you have in front of you from the page. Do not reword a quotation, and do
   not join two paragraphs into one.
3. If the user needs it, explain the teaching in plain English. Keep the explanation apart
   from the quotation, so that the user can tell the Catechism's words from yours.
4. If you do not find the point, say so. Do not stretch a paragraph to fit.
5. For a rule of practice, such as fasting or who may receive Communion, give what the
   Catechism says and point the user to their own parish.

## Without web search

If you have no web search and cannot open a page in this conversation, say so. Keep to the
basics in the package's `VALUES.md`. Do not quote the Catechism from memory as if the wording
were exact, and do not give a paragraph number you have not read. Point the user to the
address above.
