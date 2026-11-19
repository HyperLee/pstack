# Autonomous run

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Define a falsifiable finish condition and user budget before the first iteration. Read **show-me-your-work**.
2. Use event waits or foreground watcher processes within the current task. Work continues only while its execution environment remains available; do not promise work through machine sleep or invent a loop command.
3. Iterate: hypothesis, smallest justified change, verify actual artifact, retain only supported progress, log a decision. Preserve the agreed bar.
4. Keep working within the grant. Surface material product decisions, unavailable authorization or an evidenced dead end; a plateau earns a new hypothesis, not an invented success.
5. Stop at completion, budget, user stop or a genuine blocker. Return the predicate, evidence, retained/rejected changes and resume point.
