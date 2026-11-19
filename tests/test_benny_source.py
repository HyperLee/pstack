import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("source", ROOT / "automations/benny/scripts/source.py")
        cls.source = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.source)

    def test_preserves_thread_and_timestamp_precision(self):
        event = {"channel_id": "C123", "thread_ts": "1795016545.000001", "message_ts": "1795016550.000002"}
        self.assertEqual(self.source.validate(event, "C123"), event)

    def test_missing_or_mismatched_coordinates_fail_closed(self):
        for event in ({}, {"channel_id": "C456", "thread_ts": "1.000001", "message_ts": "1.000001"},
                      {"channel_id": "C123", "thread_ts": 1.000001, "message_ts": "1.000001"},
                      {"channel_id": "C123", "thread_ts": "1.000001"}):
            with self.subTest(event=event), self.assertRaises(ValueError):
                self.source.validate(event, "C123")


if __name__ == "__main__":
    unittest.main()
