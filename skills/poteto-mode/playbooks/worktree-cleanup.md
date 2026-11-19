# Worktree inventory and manual cleanup handoff

Read the [Codex runtime contract](../references/codex-runtime.md) before using tools.

1. On Windows run `python scripts/worktree-audit.py --offline [-b BASE] [repo]` from the poteto-mode skill folder. On POSIX the `bash scripts/worktree-audit.sh` wrapper remains available. Use canonical full paths when working elsewhere. It only reads local refs and worktree metadata.
2. Inspect current project chats through available Codex tools, dirty files and open PRs before recommending any candidate. Unknown usage stays unknown; no automatic safe bucket.
3. Report sizes, refs, uncommitted work, usage evidence and candidates needing human judgment. Never fetch implicitly.
4. Directory, worktree, simulator and cache deletion is manual. Stop at the inventory and hand the named candidates to the user; do not run recursive deletion or a batch of single-file unlinks.
