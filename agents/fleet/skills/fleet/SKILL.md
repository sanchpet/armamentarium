---
name: fleet
description: "Set up and run a fleet of coordinating Claude Code sessions — a lead, project leads, and ICs — with one reporting discipline across every project. Covers what a fleet costs, when a single session is better, how the levels are actually built, and what each level owes the one above. Use when several projects run in parallel and the human's attention is the bottleneck."
argument-hint: "[plan|activate|charge <project>]"
---

# Run a fleet

A fleet is worth it when **your attention**, not the machine's throughput, is what limits the work. Below that, it costs more than it returns: every session is a separate context window, coordination overhead grows faster than parallelism pays, and three focused workers beat five scattered ones.

Arguments: $ARGUMENTS

## Before anything: is this a fleet task?

A fleet earns its cost on work that splits into independent pieces — parallel review under different lenses, competing hypotheses, separate modules, research across sources. It loses on sequential work, on edits to the same files, and on anything with a dependency chain. There, one session or a handful of subagents is better.

Say so plainly when the answer is no. Building the machinery anyway produces something that looks like capability and is only cost.

## How the levels are actually built

The hierarchy is **not** one team. Two constraints decide the shape:

- a teammate cannot spawn teammates;
- a session has exactly one team.

So each level that needs workers of its own must be its own session. Teammates are the leaves.

| Level | What it is | How it is created |
|---|---|---|
| Lead | Coordinates projects, reports to the human | A long-lived session, backgrounded so it can be restarted |
| Project lead | Owns one project's task list | Its own session, dispatched by the lead |
| IC | Does one scoped task | A teammate of its project lead |

Two peer leads that watch each other need a **watchdog on the roster**, not a conversation: read `claude agents --json`, restart a missing background session, and send one message with context. Mutual "are you alive" pings are dropped as repeats and refused as bursts.

## Activation

Teammates are experimental and off by default. Enable them per project, in that project's own settings — never globally:

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" },
  "crossSessionInbound": "accept" }
```

Both keys are load-bearing. While teams are enabled, a subagent that gets a name launches as a teammate, so a flow that waits on a subagent's returned result stalls — which is why this belongs to the projects that want a fleet and not to every repository you open. And without `crossSessionInbound: "accept"`, a session that skips permission prompts holds incoming messages for a human click that a fleet is not there to collect.

## The reporting discipline

This is the part that must be identical across projects, whatever each one's subject is.

1. **A work unit exists only with a demonstrable artifact.** A commit, a config, a running service, a document, a measurement with a conclusion. "Looked into it" is not one. A task that cannot name its artifact is not ready to be assigned.
2. **Evidence travels upward, verdicts do not.** An IC reports the command and its output, or `file:line`. A project lead rejects a verdict without evidence rather than passing it on.
3. **A claim about behaviour needs a run.** Reading a rule or a config supports a claim about the text. Anything phrased as "blocked", "impossible", or "already handled" is about behaviour and needs a command that made the system behave.
4. **State outlives the session.** Every unit keeps a record that a later session can resume from: what was tried, what proved it, where it stopped, what to do next. The host repository declares where those records live and what they are called; this skill does not — read the repository's own instructions for that, and if it declares nothing, ask before inventing a location.
5. **Each unit traces to a parent.** A task names its project; a project names the goal it serves. An untraceable unit is work nobody asked for.

## What each level owes

- **IC → project lead:** the artifact, the evidence, and the gap — what it did not read but could reach.
- **Project lead → lead:** only what changes the plan. Progress is not news.
- **Lead → human:** one message per project — state, blocker, decision needed.

## Cost

Every teammate is a full session with its own context window, so usage scales with the number of active workers, not with the number of prompts you type. Start at three to five workers per project. Scale up only after the work has shown it splits cleanly.
