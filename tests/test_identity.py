"""Tests for identity pillar evaluator."""
import unittest
from zerotrustmirror.pillars.identity import evaluate
from tests.fixtures.envs.weak import WEAK_ENV
from tests.fixtures.envs.strong import STRONG_ENV


class TestIdentityWeak(unittest.TestCase):
    def test_weak_identity_low(self):
        result = evaluate(WEAK_ENV)
        self.assertLess(result.score, 40)
        self.assertEqual(result.name, "identity")

    def test_weak_identity_mfa_absent(self):
        result = evaluate(WEAK_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertFalse(fields["identity.mfa_enabled"].present)
        self.assertEqual(fields["identity.mfa_enabled"].contribution, 0)

    def test_weak_identity_pam_absent(self):
        result = evaluate(WEAK_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertFalse(fields["identity.privileged_access_management"].present)

    def test_weak_identity_evidence_nonempty(self):
        result = evaluate(WEAK_ENV)
        self.assertGreater(len(result.evidences), 0)


class TestIdentityStrong(unittest.TestCase):
    def test_strong_identity_high(self):
        result = evaluate(STRONG_ENV)
        self.assertGreater(result.score, 75)

    def test_strong_identity_mfa_present(self):
        result = evaluate(STRONG_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertTrue(fields["identity.mfa_enabled"].present)
        self.assertGreater(fields["identity.mfa_enabled"].contribution, 0)

    def test_strong_identity_pam_present(self):
        result = evaluate(STRONG_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertTrue(fields["identity.privileged_access_management"].present)


class TestIdentityParity(unittest.TestCase):
    def test_identity_scores_differ(self):
        weak = evaluate(WEAK_ENV)
        strong = evaluate(STRONG_ENV)
        self.assertNotEqual(weak.score, strong.score)
        self.assertGreater(strong.score, weak.score)


if __name__ == "__main__":
    unittest.main()
