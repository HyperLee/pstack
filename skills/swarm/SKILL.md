---
name: swarm
description: Fan out N parallel workers, drain them, and return one report. Use for $swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration.
---

# Swarm

Read `../poteto-mode/references/codex-runtime.md`. Fan out independent slices or explicitly declared race arms, collect them and return one report.

1. Frame the done predicate, scope, baseline SHAs and expected artifact. Choose partitioned coverage, a race or both. Declare first-pass, rank-all or best-of before a race.
2. Use the `swarm workers` setting and actual capacity. Assign each writer a separate worktree/output. Each brief stands alone: goal, slice, baseline, method, checks and report contract.
3. Spawn workers with the available Codex delegation tool. Batch beyond the concurrency cap. Read-only workers do not edit or drive shared state.
4. Collect PASS, ISSUES or BLOCKED with actual evidence. Reject a report missing its named baseline/method and request one correction from that worker. A second miss or dropout remains a gap, never a pass.
5. Inspect artifacts and aggregate by required slice or the declared race rule. Return findings, commands, coverage gaps and outcome in one concise report.

If delegation is unavailable, execute the slices serially and label that loss of independence. Never claim a parallel run happened when it did not.
