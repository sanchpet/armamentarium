# The technical documentation register

## First, name what kind of page this is

Mixing genres is the commonest documentation failure, and no amount of paragraph editing fixes it. A page is one of four kinds, each with its own reader and its own way of failing:

| Kind | Reader | Answers | Fails by |
|---|---|---|---|
| Tutorial | a beginner, learning | "walk me through it" | reference material dropped in; the reader drowns |
| How-to | a practitioner with a task | "how do I do X" | explanation dropped in; the reader hunts for the step |
| Reference | someone who already knows | "what are the fields and what do they mean" | opinions and recommendations dropped in |
| Explanation | someone who wants to understand | "why is it built this way" | steps dropped in; nobody learns why |

**The first action of this pass is to name the kind.** If the draft mixes two, split them and leave a link between. If the kind cannot be named, the page has not been conceived yet — say so out loud rather than smoothing it over with prose.

## The lead sentence

The first sentence says **what this page is and who it is for**. Not "Overview", not "This document describes", not a restatement of the heading.

Bad: "Token rotation setup. In this guide we will look at the process of setting up token rotation."

Good: "How to move ArgoCD off a long-lived ServiceAccount token onto a short-lived one with automatic rotation. You need write access to secrets in the target cluster and a role in AWS Secrets Manager."

The second sentence carries the preconditions: what access is required, what must already exist, and what this page does **not** cover.

## Steps

- Numbered, imperative. "Create", "Check" — not "Next, creation occurs".
- **Every step has an observable result.** "`Ready 1/1` should appear", "the response is `200` with an empty body". A step you cannot tell succeeded is not a step.
- **Every command says what it changes and what it will break.** Blast radius matters more than syntax: the reader can get syntax from `--help`, but nothing tells them the command will silently drop a policy that Terraform put there.
- Placeholders are unambiguous: `<cluster-name>`, `<vault-path>`. **Never substitute a plausible invented value** — it will be copied verbatim.
- A destructive step carries its warning before itself, not after.

## The failure path

Everyone documents the happy path, which is why it is useless: nobody opens the page when things work. **They open it when something broke.**

For every non-trivial step: what the error looks like (the literal text or code), what it means, what to do. If a known failure is silent, say so outright, because otherwise it will not be found: "deleting a policy that does not exist returns 200, so silence here does not mean success."

## The limits of what you know

Documentation lies in two ways: by describing what does not exist, and by staying quiet about what was never checked.

- Mark the unverified as unverified. "Not tested on 1.29."
- Date what will go stale. "Current as of 2026-08, operator 0.9.x."
- State what the page does not cover at the top, rather than letting the reader discover it at step ten.

## Rationale lives elsewhere

Why this design, what the alternatives were, why the obvious option is wrong — that is a decision page, and it gets a link. Inside a how-to, rationale inflates the page and buries the step the reader came for.

One exception: if not knowing the reason would lead someone to skip the step or "improve" it, the reason stays, in a single sentence.

## How documentation reads as machine-written

Separate from the wording blocklist, these are the structural tells specific to documentation:

- "Introduction", "Overview", "Conclusion", "Summary" sections carrying nothing beyond their own heading.
- A "Best Practices" section with advice true of anything and therefore of nothing.
- The first sentence of a section restating the section heading.
- `- **Term**: explanation` applied uniformly, page after page.
- Three-item lists everywhere, where two items carry the content.
- Paragraphs of even length throughout.
- "This guide will walk you through", "Before we begin", "Let's dive in".
- A table where every cell holds one sentence of the same length — the sign it was filled in rather than composed.
- Examples that look like real values but are invented. The most expensive tell on this list: the others waste the reader's time, this one deceives them.

## Voice

Flat and unadvertised. A tool is not "powerful" or "convenient", it does a specific thing.

Concrete with units: "7 to 10 minutes", "three brokers" — not "some time" and "several".

Small qualifications go in parentheses rather than becoming their own sentence.

The page ends where the content ends. There is no closing section.

## Interaction with a house template

This pass owns the **prose**: the lead sentence, the phrasing of steps, the failure path, the stated limits.

It does not own the **page frame**: which sections exist and in what order, the header, the labels, the required fields. Those come from the organisation's template.

Order: this pass first, the house template second. Where a template requires a section this register calls filler — a mandatory "Purpose", say — **the template wins**, but it gets filled according to the lead-sentence rule rather than with generalities.
