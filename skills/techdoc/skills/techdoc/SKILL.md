---
name: techdoc
description: |
  Rewrite a draft into the technical documentation register: name the kind of
  page, lead with what it is and who it is for, make every step verifiable,
  document the failure path, and strip the structural tells of generated
  prose. TRIGGER: when writing or revising a runbook, how-to, reference page,
  README, architecture note, wiki or Confluence page, or when asked to clean
  up documentation. DO NOT TRIGGER for: blog posts, PR and issue prose, chat
  messages, commit messages, code comments.
---

# Rewrite into the technical documentation register

This is not a personal voice. Documentation gets opened at three in the morning during an incident, and the reader needs the command and its consequence, not a narrative.

Works on Russian and English drafts alike: the register is language-independent, the final blocklist is picked by language.

## Hard rules

1. **No invented specifics.** Every value, version, path, flag, and error string comes from the source material. An invented example that looks real is the worst defect this skill can introduce, because it will be copied verbatim into a live system. If a concrete value would make the page usable and you do not have it, leave a marked placeholder and say what is missing.

2. **Do not document what you have not seen.** If the draft asserts behaviour that the material does not establish, mark it unverified rather than smoothing it into a confident sentence. Confident documentation of unverified behaviour is worse than an admitted gap.

3. **Do not add rationale the source does not carry.** Guessing why a design is the way it is produces plausible history that later gets cited.

4. **Cut, do not pad.** If a section carries nothing beyond its heading, delete the section. Word count is not the deliverable.

## Process — three passes, in this order

### Pass 1 — kind and shape

Read `references/register.md`. Name which of the four kinds of page this is: tutorial, how-to, reference, explanation. If the draft mixes two, split them.

Then rebuild the skeleton: lead sentence, preconditions, steps with observable results, the failure path, the stated limits of what is known. Rationale moves out to a linked decision page unless its absence would make someone skip or "improve" a step.

**Do not open the blocklist yet** — writing against a list of banned words plants those words.

### Pass 2 — structure

This is the layer that actually removes the machine-written feel.

- Every step has a result the reader can observe. Rewrite any that does not.
- Every command states what it changes and what it breaks.
- Break even paragraph lengths and uniform list sizes. Two items stay two; never pad to three.
- Remove sections that restate their own heading.
- No closing section. The page ends where the content ends.
- Destructive operations carry their warning before themselves.

### Pass 3 — final edit (only now)

Open `references/blocklist-ru.md` or `references/blocklist-en.md` by the language of the text and remove every hit.

Then answer one question: "what would still tell a reader this was generated?" Fix that one thing and stop. Do not iterate further — over-editing smooths the page back into a house style.

## Where this pass stops

It owns the prose: the lead sentence, the phrasing of steps, the failure path, the stated limits.

It does not own the page frame: which sections exist and in what order, headers, labels, required fields. Those belong to the organisation's template, and a template-driven pass runs **after** this one. Where a template requires a section this register would call filler, the template wins — but the section is filled by the lead-sentence rule, not with generalities.

## Output

Return the rewritten page only. If you marked anything unverified or left a placeholder, list those separately below the page so they can be resolved.
