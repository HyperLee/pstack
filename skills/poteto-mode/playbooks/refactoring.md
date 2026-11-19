# Refactoring

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Pin current behavior with a characterization/equivalence check before changing structure. Separate discovered new behavior or bugs from this task.
2. Name the target data shape, ownership and boundaries. Use **architect** where a nontrivial boundary changes.
3. Remove dead weight, migrate callers and remove replaced internal APIs in small steps. Preserve externally required compatibility. Give mechanical delegates explicit files and baseline.
4. Keep the pin green after each unit and prove equivalence on the real artifact. Keep only changes that reduce reader load.
5. Report the structure change, contract and equivalence evidence. Use Opening a PR when requested.
