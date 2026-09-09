"""Network pillar evaluator."""
from __future__ import annotations

from zerotrustmirror.models import Evidence, MaturityLevel, PillarResult


def evaluate(cfg: dict) -> PillarResult:
    net = cfg.get("network", {})
    evidences: list[Evidence] = []
    score = 0

    micro = net.get("micro_segmentation", False)
    evidences.append(Evidence("network.micro_segmentation", micro, f"Micro-segmentation: {micro}", 25 if micro else 0))
    score += 25 if micro else 0

    ew = net.get("east_west_policy", False)
    evidences.append(Evidence("network.east_west_policy", ew, f"E-W policy: {ew}", 20 if ew else 0))
    score += 20 if ew else 0

    tools = net.get("network_visibility_tools", [])
    tools_ok = len(tools) >= 2
    evidences.append(Evidence("network.network_visibility_tools", tools_ok, f"Visibility tools: {tools}", 20 if tools_ok else (10 if len(tools) == 1 else 0)))
    score += 20 if tools_ok else (10 if len(tools) == 1 else 0)

    vpn_only = net.get("remote_access_vpn_only", True)
    ztna = net.get("zero_trust_network_access", False)
    zt_ok = ztna and not vpn_only
    evidences.append(Evidence("network.zero_trust_network_access", zt_ok, f"ZTNA: {ztna}, VPN-only: {vpn_only}", 20 if zt_ok else 0))
    score += 20 if zt_ok else 0

    # remaining 15 pts: e-w + micro coverage
    if micro and ew:
        score += 15
        evidences.append(Evidence("network.segmentation_bonus", True, "Full segmentation bonus", 15))

    score = min(score, 100)
    maturity = _maturity(score)
    return PillarResult(name="network", score=score, maturity=maturity, evidences=evidences)


def _maturity(score: int) -> MaturityLevel:
    if score >= 80:
        return MaturityLevel.OPTIMAL
    if score >= 60:
        return MaturityLevel.ADVANCED
    if score >= 30:
        return MaturityLevel.INITIAL
    return MaturityLevel.TRADITIONAL
