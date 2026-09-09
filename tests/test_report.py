"""Tests for report generation."""
import json
import tempfile
import unittest
from pathlib import Path
from zerotrustmirror.report import build_result, generate_remediation, to_json, to_markdown, write_report
from zerotrustmirror.scoring import evaluate_all, compute_weighted_score, determine_maturity
from tests.fixtures.envs.weak import WEAK_ENV
from tests.fixtures.envs.strong import STRONG_ENV


class TestReport(unittest.TestCase):
    def test_remediation_roadmap_generated_weak(self):
        pillars = evaluate_all(WEAK_ENV)
        roadmap = generate_remediation(pillars)
        self.assertGreater(len(roadmap), 0, "Weak env should generate remediation items")

    def test_remediation_roadmap_at_least_12_items_weak(self):
        pillars = evaluate_all(WEAK_ENV)
        roadmap = generate_remediation(pillars)
        self.assertGreaterEqual(len(roadmap), 12, f"Expected >=12 remediation items, got {len(roadmap)}")

    def test_json_output_parseable(self):
        pillars = evaluate_all(WEAK_ENV)
        overall = compute_weighted_score(pillars)
        maturity = determine_maturity(overall)
        result = build_result(pillars, overall, maturity)
        j = to_json(result)
        data = json.loads(j)
        self.assertIn("overall_score", data)
        self.assertIn("pillars", data)
        self.assertEqual(len(data["pillars"]), 7)

    def test_markdown_output_has_headers(self):
        pillars = evaluate_all(WEAK_ENV)
        overall = compute_weighted_score(pillars)
        maturity = determine_maturity(overall)
        result = build_result(pillars, overall, maturity)
        md = to_markdown(result)
        self.assertIn("# Zero-Trust Readiness Report", md)
        self.assertIn("## Per-Pillar Scores", md)
        self.assertIn("## Remediation Roadmap", md)

    def test_write_report_creates_files(self):
        pillars = evaluate_all(WEAK_ENV)
        overall = compute_weighted_score(pillars)
        maturity = determine_maturity(overall)
        result = build_result(pillars, overall, maturity)
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = write_report(result, tmpdir, prefix="test")
            self.assertTrue(Path(paths["json"]).exists())
            self.assertTrue(Path(paths["markdown"]).exists())


if __name__ == "__main__":
    unittest.main()
