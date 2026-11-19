#!/usr/bin/env python3
"""Run cross-platform checks. Keep every log/cache/artifact for manual cleanup."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true", help="Require Bun, Node and Java/TLC; missing tools fail")
    parser.add_argument("--discovery", action="store_true", help="Also verify installed skills through Codex app-server")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    artifacts = Path(os.environ.get("PSTACK_TEST_ROOT") or tempfile.mkdtemp(prefix="pstack-checks-"))
    artifacts = artifacts.resolve()
    artifacts.mkdir(parents=True, exist_ok=True)
    for name in ("tmp", "cache"):
        (artifacts / name).mkdir(exist_ok=True)
    env = {**os.environ, "PYTHONUTF8": "1", "PSTACK_PYTHON": sys.executable,
           "TMPDIR": str(artifacts / "tmp"), "TMP": str(artifacts / "tmp"),
           "TEMP": str(artifacts / "tmp"), "XDG_CACHE_HOME": str(artifacts / "cache"),
           "npm_config_cache": str(artifacts / "cache/npm")}
    print(f"Retained check artifacts: {artifacts}", flush=True)
    results = []

    def run(name, command, cwd=root):
        log = artifacts / (name + ".log")
        with log.open("w", encoding="utf-8") as stream:
            try:
                result = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                                        stderr=subprocess.STDOUT)
                code = result.returncode
            except OSError as error:
                stream.write(str(error))
                code = 1
        results.append((name, code))
        print(f"{'PASS' if code == 0 else 'FAIL'}: {name} ({log})", flush=True)
        if code:
            print("\n".join(log.read_text(encoding="utf-8", errors="replace").splitlines()[-16:]), flush=True)

    run("validate", [sys.executable, "-B", "scripts/validate.py"])
    run("python-tests", [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"])
    bun = shutil.which(os.environ.get("PSTACK_BUN", "bun"))
    if bun:
        work = root / "skills/poteto-mode/scripts"
        run("watch-pr", [bun, "test", "watch-pr"], work)
        run("watch-pr-types", [bun, "run", "typecheck"], work)
    else:
        print("NOT RUN: PR watcher needs Bun and prepared dependencies", flush=True)
        if args.full:
            results.append(("missing-bun", 1))
    spec = root / "skills/statechart/scripts/statechart.py"
    import importlib.util
    module_spec = importlib.util.spec_from_file_location("statechart_launcher", spec)
    launcher = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(launcher)
    try:
        runtime = launcher.runtime()
        # Node's test runner is the contract for this suite; Bun runs the watcher.
        if "bun" in Path(runtime[0]).stem.lower():
            raise RuntimeError("Statechart tests need a supported Node executable")
        work = root / "skills/statechart/scripts"
        files = sorted((work / "test").glob("*.test.ts"))
        if os.name == "nt":
            files = [p for p in files if p.name != "cli.test.ts"]
            print("Windows CLI/process tests replace POSIX shell/signal CLI tests.", flush=True)
        jar = os.environ.get("TLA2TOOLS")
        if args.full and (not jar or not Path(jar).is_file()):
            results.append(("missing-tlc-jar", 1))
        if args.full:
            run("java-modules", [os.environ.get("JAVA") or "java", "--list-modules"])
            if "jdk.compiler@" not in (artifacts / "java-modules.log").read_text(encoding="utf-8", errors="replace"):
                print("FAIL: full oracle tests require a JDK (jdk.compiler), not only a JRE", flush=True)
                return 1
        run("statechart", [*runtime, "--test", *map(str, files)], work)
    except RuntimeError as error:
        print(f"NOT RUN: {error}", flush=True)
        if args.full:
            results.append(("missing-node", 1))
    if args.discovery:
        run("discovery", [sys.executable, "-B", "scripts/check-discovery.py"])
    return int(any(code for _, code in results))


if __name__ == "__main__":
    raise SystemExit(main())
