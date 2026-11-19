# Trace forensics

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Identify the supplied capture format; treat that fixed artifact as the dataset instead of taking a different capture.
2. Transform large data to a queryable representation and narrow to dominant frames, retainer chains or blocked threads. Use independent analysis delegates for large slices.
3. Resolve symbol/source attribution. Compare paired captures when present; otherwise label the result as the strongest supported hypothesis.
4. Return a cited diagnosis, limitations and artifact paths. Do not implement a fix unless asked.
