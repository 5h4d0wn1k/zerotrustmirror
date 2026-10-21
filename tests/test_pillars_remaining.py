"""Tests for apps, data, automation, vis pillars."""
import unittest
from zerotrustmirror.pillars import apps, data, automation, vis
from tests.fixtures.envs.weak import WEAK_ENV
from tests.fixtures.envs.strong import STRONG_ENV


class TestAppsMissingInventory(unittest.TestCase):
    """Absent app-inventory counts must not earn exposure credit (#17)."""

    def test_absent_counts_get_no_exposure_credit(self):
        result = apps.evaluate({"apps": {"api_gateway": True}})
        fields = {e.field: e for e in result.evidences}
        exposure = fields["apps.externally_reachable_apps"]
        self.assertFalse(exposure.present)
        self.assertEqual(exposure.contribution, 0)
        self.assertIn("unknown", exposure.detail)
        self.assertEqual(result.score, 15)  # only the api_gateway evidence

    def test_no_apps_section_gets_no_exposure_credit(self):
        result = apps.evaluate({})
        fields = {e.field: e for e in result.evidences}
        self.assertEqual(fields["apps.externally_reachable_apps"].contribution, 0)
        self.assertEqual(result.score, 0)

    def test_present_counts_still_scored(self):
        result = apps.evaluate(STRONG_ENV)
        fields = {e.field: e for e in result.evidences}
        exposure = fields["apps.externally_reachable_apps"]
        self.assertTrue(exposure.present)
        self.assertEqual(exposure.contribution, 25)


class TestAppsWeak(unittest.TestCase):
    def test_weak_apps_low(self):
        result = apps.evaluate(WEAK_ENV)
        self.assertLess(result.score, 40)

    def test_weak_exposure_high(self):
        result = apps.evaluate(WEAK_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertFalse(fields["apps.externally_reachable_apps"].present)


class TestAppsStrong(unittest.TestCase):
    def test_strong_apps_high(self):
        result = apps.evaluate(STRONG_ENV)
        self.assertGreater(result.score, 75)


class TestDataWeak(unittest.TestCase):
    def test_weak_data_low(self):
        result = data.evaluate(WEAK_ENV)
        self.assertLess(result.score, 40)

    def test_weak_no_classification(self):
        result = data.evaluate(WEAK_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertFalse(fields["data.data_classification_coverage_pct"].present)


class TestDataStrong(unittest.TestCase):
    def test_strong_data_high(self):
        result = data.evaluate(STRONG_ENV)
        self.assertGreater(result.score, 75)


class TestAutomationWeak(unittest.TestCase):
    def test_weak_auto_low(self):
        result = automation.evaluate(WEAK_ENV)
        self.assertLess(result.score, 40)

    def test_weak_no_soar(self):
        result = automation.evaluate(WEAK_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertFalse(fields["automation.soar_platform"].present)


class TestAutomationStrong(unittest.TestCase):
    def test_strong_auto_high(self):
        result = automation.evaluate(STRONG_ENV)
        self.assertGreater(result.score, 75)


class TestVisWeak(unittest.TestCase):
    def test_weak_vis_low(self):
        result = vis.evaluate(WEAK_ENV)
        self.assertLess(result.score, 40)

    def test_weak_no_siem(self):
        result = vis.evaluate(WEAK_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertFalse(fields["vis.siem_present"].present)


class TestVisStrong(unittest.TestCase):
    def test_strong_vis_high(self):
        result = vis.evaluate(STRONG_ENV)
        self.assertGreater(result.score, 75)


class TestParity(unittest.TestCase):
    def test_all_pillars_differ(self):
        evaluators = [apps, data, automation, vis]
        for mod in evaluators:
            w = mod.evaluate(WEAK_ENV)
            s = mod.evaluate(STRONG_ENV)
            self.assertGreater(s.score, w.score, f"{mod.__name__} parity failed")


if __name__ == "__main__":
    unittest.main()
