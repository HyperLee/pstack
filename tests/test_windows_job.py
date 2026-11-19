"""Real Win32 Job Object tests. Leaves artifacts for inspection."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
SUPERVISOR = ROOT / "skills/statechart/scripts/windows-job.py"


@unittest.skipUnless(os.name == "nt", "Win32 process contract")
class WindowsJobTests(unittest.TestCase):
    def test_exit_and_arguments(self):
        child = subprocess.Popen([sys.executable, str(SUPERVISOR), sys.executable, "-c",
                                  "import sys,json; print(json.dumps(sys.argv[1:])); sys.exit(1)",
                                  "中文 path", "a&b", 'quoted"value'], stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})
        child.wait(timeout=15)
        self.assertEqual(child.returncode, 1, child.stderr.read())
        self.assertEqual(json.loads(child.stdout.read()), ["中文 path", "a&b", 'quoted"value'])
        child.stdin.close()
        child.stdout.close()
        child.stderr.close()

    def run_tree(self, force):
        root = Path(tempfile.mkdtemp(prefix="pstack-job 中文-"))
        pidfile = root / "pids.json"
        program = ("import subprocess,sys,json,time; from pathlib import Path; "
                   "p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(120)']); "
                   "Path(sys.argv[1]).write_text(json.dumps([__import__('os').getpid(),p.pid])); "
                   "time.sleep(120)")
        child = subprocess.Popen([sys.executable, str(SUPERVISOR), sys.executable, "-c",
                                  program, str(pidfile)], stdin=subprocess.PIPE,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        try:
            deadline = time.monotonic() + 15
            while not pidfile.exists() and child.poll() is None and time.monotonic() < deadline:
                time.sleep(.05)
            self.assertTrue(pidfile.exists(), "supervisor did not launch worker")
            pids = json.loads(pidfile.read_text(encoding="utf-8"))
            if force:
                child.kill()
            else:
                child.stdin.close()
            child.wait(timeout=15)
            import ctypes
            kernel = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel.OpenProcess.restype = ctypes.c_void_p
            kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
            kernel.CloseHandle.argtypes = [ctypes.c_void_p]
            for pid in pids:
                handle = kernel.OpenProcess(0x00100000, False, pid)
                if handle:
                    try:
                        self.assertEqual(kernel.WaitForSingleObject(handle, 5000), 0,
                                         f"owned process {pid} survived")
                    finally:
                        kernel.CloseHandle(handle)
        finally:
            if child.poll() is None:
                child.kill()
                child.wait(timeout=5)
            if not child.stdin.closed:
                child.stdin.close()
            child.stderr.close()

    def test_pipe_close_stops_descendants(self):
        self.run_tree(False)

    def test_supervisor_kill_stops_descendants(self):
        self.run_tree(True)


if __name__ == "__main__":
    unittest.main()
