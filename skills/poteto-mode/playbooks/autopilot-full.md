# Autopilot-full

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Confirm explicit grants for the fixed queue, PR creation/push and merge. A request for a plan is not execution or merge permission.
2. Give each independent PR one owner in an isolated worktree/branch. The owner uses the normal build, verification and Babysit playbooks and records a decision trail. Include later corrections in every follow-up.
3. Use independent verifiers at the code-ready baseline/head. Inspect their actual evidence. New behavior or a major diff needs renewed coverage; any changed patch needs checks appropriate to that change.
4. Merge only after independent proof and current required forge checks cover what will land. Rebase/retarget only when necessary, verify the resulting context, and respect all server-enforced approvals.
5. Coordinate in the current task with native waits/watchers. Audit owner progress from artifacts and record gaps. Replace only an evidenced failed/stuck worker, preserving its branch and brief.
6. A stop reaches all owners as a no-write hold. Report each PR, actual verdict, merged state, remaining user gates and trail links. Never widen the queue.
