# Visual parity

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Capture an unchanged reference across relevant states before migration. Pin the screenshot/image-diff harness; baseline changes require the user’s decision.
2. Migrate independent components in isolated worktrees, shared primitives first. Do not change the harness to make a component pass.
3. Drive each state on the matching surface and measure image differences. Diagnose every nonzero delta; if zero is the agreed target, a nonzero result fails.
4. Report each component, baseline, measured difference and outstanding gaps. Use Opening a PR only for requested delivery.
