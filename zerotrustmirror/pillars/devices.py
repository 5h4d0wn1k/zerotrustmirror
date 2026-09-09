"""Devices pillar evaluator."""
from __future__ import annotations

from zerotrustmirror.models import Evidence, MaturityLevel, PillarResult


def evaluate(cfg: dict) -> PillarResult:
    dev = cfg.get("devices", {})
    evidences: list[Evidence] = []
    score = 0

    compliance = dev.get("device_compliance_required", False)
    evidences.append(Evidence("devices.device_compliance_required", compliance, f"Compliance required: {compliance}", 25 if compliance else 0))
    score += 25 if compliance else 0

    posture = dev.get("endpoint_posture_attestation", False)
    evidences.append(Evidence("devices.endpoint_posture_attestation", posture, f"Posture attestation: {posture}", 25 if posture else 0))
    score += 25 if posture else 0

    unmanaged = dev.get("unmanaged_device_access_allowed", True)
    no_unmanaged = not unmanaged
    evidences.append(Evidence("devices.unmanaged_device_access_allowed", no_unmanaged, f"Unmanaged access blocked: {no_unmanaged}", 20 if no_unmanaged else 0))
    score += 20 if no_unmanaged else 0

    isolation = dev.get("browser_isolation", False)
    evidences.append(Evidence("devices.browser_isolation", isolation, f"Browser isolation: {isolation}", 15 if isolation else 0))
    score += 15 if isolation else 0

    inv = dev.get("device_inventory_coverage_pct", 0)
    inv_ok = inv >= 80
    evidences.append(Evidence("devices.device_inventory_coverage_pct", inv_ok, f"Inventory coverage: {inv}%", 15 if inv_ok else (5 if inv >= 40 else 0)))
    score += 15 if inv_ok else (5 if inv >= 40 else 0)

    score = min(score, 100)
    maturity = _maturity(score)
    return PillarResult(name="devices", score=score, maturity=maturity, evidences=evidences)


def _maturity(score: int) -> MaturityLevel:
    if score >= 80:
        return MaturityLevel.OPTIMAL
    if score >= 60:
        return MaturityLevel.ADVANCED
    if score >= 30:
        return MaturityLevel.INITIAL
    return MaturityLevel.TRADITIONAL
