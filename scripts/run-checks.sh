#!/usr/bin/env bash
# Cross-platform core; all artifacts are retained for manual cleanup.
set -euo pipefail
suite=$(cd "$(dirname "$0")/.." && pwd -P)
exec python3 "$suite/scripts/run-checks.py" "$@"
