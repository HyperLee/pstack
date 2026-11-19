# Hillclimb

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Define the metric, target, guardrails, budget and stop condition. Freeze a representative harness after **benchmark-checklist** validates it.
2. Record the baseline with method, errors, actual work counts, repeated samples and spread.
3. For each hypothesis, change one thing, run the frozen harness, keep demonstrated wins and back out only your own rejected edits. Use the hillclimb role and independent outputs where useful.
4. Verify each retained unit before the next and log each decision with **show-me-your-work**. Never weaken the metric or harness to manufacture a win.
5. Stop at the target, user budget/stop, or an evidenced dead end. Report accepted/rejected hypotheses, measurements and remaining headroom. PR delivery remains conditional.
