"""Tests for apps, data, automation, vis pillars."""
import unittest
from zerotrustmirror.pillars import apps, data, automation, vis
from tests.fixtures.envs.weak import WEAK_ENV
from tests.fixtures.envs.strong import STRONG_ENV


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


class TestRunbookContradictoryCounts(unittest.TestCase):
    """automated > total is contradictory and must not pass (#6)."""

    def _fields(self, result):
        return {e.field: e for e in result.evidences}

    def test_zero_total_with_automated_fails(self):
        cfg = {"automation": {"automated_policy_enforcement": False,
                              "soar_platform": False,
                              "incident_runbooks_automated": 3,
                              "total_incident_runbooks": 0}}
        result = automation.evaluate(cfg)
        rb = self._fields(result)["automation.incident_runbooks_automated"]
        self.assertFalse(rb.present)
        self.assertEqual(rb.contribution, 0)
        self.assertIn("contradictory", rb.detail)
        self.assertEqual(result.score, 0)

    def test_automated_exceeds_total_fails(self):
        cfg = {"automation": {"automated_policy_enforcement": False,
                              "soar_platform": False,
                              "incident_runbooks_automated": 5,
                              "total_incident_runbooks": 4}}
        result = automation.evaluate(cfg)
        rb = self._fields(result)["automation.incident_runbooks_automated"]
        self.assertFalse(rb.present)
        self.assertEqual(rb.contribution, 0)
        self.assertEqual(result.score, 0)

    def test_zero_zero_still_fails_cleanly(self):
        cfg = {"automation": {"incident_runbooks_automated": 0,
                              "total_incident_runbooks": 0}}
        result = automation.evaluate(cfg)
        rb = self._fields(result)["automation.incident_runbooks_automated"]
        self.assertFalse(rb.present)
        self.assertEqual(rb.contribution, 0)

    def test_valid_counts_still_scored(self):
        cfg = {"automation": {"incident_runbooks_automated": 7,
                              "total_incident_runbooks": 10}}
        result = automation.evaluate(cfg)
        rb = self._fields(result)["automation.incident_runbooks_automated"]
        self.assertTrue(rb.present)
        self.assertEqual(rb.contribution, 25)
