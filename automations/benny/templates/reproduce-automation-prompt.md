# Benny reproduce invocation / unconnected scheduler template

Status: UNCONNECTED. Use this as a manually supplied request after filling actual configuration and source coordinates. It does not register a Slack event trigger or schedule.

Read `.codex/automations/benny/FOR_AGENTS.md`, then `.codex/automations/benny/skills/reproduce-and-fix-issues/SKILL.md` from the target repository. Supply the actual external configuration path. The operational file owns the workflow and gates.

```json
{"source":{"channel_id":"C123","thread_ts":"1795016545.000001","message_ts":"1795016545.000001"}}
```

Resolve an optional permalink through an available connector and validate all coordinates before work. Read the real original thread to confirm identity. Freeze channel/root throughout. State the user's actual grants for thread replies, tracker writes and any draft PR separately; absent grants mean in-chat proposals only. Workers receive no posting capability or credentials. Missing required input/tool means no external writes.

A future scheduled adapter must provide durable event IDs/checkpoints, deduplication, overlap control and bounded retries. No such service is included. Use supported Codex automation tools only after an explicit recurring-task request and verification of that input adapter.

An operations-channel status thread is optional and disabled by default. Name that channel and the user's separate posting/edit grants before enabling `permissions.allow_operations_posts` or `permissions.allow_operations_edits`. Without those grants and flags, keep status and follow-ups in the current chat. A configured channel alone is not permission to post.
