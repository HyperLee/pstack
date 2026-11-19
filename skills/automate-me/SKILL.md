---
name: automate-me
description: Use when creating or updating a personal working-style skill from the user's confirmed preferences and relevant accessible conversation history, including requests to automate me or refresh a personal mode.
---

# Automate me

Read `../poteto-mode/references/codex-runtime.md`. Create or update a personal `-mode` skill from the user's actual working preferences.

Find an existing mode in project/user skill locations. For an update, preserve uncontradicted choices. Use the current conversation and relevant accessible project history, or user-specified exports. Do not scan unrelated chats or guess internal transcript paths. Confirm only preferences that materially affect the result; distinguish repeated evidence from a one-off.

Use the available **skill-creator** to author a concise skill under project `.agents/skills/<handle>-mode/` or the personal skill location the user selects. Keep triggers specific to that user/style, not generic coding. Follow the creator's current invocation-policy guidance; do not impose an explicit-only rule without the user's choice. Write in the language and voice the user asks for.

Show the draft when preference approval is needed, apply **unslop**, validate, and test the meaningful behavior. Opening a PR is conditional on the requested delivery. Do not persist preferences to unrelated memory/configuration or modify cached plugin files.
