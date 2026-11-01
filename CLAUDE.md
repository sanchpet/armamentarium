# CLAUDE.md

## What this is

`armamentarium` — the public half of a two-repository Claude Code plugin marketplace. No application code, only plugin definitions. The private half is `armamentarium-privatum`; anything carrying personal data belongs there, not here.

## The public/private boundary

A plugin belongs here only if all three hold:

1. It carries no personal data — no voice samples, no personal infrastructure, no private conventions.
2. It works outside the owner's vault. A skill that reads vault paths, invariants, or ADR numbers is vault machinery and stays in the vault.
3. It is written in English. The vault's own skills are Russian; moving one here is a translation and a decoupling, not a copy.

## Adding a plugin

1. Create the directory under `skills/`, `hooks/`, or `mcp/`.
2. Add `.claude-plugin/plugin.json` with name, version, description, author.
3. Add the content: `skills/<skill>/SKILL.md`, or `hooks/hooks.json` plus `scripts/`.
4. Register it in `.claude-plugin/marketplace.json`. The description must match `plugin.json` exactly.
5. Add a row to the README table.
6. Bump the version of any plugin whose content changed — one bump per branch, not per commit.

## Conventions

- All content in English.
- Branch and PR from the first change; no committing straight to `main`.
- Commits carry `--signoff`.
