"""Installation behavior. Test artifacts are retained for manual cleanup."""
import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = Path(tempfile.mkdtemp(prefix="pstack-install-tests-"))


class InstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("installer", ROOT / "scripts/install-skills.py")
        cls.installer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.installer)

    def target(self):
        return Path(tempfile.mkdtemp(prefix="project with spaces-", dir=ARTIFACTS))

    def test_project_install_is_complete_and_relocatable(self):
        target = self.target()
        self.installer.install(ROOT, project=target, mode="copy" if os.name == "nt" else "symlink")
        installed = target / ".agents/skills/poteto-mode"
        if os.name != "nt":
            self.assertTrue(installed.is_symlink())
            self.assertFalse(Path(os.readlink(installed)).is_absolute())
        else:
            self.assertFalse(installed.is_symlink())
        bundle = target / ".codex/pstack"
        self.assertEqual(len(list((target / ".agents/skills").glob("*/SKILL.md"))), 58)
        for item in ("README.md", "LICENSE", "docs/guide/README.md", "scripts/install-skills.py",
                     "automations/benny/FOR_AGENTS.md"):
            self.assertTrue((bundle / item).is_file(), item)
        self.assertFalse((bundle / ".git").exists())
        relocated = self.target() / "relocated"
        shutil.copytree(target, relocated, symlinks=True)
        self.assertTrue((relocated / ".agents/skills/poteto-mode/SKILL.md").is_file())
        if os.name != "nt":
            self.assertEqual((relocated / ".agents/skills/poteto-mode").resolve().parents[1],
                             (relocated / ".codex/pstack").resolve())

    def test_dry_run_creates_nothing(self):
        target = self.target()
        before = list(target.iterdir())
        self.installer.install(ROOT, project=target, dry_run=True)
        self.assertEqual(list(target.iterdir()), before)

    def test_repeated_install_is_idempotent(self):
        target = self.target()
        self.installer.install(ROOT, project=target, mode="copy" if os.name == "nt" else "symlink")
        path = target / ".codex/pstack/README.md"
        before = path.stat().st_mtime_ns
        self.installer.install(ROOT, project=target, mode="copy" if os.name == "nt" else "symlink")
        self.assertEqual(path.stat().st_mtime_ns, before)

    def test_link_conflict_prevents_partial_install(self):
        target = self.target()
        conflict = target / ".agents/skills/swarm"
        conflict.mkdir(parents=True)
        (conflict / "mine.txt").write_text("user content")
        with self.assertRaises(self.installer.InstallConflict):
            self.installer.install(ROOT, project=target, mode="copy" if os.name == "nt" else "symlink")
        self.assertEqual((conflict / "mine.txt").read_text(), "user content")
        self.assertFalse((target / ".codex/pstack").exists())
        self.assertFalse((target / ".agents/skills/poteto-mode").exists())

    def test_modified_bundle_is_not_overwritten(self):
        target = self.target()
        self.installer.install(ROOT, project=target, mode="copy" if os.name == "nt" else "symlink")
        path = target / ".codex/pstack/README.md"
        path.write_text("local changes")
        with self.assertRaises(self.installer.InstallConflict):
            self.installer.install(ROOT, project=target, mode="copy" if os.name == "nt" else "symlink")
        self.assertEqual(path.read_text(), "local changes")

    def test_user_links_preserve_source_with_spaces(self):
        home = self.target()
        source = self.target() / "source clone"
        source.mkdir()
        for name in self.installer.PAYLOAD:
            original = ROOT / name
            if original.is_dir():
                shutil.copytree(original, source / name, ignore=shutil.ignore_patterns("node_modules", "__pycache__"))
            elif original.exists():
                shutil.copy2(original, source / name)
        self.installer.install(source, user_home=home, mode="copy" if os.name == "nt" else "symlink")
        link = home / ".agents/skills/swarm"
        self.assertEqual(link.resolve(), ((home / ".agents/skills/swarm") if os.name == "nt"
                                          else (source / "skills/swarm")).resolve())
        self.installer.install(source, user_home=home, mode="copy" if os.name == "nt" else "symlink")


if __name__ == "__main__":
    print(f"Retained test artifacts: {ARTIFACTS}", flush=True)
    unittest.main()
