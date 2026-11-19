#!/usr/bin/env bash
# Keep a single implementation of UTF-8 TSV escaping and append behavior.
set -euo pipefail
exec python3 "$(dirname "$0")/log.py" "$@"
