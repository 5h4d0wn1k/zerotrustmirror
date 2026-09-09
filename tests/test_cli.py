"""Tests for CLI entry point."""
import unittest
import sys
from zerotrustmirror.cli import main


class TestCLI(unittest.TestCase):
    def test_no_args_exits_0(self):
        result = main([])
        self.assertEqual(result, 0)

    def test_version_exits_0(self):
        with self.assertRaises(SystemExit) as ctx:
            main(["--version"])
        self.assertEqual(ctx.exception.code, 0)

    def test_demo_exits_0(self):
        result = main(["demo", "--out-dir", "/tmp/zta_demo_test"])
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
