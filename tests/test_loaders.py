"""Tests for loaders module."""
import json
import tempfile
import unittest
from pathlib import Path
from zerotrustmirror.loaders import load_env, load_channel_logs


class TestLoaders(unittest.TestCase):
    def test_load_json_env(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"org_name": "test"}, f)
            f.flush()
            data = load_env(f.name)
        self.assertEqual(data["org_name"], "test")

    def test_load_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_env("/nonexistent/path.json")

    def test_load_channel_logs_empty(self):
        result = load_channel_logs("/nonexistent/path.json")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
