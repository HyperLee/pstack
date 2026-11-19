# Feature

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Name the user-visible behavior and done predicate. Inspect the existing design and data shape before code.
2. Trace affected boundaries and run **architect** for a nontrivial interface. Use **arena** only when independent alternatives settle a real choice.
3. Build in small verifiable units, with tests for observable behavior and an isolated delegate when useful. Keep shared state under one owner.
4. Drive the actual product journey with the available verifier, including failure paths and existing behavior that must remain.
5. Report the resulting behavior, checks and proof. Use Opening a PR when requested.
