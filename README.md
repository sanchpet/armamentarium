# armamentarium

Public marketplace of Claude Code plugins. Reasoning and verification skills that carry no personal data and work in any repository.

The private counterpart, `armamentarium-privatum`, holds the plugins that cannot be published: voice profiles built from the owner's own writing, and personal infrastructure conventions.

## Install

```
/plugin marketplace add sanchpet/armamentarium
/plugin install think@armamentarium
/plugin install verify@armamentarium
```

## Plugins

| Plugin | What it does |
|---|---|
| `think` | Structured reasoning through the ADI cycle: abduction, deduction, induction, audit, decide. For decisions with more than one plausible answer, where the risk is anchoring on the first idea. |
| `verify` | Runs a fresh sub-agent against a finished artifact with context isolation, so it judges the result rather than the reasoning that produced it. Types: `code`, `chain`, `adversarial`. |

## Layout

Plugins are grouped by their primary component type. A plugin is a directory with `.claude-plugin/plugin.json` and its content next to it: `skills/<skill>/SKILL.md` for skills, `hooks/hooks.json` plus `scripts/` for hooks. The registry is `.claude-plugin/marketplace.json`.

Adding one: create the directory, write `plugin.json`, write the content, register it in `marketplace.json`, add a row above.

## Validation

`claude plugin validate .` at the root checks manifests and `source` path syntax; the per-plugin form also parses frontmatter. Neither checks that a `source` points at a directory that exists, so a renamed or deleted plugin is caught only by hand.
