---
name: setup-pstack
description: Configure pstack's project or personal JSON profile for model inheritance, supported per-role overrides, reasoning budget and worker limits. Use for $setup-pstack or requests to change pstack settings.
---

# Set up pstack for Codex

Read `../poteto-mode/references/codex-runtime.md` for the profile schema and role names. Setup is optional; with no profile, pstack inherits the chat model and reasoning and uses up to three workers.

1. Inspect the current project's profile, then the personal profile, and the actual model/tool capabilities. Never invent entitled model names. Missing enumeration is fine: offer inheritance.
2. Ask for the target scope (project by default, personal on request), budget (inherit by default; small, medium or large), worker cap, and any desired role overrides. Show current choices and preserve fields the user did not change.
3. Show the resulting profile. Validate it through `scripts/profile.py` beside this skill with `python` on Windows or `python3` on POSIX. Real model overrides must be confirmed supported; otherwise keep inheritance and explain the limit.
4. Write only the selected `.codex/pstack.json` or `~/.codex/pstack.json`. Do not overwrite Codex config.toml or AGENTS.md. Never migrate a Cursor model rule automatically.
5. Explain that pstack reads the file when its workflow starts; no always-applied host rule or restart is required. The profile is not a global host setting.
6. If useful and absent, offer once each a project verification skill and a formal verification skill. Generate either only when requested.

A minimal profile is:

```json
{"schema_version":1,"budget":"inherit","max_workers":3,"roles":{}}
```

A scalar role is an object, for example `"bug-fix": {"model":"inherit-parent","reasoning_effort":"inherit"}`. Panel role values are ordered lists of the same objects. See the runtime contract for all role names and precedence.
