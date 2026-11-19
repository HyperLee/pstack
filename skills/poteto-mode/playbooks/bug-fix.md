# Bug fix

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Reproduce the symptom on the real matching surface before editing. Save the failing command, baseline and expected behavior.
2. Trace the first wrong decision with **principle-fix-root-causes**, not a convenient downstream symptom.
3. Use **tdd** when a focused regression check is practical. Implement the smallest root-cause change; a delegate uses the bug-fix role and an isolated baseline.
4. Run the repro again plus relevant checks and blast-radius smoke. Keep before/after evidence. A build alone is not proof.
5. Deliver the verified diff, root cause, tests and residual gaps. Use Opening a PR only when PR delivery is requested.
