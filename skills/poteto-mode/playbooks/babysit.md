# Babysit a PR or stack

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Read the current PR head, base, checks, review threads and conflicts using available forge tools or gh. Identify the exact outstanding gate.
2. Within the user’s grant, fix proven scoped failures and review comments on their merits. Preserve required checks and authorization boundaries.
3. Use a foreground watch or bundled watch-pr helper when waiting. Do not require Bugbot, start a bot or create a scheduled automation to monitor this job.
4. Re-read the current head/checks after changes. Report merge-ready status and gaps; merge only when explicitly authorized and independently verified through Shipping.
