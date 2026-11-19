# Perf issue

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. State the measured symptom and metric. Capture a baseline on the actual path; apply **benchmark-checklist** before trusting it.
2. Capture a profile/trace and identify the limiting resource or hot path. Explain why the result is plausible.
3. Make one smallest justified improvement, using the perf-issue role for delegated work. Verify each attempt before another.
4. Repeat equivalent before/after measurements with errors, work counts, variation and end-to-end impact. An untuned or skipped-work result is inconclusive.
5. Report baseline, result, delta, method and evidence. For sustained optimization use Hillclimb; use Opening a PR when requested.
