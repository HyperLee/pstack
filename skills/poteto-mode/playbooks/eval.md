# Evaluate a skill or prompt

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. State the behavior being improved, realistic task, measurable rubric and budget before running. Include an unchanged/no-guidance control.
2. Use isolated outputs with neutral labels and the same input/baseline. Candidate briefs receive the natural task, not the expected answer or evaluation labels.
3. Run independent Codex agents when available, respecting capacity and explicit model access. When independence/model variety is unavailable, report that limitation.
4. Judge all artifacts under the same rubric, inspect outputs yourself and verify claimed chains against actually accessible tool/evidence records.
5. Report outcomes, variance, behavioral evidence, gaps and whether the change is supported. Do not claim a controlled independent eval from a single self-review.
