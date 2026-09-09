"""Tests for fixtures — verify pack values directly."""
import unittest
from tests.fixtures.envs.weak import WEAK_ENV
from tests.fixtures.envs.strong import STRONG_ENV


class TestFixtures(unittest.TestCase):
    def test_weak_no_mfa(self):
        self.assertFalse(WEAK_ENV["identity"]["mfa_enabled"])
        self.assertEqual(WEAK_ENV["identity"]["mfa_coverage_pct"], 0)

    def test_weak_no_device_compliance(self):
        self.assertFalse(WEAK_ENV["devices"]["device_compliance_required"])
        self.assertTrue(WEAK_ENV["devices"]["unmanaged_device_access_allowed"])

    def test_weak_no_microseg(self):
        self.assertFalse(WEAK_ENV["network"]["micro_segmentation"])

    def test_weak_no_classification(self):
        self.assertEqual(WEAK_ENV["data"]["data_classification_coverage_pct"], 0)

    def test_weak_no_soar(self):
        self.assertFalse(WEAK_ENV["automation"]["soar_platform"])

    def test_weak_no_siem(self):
        self.assertFalse(WEAK_ENV["vis"]["siem_present"])

    def test_strong_mfa_enabled(self):
        self.assertTrue(STRONG_ENV["identity"]["mfa_enabled"])
        self.assertGreaterEqual(STRONG_ENV["identity"]["mfa_coverage_pct"], 90)

    def test_strong_device_compliance(self):
        self.assertTrue(STRONG_ENV["devices"]["device_compliance_required"])
        self.assertTrue(STRONG_ENV["devices"]["endpoint_posture_attestation"])

    def test_strong_microseg(self):
        self.assertTrue(STRONG_ENV["network"]["micro_segmentation"])

    def test_strong_classification(self):
        self.assertGreaterEqual(STRONG_ENV["data"]["data_classification_coverage_pct"], 80)

    def test_strong_soar(self):
        self.assertTrue(STRONG_ENV["automation"]["soar_platform"])

    def test_strong_siem(self):
        self.assertTrue(STRONG_ENV["vis"]["siem_present"])

    def test_weak_org_name(self):
        self.assertIn("Weak", WEAK_ENV["org_name"])

    def test_strong_org_name(self):
        self.assertIn("Strong", STRONG_ENV["org_name"])


if __name__ == "__main__":
    unittest.main()
