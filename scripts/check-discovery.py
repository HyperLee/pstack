#!/usr/bin/env python3
"""Check native Codex discovery in an isolated project; never starts a model/chat."""
import importlib.util
import json
from pathlib import Path
import select
import subprocess
import tempfile
import time


def main():
    suite = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("pstack_installer", suite / "scripts/install-skills.py")
    installer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installer)
    project = Path(tempfile.mkdtemp(prefix="pstack-native-discovery-")).resolve()
    print("Retained native discovery artifacts: " + str(project), flush=True)
    subprocess.run(["git", "init", "-q", str(project)], check=True)
    installer.install(suite, project=project)
    with (project / "app-server.stderr").open("w") as stderr:
        child = subprocess.Popen([
            "codex", "-c", "sqlite_home=" + json.dumps(str(project / "state")),
            "-c", "log_dir=" + json.dumps(str(project / "logs")), "app-server",
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr, text=True, bufsize=1)

        def send(value):
            child.stdin.write(json.dumps(value) + "\n")
            child.stdin.flush()

        def receive(wanted):
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                if not select.select([child.stdout], [], [], 1)[0]:
                    continue
                line = child.stdout.readline()
                if not line:
                    raise RuntimeError("Codex closed before responding; inspect app-server.stderr")
                value = json.loads(line)
                if value.get("id") == wanted:
                    if "error" in value:
                        raise RuntimeError(str(value["error"]))
                    return value["result"]
            raise TimeoutError("Timed out waiting for Codex; inspect app-server.stderr")

        try:
            send({"id": 1, "method": "initialize", "params": {
                "clientInfo": {"name": "pstack-readonly-discovery", "version": "1"},
                "capabilities": {"experimentalApi": True, "explicitGatewayOauth": True}}})
            receive(1)
            send({"method": "initialized", "params": {}})
            send({"id": 2, "method": "skills/list", "params": {"cwds": [str(project)], "forceReload": True}})
            entries = receive(2)["data"]
            prefix = str(project) + "/"
            skills = [skill for entry in entries for skill in entry["skills"] if skill["path"].startswith(prefix)]
            errors = [error for entry in entries for error in entry["errors"] if error["path"].startswith(prefix)]
            report = {"skills_count": len(skills), "names": sorted(skill["name"] for skill in skills),
                      "interface_count": sum(bool(skill.get("interface")) for skill in skills), "errors": errors}
            (project / "discovery.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
            if len(skills) != 58 or report["interface_count"] != 58 or errors:
                raise RuntimeError("Native discovery failed; inspect discovery.json")
            print("Native Codex discovery: 58 skills, 58 interfaces, 0 errors")
        finally:
            child.stdin.close()
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                child.terminate()
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait(timeout=5)


if __name__ == "__main__":
    main()
