---
name: setup-benny
description: Configure the optional Benny direct-read workflows for manual Codex execution and prepare unconnected scheduler integration templates.
---

# Set up Benny

Read the pack's `../../FOR_AGENTS.md` first. These operational files are not generally discovered skills.

1. Identify the target repository and complete pstack suite. If copying this pack to `.codex/automations/benny/`, preserve destination-only files and merge source-managed conflicts after reviewing differences. Keep configuration outside the pack. Do not change Codex/legacy plugin settings.
2. Verify shared skills resolve from the target's complete suite: why, tdd, unslop and the principles referenced by the operational files. Do not rely on this chat's loaded context as proof of a fresh install.
3. Adapt `../../templates/configuration.example.yaml`, the routing map and feature map into `.codex/benny/` or another explicit user-owned path. Fill real repository/tool references; no credentials or guessed model IDs.
4. Confirm manual input uses channel_id, thread_ts and message_ts strings. Validate with the pack's source.py, then use the configured read connector to confirm the original thread and message membership. If only a permalink was supplied, resolve it with that connector first.
5. Check actual capabilities for Slack reads/thread replies, the selected tracker, repository access and app control. Default all external writes to disabled. Source-thread posts, operations-channel posts/edits, tracker writes and draft PRs each require their corresponding flags and actual user grants. A configured operations channel alone enables nothing; otherwise status stays in chat. Missing required capability stops that lane without side effects.
6. A manual triage request reads `../triage-issue-reports/SKILL.md`. A manual repro request reads `../reproduce-and-fix-issues/SKILL.md`. Pass the configuration path and immutable source object, not a fabricated native trigger.
7. Keep scheduler/event prompts as unconnected templates. A later explicitly requested integration must first implement the input adapter, durable event dedupe/checkpoints, overlap policy and bounded work. Only then use the available supported automation tool. Do not create a recurring automation to watch one current PR/job.
8. Validate against isolated test fixtures/fake connectors before any authorized live test. Confirm thread-only routing, no worker posting capability, bounded fix attempts, draft-only PRs and retained evidence. This setup does not itself post, create issues/PRs or enable schedules.

Source artifacts/configuration must be committed together when a future remote runner needs them. Local source/cache paths are not valid references for another machine. Respect the repository's own review and delivery requirements.
