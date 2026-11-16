# armamentarium

The owner's agentic toolset in one Claude Code marketplace: own reasoning and verification skills, plus open-source plugins referenced upstream at a pinned commit. One marketplace to add, one list to read.

The private counterpart, `armamentarium-privatum`, holds the plugins that cannot be published: voice profiles built from the owner's own writing, and personal infrastructure conventions.

## Install

```
/plugin marketplace add sanchpet/armamentarium
/plugin install think@armamentarium
```

## Own plugins

| Plugin | What it does |
|---|---|
| `think` | Structured reasoning through the ADI cycle: abduction, deduction, induction, audit, decide. For decisions with more than one plausible answer, where the risk is anchoring on the first idea. |
| `dialectic` | The blind solver and discriminator method for a decision that is not obvious: a fresh solver gets the task without your options, a discriminator checks both positions against the code and the measurements, and the answer is a synthesis of which both are special cases. For a responsible decision, role agents then try to refute the synthesis. |
| `verify` | Runs a fresh sub-agent against a finished artifact with context isolation, so it judges the result rather than the reasoning that produced it. Types: `code`, `chain`, `adversarial`. |
| `techdoc` | Rewrites a draft into the technical documentation register: names which of the four kinds of page it is, leads with what the page is and who it is for, makes every step verifiable, documents the failure path. Owns the prose, not the house template — a template-driven pass runs after it. |

## Upstream plugins

Referenced, not copied: `marketplace.json` names the upstream repository, the tag and the commit, and Claude Code fetches the plugin from there at that commit.

| Plugin | Upstream | Pinned | Runs code outside the pin |
|---|---|---|---|
| `modern-web-guidance` | [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) | `v1.0.0` | Yes: every search runs `npx modern-web-guidance@latest`, the newest npm release, whatever the pin. |
| `codex` | [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) (`plugins/codex`) | `v1.0.6` | Hooks on session start, end and stop run its bundled scripts; the scripts are pinned, the Codex CLI they call is not. |

The last column is where the pin stops protecting: a plugin that fetches or calls code at run time executes whatever that code is today.

### Updates

`bump-upstream` runs every Monday (and on demand). For each upstream plugin it finds the newest tag, moves the pin, and opens one PR listing, per plugin, the compare link and the changed files that run code or steer the agent (`SKILL.md`, hooks, MCP, agents, commands, scripts). Merging the PR is the update; nothing reaches the agent before that.

Repository setting it relies on: Actions may create pull requests.

## Layout

Own plugins are grouped by their primary component type. A plugin is a directory with `.claude-plugin/plugin.json` and its content next to it: `skills/<skill>/SKILL.md` for skills, `hooks/hooks.json` plus `scripts/` for hooks. The registry is `.claude-plugin/marketplace.json`; upstream plugins exist only there.

## Validation

`claude plugin validate .` at the root checks manifests and `source` syntax; the per-plugin form also parses frontmatter. Neither checks that a `source` resolves, so a renamed directory or a moved upstream path is caught only by installing: `CLAUDE_CONFIG_DIR=$(mktemp -d) claude plugin marketplace add . && claude plugin install <plugin>@armamentarium`.
