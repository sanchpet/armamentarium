# CLAUDE.md

## What this is

`armamentarium` — the public marketplace of the owner's agentic toolset: own plugins, plus open-source plugins referenced upstream at a pinned commit. No application code beyond the pin-bump script. The private half is `armamentarium-privatum`; anything carrying personal data belongs there, not here.

## Own plugins: the public/private boundary

An own plugin belongs here only if all three hold:

1. It carries no personal data — no voice samples, no personal infrastructure, no private conventions.
2. It works outside the owner's vault. A skill that reads vault paths, invariants, or ADR numbers is vault machinery and stays in the vault.
3. It is written in English. The vault's own skills are Russian; moving one here is a translation and a decoupling, not a copy.

## Adding an own plugin

1. Create the directory under `skills/`, `hooks/`, or `mcp/`.
2. Add `.claude-plugin/plugin.json` with name, version, description, author.
3. Add the content: `skills/<skill>/SKILL.md`, or `hooks/hooks.json` plus `scripts/`.
4. Register it in `.claude-plugin/marketplace.json`. The description must match `plugin.json` exactly.
5. Add a row to the README table.
6. Bump the version of any plugin whose content changed — one bump per branch, not per commit.

## Adding an upstream plugin

1. Read it before adding: the `description` of every skill (it decides when the skill fires), hooks, MCP servers, agents, and anything it fetches or runs at run time. It needs a license.
2. Register it in `marketplace.json` by reference, never by copying files: `{"source": "github", "repo", "ref", "sha"}` when the plugin is the repository root, `{"source": "git-subdir", "url", "path", "ref", "sha"}` when it sits in a subdirectory. `ref` is a tag, `sha` the commit it points to; the bump script tracks tags.
3. Take `description` from the upstream `plugin.json` verbatim and set `license`.
4. Add a row to the README's upstream table, including what it runs outside the pin.
5. Prove it installs into a throwaway config dir (see Validation in the README).

Pins move only through the `bump-upstream` PR or a deliberate PR by hand, never by editing `main`.

## Conventions

- All content in English.
- Branch and PR from the first change; no committing straight to `main`.
- Commits carry `--signoff`.
