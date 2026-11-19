import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / "skills/setup-pstack/scripts/profile.py"
        spec = importlib.util.spec_from_file_location("profile", path)
        cls.profile = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.profile)

    def test_defaults_inherit(self):
        self.assertEqual(self.profile.validate({}), {
            "schema_version": 1, "budget": "inherit", "max_workers": 3, "roles": {}})

    def test_scalar_and_panel_roles(self):
        data = {"budget": "small", "roles": {
            "bug-fix": {"model": "inherit-parent"},
            "arena runners": [{"model": "auto"}, {"reasoning_effort": "high"}]}}
        self.assertEqual(self.profile.validate(data)["roles"], data["roles"])

    def test_invalid_profiles_fail(self):
        for data in ({"max_workers": True}, {"max_workers": 0}, {"schema_version": 2},
                     {"budget": "unlimited"}, {"roles": {"unknown": {}}},
                     {"roles": {"bug-fix": []}}, {"roles": {"arena runners": {}}},
                     {"roles": {"bug-fix": {"reasoning_effort": "imaginary"}}},
                     {"roles": {"arena runners": []}}, {"extra": 1}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.profile.validate(data)

    def test_project_profile_replaces_personal_profile(self):
        root = Path(tempfile.mkdtemp(prefix="pstack-profile-tests-"))
        print(f"Retained profile test artifacts: {root}")
        (root / ".codex").mkdir()
        personal = root / "personal.json"
        personal.write_text('{"budget":"large","max_workers":9}')
        project = root / ".codex/pstack.json"
        project.write_text('{"budget":"small"}')
        result, source = self.profile.load(root, personal)
        self.assertEqual(source, project)
        self.assertEqual(result["budget"], "small")
        self.assertEqual(result["max_workers"], 3)


if __name__ == "__main__":
    unittest.main()
