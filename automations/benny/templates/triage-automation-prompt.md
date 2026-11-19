# Benny triage invocation / unconnected scheduler template

Status: UNCONNECTED. Use this as a manually supplied request after filling actual configuration and source coordinates. It does not register a Slack event trigger or schedule.

Read `.codex/automations/benny/FOR_AGENTS.md`, then `.codex/automations/benny/skills/triage-issue-reports/SKILL.md` from the target repository. Supply the actual external configuration path. The operational file owns the workflow and gates.

```json
{"source":{"channel_id":"C123","thread_ts":"1795016545.000001","message_ts":"1795016545.000001"}}
```

Resolve an optional permalink through an available connector and validate all coordinates before work. Read the real original thread to confirm identity. Freeze channel/root throughout. State the user's actual grants for thread replies, tracker writes and any draft PR separately; absent grants mean in-chat proposals only. Workers receive no posting capability or credentials. Missing required input/tool means no external writes.

A future scheduled adapter must provide durable event IDs/checkpoints, deduplication, overlap control and bounded retries. No such service is included. Use supported Codex automation tools only after an explicit recurring-task request and verification of that input adapter.
