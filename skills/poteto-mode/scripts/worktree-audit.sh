#!/usr/bin/env bash
# Read-only inventory. Directory cleanup is a manual handoff.
set -euo pipefail
exec python3 "$(dirname "$0")/worktree-audit.py" "$@"
