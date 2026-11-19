---
name: make-bot-ui
description: Use when creating a small UI for a configured webhook or event handler, including server-side credential handling. Produces an unconnected integration template when no handler exists.
---

# Make a bot UI

Read `../poteto-mode/references/codex-runtime.md`. Build a small interface for an already identified webhook/event handler. This skill does not create a native Codex webhook or event scheduler.

Establish the endpoint, JSON payload, allowed action, authentication mechanism and observable acknowledgment. If no handler exists, deliver a UI/server integration template with explicit unconnected status. Do not invent an endpoint, scheduler API or secret-request tool.

Keep credentials in server-side environment/secret-manager references. The browser sends a small JSON request to the local server; the server validates it and calls the configured handler with a timeout and bounded attempts. Do not print or log tokens. Treat payloads as untrusted data.

Bind to localhost by default. Expose through an existing approved network route only when the user requests it; do not install networking agents or change machine exposure automatically. A harmless end-to-end probe must confirm delivery before claiming the UI is connected. Without a real service grant, test against a local fake and clearly label the remaining integration.
