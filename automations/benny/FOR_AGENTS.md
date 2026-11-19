# Benny for Codex: operating contract

This optional pack is read directly, not registered in `.agents/skills`. Read `skills/setup-benny/SKILL.md` here when the user requests setup. The default mode is a manually invoked run, not a live Slack event automation.

The pack has two workflows: triage one supplied Slack report, then reproduce a trusted triaged bug and optionally prepare a bounded draft fix. Reading a template does not authorize any post, tracker write or PR creation. Obtain those grants from the actual task; preserve existing explicit grants.

## Input contract

The caller supplies external configuration and one immutable `source` object:

```json
{"channel_id":"C123","thread_ts":"1795016545.000001","message_ts":"1795016545.000001"}
```

An optional `permalink` can accompany those fields. Resolve a permalink through an available read connector before deriving coordinates; never guess them. Timestamps stay strings. Validate shape with `python3 scripts/source.py EVENT.json --channel CONFIGURED_CHANNEL`, then read the real thread to confirm the root, message membership and configured channel. Shape validation alone is not authorization or proof that a thread exists.

Freeze channel/root for the whole run. A follow-up message timestamp never replaces the root. Fail closed without external writes if coordinates, configuration, tools, or authorization are absent/uncertain. Only the coordinator posts. Source-channel posts stay in the original thread and require `permissions.allow_slack_posts` plus the user's grant. Never supply Slack credentials or posting capabilities to workers; when isolation cannot enforce that, the coordinator does the work serially.

The repro workflow's optional operations-channel status is a separate lane. A configured operations channel alone grants nothing. Creating its status thread or replying there requires both `permissions.allow_operations_posts: true` and explicit permission for that named channel. Editing its status additionally requires `permissions.allow_operations_edits: true` and the matching edit grant. These flags default to false. Without them, keep all operations status/follow-ups in the current chat and do not create an operations thread. These grants never authorize a source-channel root post, a DM or a different destination. Triage still posts only its one authorized source-thread verdict.

Use a complete project pstack install for shared skills. The suite root is canonical; consult `skills/poteto-mode/references/codex-runtime.md` there. Keep user-owned configuration outside the copied pack, normally `.codex/benny/`. Do not overwrite destination-only/local configuration when refreshing.

## Future scheduler integration

Scheduled and Slack-event templates are UNCONNECTED in this port. No polling service, webhook receiver or durable checkpoint store is provided. A later integration must supply a verified event adapter, durable event IDs, checkpoint ownership, deduplication/idempotent writes, overlap handling and bounded polling before enabling a schedule. Use actual available Codex automation tools only when the user explicitly requests a recurring task. A recurring prompt alone cannot manufacture a Slack trigger envelope.

Do not merge or deploy. Draft fixes require the operational repro/fix gates and explicit authorization. Stop owned app processes, retain evidence and temporary directories, and hand directory cleanup to the user.
