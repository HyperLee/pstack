#!/usr/bin/env python3
"""Cross-platform statechart launcher. Resolve real executables, not shell aliases."""
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys


def runtime():
    for name in ("node", "bun"):
        candidate = shutil.which(name)
        if not candidate:
            continue
        # On Windows a package manager may expose node.cmd; query it with fixed
        # arguments only, then execute the actual .exe with user arguments.
        try:
            if name == "node" and candidate.lower().endswith((".cmd", ".bat")):
                result = subprocess.run([candidate, "-p", "process.execPath"],
                                        capture_output=True, text=True, encoding="utf-8", timeout=10)
                candidate = result.stdout.strip()
                if result.returncode or not Path(candidate).is_file():
                    continue
            result = subprocess.run([candidate, "--version"], capture_output=True,
                                    text=True, encoding="utf-8", timeout=10)
            match = re.search(r"(\d+)\.(\d+)\.(\d+)", result.stdout)
            if result.returncode or not match:
                continue
            version = tuple(map(int, match.groups()))
            if name == "node" and ((22, 18, 0) <= version < (23, 0, 0) or version >= (23, 6, 0)):
                return [candidate, "--disable-warning=ExperimentalWarning"]
            if name == "bun" and version >= (1, 1, 5):
                return [candidate]
        except (OSError, subprocess.TimeoutExpired):
            continue
    raise RuntimeError("statechart needs Node 22.18–22.x / 23.6+ or Bun 1.1.5+ on PATH")


def main():
    command = [*runtime(), str(Path(__file__).resolve().with_suffix(".ts")), *sys.argv[1:]]
    env = {**os.environ, "PSTACK_PYTHON": sys.executable}
    windows = os.name == "nt"
    if windows:
        command = [sys.executable, str(Path(__file__).with_name("windows-job.py")), *command]
    child = subprocess.Popen(command, env=env, stdin=subprocess.PIPE if windows else None)
    try:
        return child.wait()
    except KeyboardInterrupt:
        if windows:
            child.stdin.close()
        try:
            child.wait(timeout=10)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait(timeout=5)
        return 130
    finally:
        if windows and not child.stdin.closed:
            child.stdin.close()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(2)
