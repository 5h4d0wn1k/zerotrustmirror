"""Tests for multichannel correlation engine."""
import unittest
from zerotrustmirror.correlation import correlate
from tests.fixtures.channels import WEB_LOGS, NETWORK_LOGS, HOST_LOGS


class TestCorrelation(unittest.TestCase):
    def test_alice_correlated_across_three_channels(self):
        behaviors = correlate([WEB_LOGS, NETWORK_LOGS, HOST_LOGS])
        alice_behaviors = [b for b in behaviors if b.user == "alice@example.com"]
        self.assertGreater(len(alice_behaviors), 0, "alice@example.com not found in correlations")

    def test_alice_channels_include_all_three(self):
        behaviors = correlate([WEB_LOGS, NETWORK_LOGS, HOST_LOGS])
        alice = next(b for b in behaviors if b.user == "alice@example.com")
        channels = set(e.channel for e in alice.events)
        self.assertIn("web", channels)
        self.assertIn("network", channels)
        self.assertIn("host", channels)

    def test_alice_risk_score_plausible(self):
        behaviors = correlate([WEB_LOGS, NETWORK_LOGS, HOST_LOGS])
        alice = next(b for b in behaviors if b.user == "alice@example.com")
        self.assertGreater(alice.risk_score, 0.3)
        self.assertLessEqual(alice.risk_score, 1.0)

    def test_alice_policy_finding_nonempty(self):
        behaviors = correlate([WEB_LOGS, NETWORK_LOGS, HOST_LOGS])
        alice = next(b for b in behaviors if b.user == "alice@example.com")
        self.assertGreater(len(alice.policy_finding), 0)

    def test_alice_has_privilege_escalation_in_finding(self):
        behaviors = correlate([WEB_LOGS, NETWORK_LOGS, HOST_LOGS])
        alice = next(b for b in behaviors if b.user == "alice@example.com")
        self.assertIn("privilege escalation", alice.policy_finding.lower())

    def test_single_channel_no_correlation(self):
        behaviors = correlate([WEB_LOGS])
        multi = [b for b in behaviors if len(set(e.channel for e in b.events)) > 1]
        self.assertEqual(len(multi), 0, "Single channel should not produce multi-channel correlations")


if __name__ == "__main__":
    unittest.main()
