# Runtime forensics

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Keep product changes out of scope unless separately requested. Capture the live symptom with an available matching control tool.
2. Reduce the profile, heap or trace to a concrete hot path, retainer or recurring event. Delegate large independent analysis slices.
3. Test the proposed mechanism through permitted instrumentation and map it to a source symbol/line. Distinguish instrumentation effects from the original symptom.
4. Return the observed signal, mechanism, source and artifacts. Route a requested fix to Bug fix or Perf issue.
