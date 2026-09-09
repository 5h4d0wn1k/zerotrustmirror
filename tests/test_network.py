"""Tests for network pillar evaluator."""
import unittest
from zerotrustmirror.pillars.network import evaluate
from tests.fixtures.envs.weak import WEAK_ENV
from tests.fixtures.envs.strong import STRONG_ENV


class TestNetworkWeak(unittest.TestCase):
    def test_weak_network_low(self):
        result = evaluate(WEAK_ENV)
        self.assertLess(result.score, 40)

    def test_weak_no_microseg(self):
        result = evaluate(WEAK_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertFalse(fields["network.micro_segmentation"].present)

    def test_weak_vpn_only(self):
        result = evaluate(WEAK_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertFalse(fields["network.zero_trust_network_access"].present)


class TestNetworkStrong(unittest.TestCase):
    def test_strong_network_high(self):
        result = evaluate(STRONG_ENV)
        self.assertGreater(result.score, 75)

    def test_strong_microseg(self):
        result = evaluate(STRONG_ENV)
        fields = {e.field: e for e in result.evidences}
        self.assertTrue(fields["network.micro_segmentation"].present)


class TestNetworkParity(unittest.TestCase):
    def test_network_differ(self):
        weak = evaluate(WEAK_ENV)
        strong = evaluate(STRONG_ENV)
        self.assertGreater(strong.score, weak.score)


if __name__ == "__main__":
    unittest.main()
