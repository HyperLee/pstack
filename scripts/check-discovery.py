#!/usr/bin/env python3
"""Check native Codex discovery in an isolated project; never starts a model/chat."""
import importlib.util
import json
from pathlib import Path
import queue
import threading
import subprocess
import tempfile
import time


class ResponseReader:
    """A pipe reader on Windows and POSIX, with bounded caller waits."""
    def __init__(self, stream):
        self.lines = queue.Queue()
        def read():
            try:
                for line in stream:
                    self.lines.put(line)
            finally:
                self.lines.put(None)
        threading.Thread(target=read, daemon=True).start()

    def receive(self, wanted, timeout=30):
        deadline = time.monotonic() + timeout
        while True:
            try:
                line = self.lines.get(timeout=max(0, deadline - time.monotonic()))
            except queue.Empty:
                raise TimeoutError("Timed out waiting for Codex; inspect app-server.stderr") from None
            if line is None:
                raise RuntimeError("Codex closed before responding; inspect app-server.stderr")
            value = json.loads(line)
            if value.get("id") == wanted:
                if "error" in value:
                    raise RuntimeError(str(value["error"]))
                return value["result"]


def within(path, root):
    try:
        Path(path).resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def main():
    suite = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("pstack_installer", suite / "scripts/install-skills.py")
    installer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installer)
    project = Path(tempfile.mkdtemp(prefix="pstack-native-discovery-")).resolve()
    print("Retained native discovery artifacts: " + str(project), flush=True)
    subprocess.run(["git", "init", "-q", str(project)], check=True)
    installer.install(suite, project=project)
    with (project / "app-server.stderr").open("w", encoding="utf-8") as stderr:
        child = subprocess.Popen([
            "codex", "-c", "sqlite_home=" + json.dumps(str(project / "state")),
            "-c", "log_dir=" + json.dumps(str(project / "logs")), "app-server",
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr,
            text=True, encoding="utf-8", bufsize=1)
        reader = ResponseReader(child.stdout)

        def send(value):
            child.stdin.write(json.dumps(value) + "\n")
            child.stdin.flush()

        def receive(wanted):
            return reader.receive(wanted)

        try:
            send({"id": 1, "method": "initialize", "params": {
                "clientInfo": {"name": "pstack-readonly-discovery", "version": "1"},
                "capabilities": {"experimentalApi": True, "explicitGatewayOauth": True}}})
            receive(1)
            send({"method": "initialized", "params": {}})
            send({"id": 2, "method": "skills/list", "params": {"cwds": [str(project)], "forceReload": True}})
            entries = receive(2)["data"]
            skills = [skill for entry in entries for skill in entry["skills"] if within(skill["path"], project)]
            errors = [error for entry in entries for error in entry["errors"] if within(error["path"], project)]
            report = {"skills_count": len(skills), "names": sorted(skill["name"] for skill in skills),
                      "interface_count": sum(bool(skill.get("interface")) for skill in skills), "errors": errors}
            (project / "discovery.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
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
