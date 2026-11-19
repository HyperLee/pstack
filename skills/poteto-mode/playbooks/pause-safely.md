# Pause safely

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Honor an explicit pause/stop promptly and propagate it to all delegates.
2. Stop at a safe boundary. Preserve the user’s edits and current evidence; terminate only processes this run owns. Never delete scratch directories as cleanup.
3. Record branch/worktree, pending diff, running or stopped workers, decisions, checks and next step in a resume note. Commit/push a checkpoint only if the user’s grant covers it.
4. Report what was preserved and how to resume. A normal “keep going” request does not trigger this playbook.
