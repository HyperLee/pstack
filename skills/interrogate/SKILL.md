---
name: interrogate
description: Use for "interrogate", "adversarial review", "multi-model review", "challenge this", "stress test this code", "find blind spots", or "tear this apart". Adversaries try to break a change or design, and only findings proven by a run survive.
---

# Interrogate

Read `../poteto-mode/references/codex-runtime.md`. Review the user's scope without applying fixes. By default inspect the branch diff from its merge base through the working tree.

State the intent. Give independent reviewers the same baseline, complete scoped diff including uncommitted changes, and isolated outputs. Use `interrogate reviewers` or two inherited-model agents. Ask them to prove concrete failures on real code with the exact command, actual output and expected behavior. A design-only review may use a probe in its own scratch directory when the user permits it.

Rerun each reported reproduction. Keep failures that break the intent; merge findings sharing a root cause. Drop unproven claims and explain the gaps. Report intent, verified findings, commands/evidence and dropped counts. No findings is valid. No independent tools means an explicitly labeled single-agent review, not a fabricated panel.
