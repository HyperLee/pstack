from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SafetyTests(unittest.TestCase):
    def test_executable_sources_have_no_recursive_delete(self):
        bad = []
        for p in (ROOT / "skills").rglob("*"):
            if not p.is_file() or "node_modules" in p.parts or "corpus" in p.parts:
                continue
            if p.suffix not in (".ts", ".sh", ".py"):
                continue
            source = p.read_text()
            if (re.search(r'\brm\s+-(?:rf|fr|r)\b', source) or
                    re.search(r'rmSync\([^;]*recursive\s*:\s*true', source, re.S)):
                bad.append(str(p.relative_to(ROOT)))
        self.assertEqual(bad, [])

    def test_audit_does_not_fetch_or_change_refs(self):
        root = Path(tempfile.mkdtemp(prefix="pstack-audit-tests-"))
        print(f"Retained audit test artifacts: {root}")
        repo = root / "repo with spaces"
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                        "commit", "--allow-empty", "-qm", "initial"], check=True)
        subprocess.run(["git", "-C", str(repo), "worktree", "add", "-q", "-b", "candidate",
                        str(root / "linked tree")], check=True)
        refs = subprocess.check_output(["git", "-C", str(repo), "show-ref"])
        result = subprocess.run(["bash", str(ROOT / "skills/poteto-mode/scripts/worktree-audit.sh"),
                                 "--offline", "-b", "HEAD", str(repo)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(root / "linked tree"), result.stdout)
        self.assertIn("unknown", result.stdout)
        self.assertNotIn("\tsafe\t", result.stdout)
        self.assertEqual(refs, subprocess.check_output(["git", "-C", str(repo), "show-ref"]))
        self.assertTrue((root / "linked tree").is_dir())

    def test_audit_continues_after_a_missing_registered_worktree(self):
        root = Path(tempfile.mkdtemp(prefix="pstack-stale-audit-tests-"))
        print(f"Retained stale-worktree test artifacts: {root}")
        repo = root / "repo"
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                        "commit", "--allow-empty", "-qm", "initial"], check=True)
        linked = root / "registered tree"
        subprocess.run(["git", "-C", str(repo), "worktree", "add", "-q", "-b", "candidate", str(linked)], check=True)
        linked.rename(root / "preserved moved tree")
        result = subprocess.run(["bash", str(ROOT / "skills/poteto-mode/scripts/worktree-audit.sh"),
                                 "--offline", "-b", "HEAD", str(repo)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(linked), result.stdout)
        self.assertIn("unknown", result.stdout)
        self.assertIn("hold-unavailable", result.stdout)
        self.assertTrue((root / "preserved moved tree").is_dir())


if __name__ == "__main__":
    unittest.main()
