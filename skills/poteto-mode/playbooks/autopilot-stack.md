# Autopilot-stack

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Use Autopilot-full’s isolation, ownership and independent verification, with a no-merge grant.
2. Stack a PR only when it depends on another queued patch; otherwise branch from trunk independently.
3. Stop when each requested PR is verified and its current checks pass. Report the dependency order and evidence for the user to review. Do not push again after handoff without a new instruction.
