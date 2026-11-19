---
name: poteto-help
description: Guides users through pstack setup, $poteto-mode, and picking the skill, playbook, or principle for a task. Type $poteto-help with a question.
---

# Poteto help for Codex

Resolve this file’s canonical path first and read `../poteto-mode/references/codex-runtime.md`. Answer help questions without starting costly implementation work. A direct request to perform work routes to poteto-mode instead.

Read the relevant installed local source before recommending it. Locate the complete suite using `.pstack-suite.json` beside a copied skill, or two directories above a canonical source skill. The README and `docs/guide/` live at that suite root. Link those local files; the upstream Cursor README is provenance, not Codex usage documentation.

- Installation and model/worker budget: README, guide 01, **setup-pstack**.
- Choose a playbook or word a prompt: guide 02, **poteto-mode**, **sharpen**.
- Understand existing work: guide 03, **how**, **why**, **teach**, **recall**.
- Competing designs and independent coverage: guide 04, **architect**, **arena**, **swarm**, **interrogate**.
- Implementation and cleanup: guide 05, **tdd**, **no-comments**, **typescript-best-practices**.
- Proof, formal checks and requested delivery: guide 06, **create-verification-skill**, **statechart**, **benchmark-checklist**.
- Long tasks, checkpoints and PR queues: guide 07 and **show-me-your-work**. Foreground execution is not guaranteed while the computer sleeps.
- Principles and preferences: guides 08–09, **correct**, **reflect**, **automate-me**.
- Examples and missing-tool behavior: guide 10 and the runtime contract.

Use `$skill-name` in Codex CLI, or the available skill selector in the desktop app. Do not describe Cursor Custom Modes, marketplace install commands or a host `/loop` command as Codex features. Most pstack skills preserve the original explicit-invocation policy; setup-pstack may also be selected from its description.

Return the answer, one suitable example prompt, its local source link and any actual capability limitation. Ask at most one material clarification when the question cannot be resolved from available context.
