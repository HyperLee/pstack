#!/usr/bin/env bash
# All artifacts are retained. No directory cleanup is performed.
set -euo pipefail
suite=$(cd "$(dirname "$0")/.." && pwd -P)
artifacts=${PSTACK_TEST_ROOT:-$(mktemp -d "${TMPDIR:-/tmp}/pstack-checks-XXXXXX")}
mkdir -p "$artifacts/tmp" "$artifacts/cache"
export TMPDIR="$artifacts/tmp"
export XDG_CACHE_HOME="$artifacts/cache"
export npm_config_cache="$artifacts/cache/npm"
printf 'Retained check artifacts: %s\n' "$artifacts"
cd "$suite"
python3 -B scripts/validate.py
python3 -B -m unittest discover -s tests -v
bun_bin=${PSTACK_BUN:-bun}
if command -v "$bun_bin" >/dev/null 2>&1; then
  (cd skills/poteto-mode/scripts && "$bun_bin" test watch-pr && "$bun_bin" run typecheck)
else
  printf 'NOT RUN: PR watcher tests/typecheck need Bun and prepared dependencies.\n'
fi
(cd skills/statechart/scripts && node --disable-warning=ExperimentalWarning --test test/*.test.ts)
printf 'Artifacts retained for manual cleanup: %s\n' "$artifacts"
