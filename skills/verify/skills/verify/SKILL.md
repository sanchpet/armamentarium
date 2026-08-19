---
name: verify
description: "Verify a finished result against a standard using a fresh sub-agent with context isolation — it checks the RESULT, not the process that produced it. Types: code / chain / adversarial. Use before calling something done; trivial work does not need it."
argument-hint: "[code|chain|adversarial|auto] [path or target]"
---

# Verify the result

The point is context isolation. The sub-agent checks the artifact against a standard **without seeing how it was made**, so it cannot anchor on the author's reasoning. A verifier that read the author's chain of thought is a rubber stamp.

Arguments: $ARGUMENTS

## Step 0 — pick the check

| Argument | What it checks |
|----------|----------------|
| `code` | Logic, edge cases, secrets and PII, coupling, whether tests assert an observable result |
| `chain` | Data flow: were the downstream consumers of every changed output actually read, and do the contracts still match |
| `adversarial` | Scope and bias, pre-mortem: was the scope derived or fitted, what was never read, where this breaks in production |
| `auto` / empty | Infer from the argument: a source file → `code`; several files across components → offer `chain`; straight after a fix → offer `adversarial` |

## Step 1 — assemble the input (orchestrator)

- **code:** `git diff` or the named files, plus the conventions of the repo being touched (`CLAUDE.md`, linter config, the surrounding code), plus the code checklist.
- **chain:** `git diff`, plus a grep for every consumer of the changed functions and outputs, plus the text of each consumer.
- **adversarial:** `git diff`, plus the list of files the author did **not** read but that the change can reach, plus the original task description.

## Step 2 — run the sub-agent

Spawn the sub-agent with only the input from step 1. It does **not** receive the session history, the original instruction to the author, or any intermediate reasoning. Artifact, standard, checklist — nothing else.

**The standard** is what the result is measured against: for `code`, the repo's own conventions; for `chain` and `adversarial`, the code itself. **If no standard can be named, stop.** What is wanted then is a reviewer with taste, not a verifier, and pretending otherwise produces confident noise.

Checklists:

- **code** — Is the logic right? Are the edge cases handled? Any secrets, PII, or injection? Is the coupling justified? Does each test assert something observable rather than restating the implementation?
- **chain** — Who consumes each changed output? Was every one of them read? Do the types and formats still line up? Are the variables and environment names defined in scope? Is the contract intact?
- **adversarial** — Did the scope come from analysis or was it fitted to a conclusion? What was not read but is reachable? Name three ways this breaks in production. What are the alternative explanations for the original problem? Does the claimed scope ("one file", "simple fix") match the real one?

## Step 3 — verdict

The sub-agent returns:

- **PASS** (no critical, no high), **CONDITIONAL** (no critical, at least one high), or **FAIL** (at least one critical).
- A table of findings: severity, file, line, what, why, and the standard it violates.
- A severity summary and a recommendation of one to three sentences.

## Step 4 — hand it back

Show the verdict. Accepting it, fixing against it, or rejecting it with an argument is the author's call. A disputed verdict is not pushed through.
