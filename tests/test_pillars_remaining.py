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
