# Ship a verified change

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. Confirm the user’s merge grant and the exact PR queue. Independently verify each patch on the real matching surface; green CI alone is not a behavioral verdict.
2. For a stack, land only the contiguous verified run from the bottom. Pin each verdict to its baseline/head and recheck any changed patch or changed execution context.
3. Re-read forge-enforced gates and current base/head immediately before each authorized merge. Never bypass a required approval/check.
4. Merge one PR at a time through the supported forge operation, then read back actual merged state and base. Queued/auto-merge requested is not merged. Reverify a retargeted/rebased patch as necessary.
5. Foreground-watch the fixed queue until its ceiling is actually merged or a real blocker needs attention. Stop at the named ceiling; never extend the queue without authorization.
