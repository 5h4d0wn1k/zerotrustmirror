"""Automation/Orchestration pillar evaluator."""
from __future__ import annotations

from zerotrustmirror.models import Evidence, MaturityLevel, PillarResult


def evaluate(cfg: dict) -> PillarResult:
    auto = cfg.get("automation", {})
    evidences: list[Evidence] = []
    score = 0

    enforcement = auto.get("automated_policy_enforcement", False)
    evidences.append(Evidence("automation.automated_policy_enforcement", enforcement, f"Auto enforcement: {enforcement}", 30 if enforcement else 0))
    score += 30 if enforcement else 0

    soar = auto.get("soar_platform", False)
    evidences.append(Evidence("automation.soar_platform", soar, f"SOAR: {soar}", 30 if soar else 0))
    score += 30 if soar else 0

    auto_rb = auto.get("incident_runbooks_automated", 0)
    total_rb = auto.get("total_incident_runbooks", 1)
    rb_ratio = auto_rb / max(total_rb, 1)
    rb_ok = rb_ratio >= 0.70
    evidences.append(Evidence("automation.incident_runbooks_automated", rb_ok, f"Runbooks automated: {auto_rb}/{total_rb} ({rb_ratio:.0%})", 25 if rb_ok else (10 if rb_ratio > 0 else 0)))
    score += 25 if rb_ok else (10 if rb_ratio > 0 else 0)

    if enforcement and soar:
        score += 15
        evidences.append(Evidence("automation.enforcement_soar_bonus", True, "Enforcement+SOAR bonus", 15))

    score = min(score, 100)
    maturity = _maturity(score)
    return PillarResult(name="automation", score=score, maturity=maturity, evidences=evidences)


def _maturity(score: int) -> MaturityLevel:
    if score >= 80:
        return MaturityLevel.OPTIMAL
    if score >= 60:
        return MaturityLevel.ADVANCED
    if score >= 30:
        return MaturityLevel.INITIAL
    return MaturityLevel.TRADITIONAL
