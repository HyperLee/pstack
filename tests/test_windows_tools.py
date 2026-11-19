import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class WindowsToolTests(unittest.TestCase):
    def test_discovery_reads_pipes_and_reports_eof_without_select(self):
        spec = importlib.util.spec_from_file_location("discovery", ROOT / "scripts/check-discovery.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(hasattr(module, "ResponseReader"), "pipe reader must support Windows")
        reader = module.ResponseReader(io.StringIO('{"id":2,"result":{"ok":true}}\n'))
        self.assertEqual(reader.receive(2), {"ok": True})
        with self.assertRaises(RuntimeError):
            reader.receive(3)

    def test_log_preserves_chinese_and_sanitizes_cells(self):
        root = Path(tempfile.mkdtemp(prefix="pstack-log-"))
        log = root / "中文 log.tsv"
        command = [sys.executable, str(ROOT / "skills/show-me-your-work/scripts/log.py"),
                   str(log), "驗證", "=danger\tcell", "why\nnext", "@evidence", "通過"]
        first = subprocess.run(command, capture_output=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        subprocess.run(command, check=True)
        rows = log.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(rows), 3)
        cells = rows[1].split("\t")
        self.assertEqual(len(cells), 6)
        self.assertEqual(cells[1:], ["驗證", "'=danger cell", "why next", "'@evidence", "通過"])

    def test_profile_accepts_utf8_bom(self):
        root = Path(tempfile.mkdtemp(prefix="pstack-bom-"))
        profile = root / "profile.json"
        profile.write_text(json.dumps({"budget": "small"}), encoding="utf-8-sig")
        result = subprocess.run([sys.executable, str(ROOT / "skills/setup-pstack/scripts/profile.py"),
                                 str(profile)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
