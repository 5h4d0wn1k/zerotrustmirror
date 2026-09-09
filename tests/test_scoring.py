"""Tests for scoring module."""
import unittest
from zerotrustmirror.scoring import evaluate_all, compute_weighted_score, determine_maturity
from zerotrustmirror.models import MaturityLevel
from tests.fixtures.envs.weak import WEAK_ENV
from tests.fixtures.envs.strong import STRONG_ENV


class TestScoring(unittest.TestCase):
    def test_weak_overall_below_40(self):
        pillars = evaluate_all(WEAK_ENV)
        score = compute_weighted_score(pillars)
        self.assertLess(score, 40, f"Weak score {score} should be < 40")

    def test_strong_overall_above_75(self):
        pillars = evaluate_all(STRONG_ENV)
        score = compute_weighted_score(pillars)
        self.assertGreater(score, 75, f"Strong score {score} should be > 75")

    def test_weak_maturity_traditional(self):
        pillars = evaluate_all(WEAK_ENV)
        score = compute_weighted_score(pillars)
        maturity = determine_maturity(score)
        self.assertEqual(maturity, MaturityLevel.TRADITIONAL)

    def test_strong_maturity_optimal_or_advanced(self):
        pillars = evaluate_all(STRONG_ENV)
        score = compute_weighted_score(pillars)
        maturity = determine_maturity(score)
        self.assertIn(maturity, (MaturityLevel.OPTIMAL, MaturityLevel.ADVANCED))

    def test_all_seven_pillars(self):
        pillars = evaluate_all(WEAK_ENV)
        self.assertEqual(len(pillars), 7)

    def test_strong_identity_score_approx_90(self):
        pillars = evaluate_all(STRONG_ENV)
        ident = next(p for p in pillars if p.name == "identity")
        self.assertGreaterEqual(ident.score, 80)
        self.assertLessEqual(ident.score, 100)

    def test_weak_identity_score_approx_25(self):
        pillars = evaluate_all(WEAK_ENV)
        ident = next(p for p in pillars if p.name == "identity")
        self.assertGreaterEqual(ident.score, 0)
        self.assertLessEqual(ident.score, 35)


if __name__ == "__main__":
    unittest.main()
