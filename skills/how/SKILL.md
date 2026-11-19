---
name: how
description: Use for "how does X work", code walkthroughs before changing something, and placement / ownership / layering questions ("where should this live", "which package owns this", "is this the right layer"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation.
---

# How

Read `../poteto-mode/references/codex-runtime.md`. Trace the subsystem and answer the user's actual question, at the level of an engineer who needs to work in this code.

Use one read-only Codex subagent for exploration and explanation when available. Give the question, scope, source entry points and a no-edit brief. Otherwise perform the same read-only investigation directly. Explain ownership, runtime flow, types and non-obvious boundaries with source citations. Preserve the investigator's evidence and uncertainty. Use **why** for historical motivation.
