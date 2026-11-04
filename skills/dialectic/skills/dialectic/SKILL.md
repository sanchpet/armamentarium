---
name: dialectic
description: "The blind solver and discriminator method for a decision that is not obvious or short of arguments: a fresh solver gets the task without your options, a discriminator checks both positions against the code and the measurements, and the answer is a synthesis in which both positions are special cases (the first law of dialectics, Weinberg's Rule of Three, Beck's triangulation). For a responsible decision, role agents then try to refute the synthesis. Use it when choosing or synthesising between designs, when a decision would be irreversible or changes a public contract, or when you notice you are defending the first idea you had."
argument-hint: "[the decision and the material it rests on]"
---

# Blind solver and discriminator

Task: $ARGUMENTS

Use this when the answer is not obvious and the arguments for one option are thin. Two agents, a blind solver and a discriminator, apply the first law of dialectics and The Rule of Three by Gerald M. Weinberg (The Secrets of Consulting) to find, by choice or by synthesis, the best decision.

The point is completeness of viewpoints, that is of decision criteria, as in Kent Beck's triangulation in TDD. One example, `plus(3, 1) = 4`, is passed by the fake `return 4`. A second example with a different answer, `plus(3, 4) = 7`, exposes the contradiction, and what resolves it is not picking one of the answers but the generalisation `a + b`, of which both are special cases: a synthesis. The rules below follow from that. A second agent given our framing is the same example again: it forces nothing. The solver gets the task, not our options, otherwise its example coincides with ours. The discriminator checks the examples' answers against the facts: a wrong answer forces a wrong generalisation. And whatever both examples share stays unforced: both take `a = 3`, and `3 + b` passes them as well as `a + b`, which is why the premises the task calls settled are proven again.

## Rules

- The solver gets the task, never our conclusion and never our options. "We are choosing between A and B" hands it the frame that made A and B the only candidates. The discriminator gets both positions, the solver's and ours, and checks their claims against the code, the spec and the measurements.
- The solver agreeing with us is an argument only when the task could have split us: the example `fib(2) = 1` is passed by the fake `return 1` too. So on agreement the discriminator names the alternative the agreement excluded; if it cannot name one, the agreement proved nothing.
- The synthesis is not invented as a third option: each position is re-read as a special case, what it really means, which property it serves. In Beck's derivation of Fibonacci: "we wrote 2, but we mean 1 + 1", and those ones are `fib(n-1)` and `fib(n-2)`. The decision is the structure of which both positions turn out to be special cases.
- The premises the task calls settled are proven again too: an agent that was not told to doubt them does not check them.
- The agents are fresh, not forks of the current session (a fork inherits our context and with it our frame), on the strongest model available.
- The agents only read: they do not build, do not create worktrees, do not write to a repository or a database, no DDL and no DML, not even `IF EXISTS`. A measurement on a database is a `SELECT` or an `EXPLAIN`.

## Procedure

1. **Brief the solver** with the task, the material to read (paths, documents, measured facts) and the constraints that bind. Ask for a concrete mechanism, its failure cases and what it does in each, the premises it re-verified or would need to, and what it would not do and why. Tell it to decide, not to ask.
2. **Brief the discriminator** with the task, the solver's answer verbatim and our position verbatim, with the same material. Ask it to check every claim of both against the code, the spec and the measurements, to name where the two positions are special cases of one structure, and, where they agree, to name the alternative the agreement excluded.
3. **Synthesise.** Re-read each position as a special case; write the structure that holds both; keep what the discriminator confirmed, drop what it refuted. Say what changed from our original position and why.

## Refutation by roles

For a responsible decision, one that changes the public API of a core or a library, a contract on the wire, a schema or a migration of live data, a security or tenant-isolation boundary, a locking or transaction protocol, or one that is irreversible, the synthesis is additionally attacked by role agents. The roles are chosen by the decision, not all of them every time:

- Software Design / DDD: boundaries, invariants, language;
- Distributed Systems: ordering, idempotency, failure half-way;
- Database: plans under RLS, locks, migrations;
- Performance: the scale of production, not of the test stand;
- Security: isolation, leaks, authorisation bypass;
- Operability: retries, parking, observability, recovery;
- Evolution: compatibility of contracts, rollback;
- Verifiability: who executes the decision, and the mutation that breaks it.

Each agent gets the task, the decision and the code, and tries to refute the decision from its position. A finding is accepted only as a failure scenario (inputs and state, then the wrong result) with a reference to the code, the spec or a measurement, or as a measurement to be taken; "no findings" is a valid answer. These agents only read, like the solver and the discriminator. Contradictions between the findings and the decision are synthesised by the first law of dialectics and Weinberg's Rule of Three, and every accepted finding gets an executor.

**Output:** the synthesis, the positions it holds as special cases, the premises re-proven and the ones found wrong, the accepted findings with their executors, and the residual uncertainty.
