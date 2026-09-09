"""Tests for devices pillar evaluator."""
import unittest
from zerotrustmirror.pillars.devices import evaluate
from tests.fixtures.envs.weak import WEAK_ENV
from tests.fixtures.envs.strong import STRONG_ENV


class TestDevicesWeak(unittest.TestCase):
    def test_weak_devices_low(self):
        result = evaluate(WEAK_ENV)
        self.assertLess(result.score, 40)

    def test_weak_unmanaged_allowed(self):
        result = evaluate(WEAK_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertFalse(fields["devices.unmanaged_device_access_allowed"].present)  # allowed=True => no_unmanaged=False

    def test_weak_no_posture(self):
        result = evaluate(WEAK_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertFalse(fields["devices.endpoint_posture_attestation"].present)


class TestDevicesStrong(unittest.TestCase):
    def test_strong_devices_high(self):
        result = evaluate(STRONG_ENV)
        self.assertGreater(result.score, 75)

    def test_strong_posture_present(self):
        result = evaluate(STRONG_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertTrue(fields["devices.endpoint_posture_attestation"].present)


class TestDevicesParity(unittest.TestCase):
    def test_devices_differ(self):
        weak = evaluate(WEAK_ENV)
        strong = evaluate(STRONG_ENV)
        self.assertGreater(strong.score, weak.score)


if __name__ == "__main__":
    unittest.main()
