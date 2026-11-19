---
name: arena
description: Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for $arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape.
---

# Arena

Read `../poteto-mode/references/codex-runtime.md`. Produce independent alternatives, choose one base and integrate only the strongest compatible ideas.

1. State the requested artifact. Derive 3–6 task-specific rubric criteria; candidates receive the original task, not the judge's preferred answer.
2. Use the configured `arena runners` list, or two independent inherited-model workers. Give each the same brief and a separate output/worktree. Respect actual capacity; batch if needed.
3. Have a fresh read-only judge score all outputs under neutral labels against the rubric. Use `arena cross-judge pool` when available. Only claim cross-vendor judgment when verified different vendors actually ran.
4. Read every candidate, compare the evidence and choose the easiest coherent design to maintain. Investigate judge disagreement rather than averaging designs.
5. Graft only useful compatible ideas from losing candidates into the base, then verify the synthesized artifact on the matching surface.
6. Report the base, rubric, retained ideas, rejected ideas, dropouts and verification evidence.

Without subagents, explore alternatives sequentially and mark that independent candidate/judge checks did not run. If independence is a required acceptance gate, hand back that gap instead of declaring it satisfied.
