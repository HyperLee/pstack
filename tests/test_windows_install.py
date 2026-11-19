"""Copy installations work without link privileges; artifacts are retained."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class CopyInstallTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("installer", ROOT / "scripts/install-skills.py")
        cls.installer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.installer)

    def target(self):
        path = Path(tempfile.mkdtemp(prefix="pstack-Windows 中文 spaces-"))
        print("Retained install artifacts:", path)
        return path

    def test_copy_install_relocates_and_repeats_without_links(self):
        target = self.target()
        self.installer.install(ROOT, project=target, mode="copy")
        skill = target / ".agents/skills/poteto-help"
        self.assertFalse(skill.is_symlink())
        self.assertEqual(len(list((target / ".agents/skills").glob("*/SKILL.md"))), 58)
        marker = json.loads((skill / ".pstack-suite.json").read_text(encoding="utf-8"))
        self.assertEqual((skill / marker["suite"]).resolve(), target / ".codex/pstack")
        before = (skill / "SKILL.md").stat().st_mtime_ns
        self.installer.install(ROOT, project=target, mode="copy")
        self.assertEqual((skill / "SKILL.md").stat().st_mtime_ns, before)
        moved = self.target() / "moved"
        shutil.copytree(target, moved)
        relocated = moved / ".agents/skills/poteto-help"
        self.assertTrue((relocated / marker["suite"] / "docs/guide/README.md").is_file())
        locator = moved / ".agents/skills/poteto-mode/scripts/locate-suite.py"
        result = subprocess.check_output([sys.executable, str(locator), str(relocated / "SKILL.md")],
                                         encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})
        self.assertEqual(Path(result.strip()), moved / ".codex/pstack")
        subprocess.run(["git", "init", "-q", str(moved)], check=True)
        subprocess.run(["git", "-C", str(moved), "add", ".agents", ".codex"], check=True,
                       capture_output=True)
        subprocess.run(["git", "-C", str(moved), "-c", "user.name=Test", "-c",
                        "user.email=test@example.invalid", "commit", "-qm", "Windows copy install"], check=True)
        checkout = self.target() / "checkout"
        subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(moved), str(checkout)], check=True)
        copied_marker = json.loads((checkout / ".agents/skills/poteto-help/.pstack-suite.json").read_text(encoding="utf-8"))
        self.assertTrue((checkout / ".agents/skills/poteto-help" / copied_marker["suite"] /
                         "docs/guide/README.md").is_file())
        self.installer.install(ROOT, project=checkout, mode="copy")

    def test_preview_and_conflict_never_write(self):
        target = self.target()
        self.installer.install(ROOT, project=target, mode="copy", dry_run=True)
        self.assertEqual(list(target.iterdir()), [])
        occupied = target / ".agents/skills/swarm"
        occupied.mkdir(parents=True)
        (occupied / "mine.txt").write_text("使用者資料", encoding="utf-8")
        with self.assertRaises(self.installer.InstallConflict):
            self.installer.install(ROOT, project=target, mode="copy")
        self.assertFalse((target / ".codex/pstack").exists())
        self.assertEqual((occupied / "mine.txt").read_text(encoding="utf-8"), "使用者資料")

    def test_modified_copy_is_preserved(self):
        target = self.target()
        self.installer.install(ROOT, project=target, mode="copy")
        skill = target / ".agents/skills/swarm/SKILL.md"
        skill.write_text("local changes", encoding="utf-8")
        with self.assertRaises(self.installer.InstallConflict):
            self.installer.install(ROOT, project=target, mode="copy")
        self.assertEqual(skill.read_text(encoding="utf-8"), "local changes")

    def test_interrupted_bundle_write_reports_retained_paths(self):
        target = self.target()
        write = Path.write_bytes
        def interrupted(path, data):
            if path.name == "LICENSE":
                raise OSError("simulated write failure")
            return write(path, data)
        with patch.object(Path, "write_bytes", interrupted):
            with self.assertRaises(self.installer.InstallConflict) as error:
                self.installer.install(ROOT, project=target, mode="copy")
        self.assertIn(str(target / ".codex/pstack"), str(error.exception))
        self.assertTrue((target / ".codex/pstack/README.md").is_file())
        self.assertFalse((target / ".agents/skills/poteto-mode").exists())

    def test_user_copy_is_independent_of_source(self):
        home = self.target()
        self.installer.install(ROOT, user_home=home, mode="copy")
        marker = home / ".agents/skills/poteto-mode/.pstack-suite.json"
        self.assertTrue(marker.is_file())
        self.assertTrue((home / ".codex/pstack/docs/guide/README.md").is_file())

    @unittest.skipUnless(os.name == "nt", "Windows junction contract")
    def test_junction_conflict_on_python_without_isjunction(self):
        target, external = self.target(), self.target()
        link = target / ".agents"
        subprocess.run(["cmd", "/d", "/c", "mklink", "/J", str(link), str(external)],
                       check=True, capture_output=True)
        with patch.object(os.path, "isjunction", lambda path: False, create=True):
            with self.assertRaises(self.installer.InstallConflict):
                self.installer.install(ROOT, project=target, mode="copy")
        self.assertEqual(list(external.iterdir()), [])
        self.assertFalse((target / ".codex").exists())


if __name__ == "__main__":
    unittest.main()
