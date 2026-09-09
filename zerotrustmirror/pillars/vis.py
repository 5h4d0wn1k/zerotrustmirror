"""Visibility/Analytics pillar evaluator."""
from __future__ import annotations

from zerotrustmirror.models import Evidence, MaturityLevel, PillarResult


def evaluate(cfg: dict) -> PillarResult:
    vis = cfg.get("vis", {})
    evidences: list[Evidence] = []
    score = 0

    aggregation = vis.get("log_aggregation", False)
    evidences.append(Evidence("vis.log_aggregation", aggregation, f"Log aggregation: {aggregation}", 20 if aggregation else 0))
    score += 20 if aggregation else 0

    siem = vis.get("siem_present", False)
    evidences.append(Evidence("vis.siem_present", siem, f"SIEM: {siem}", 25 if siem else 0))
    score += 25 if siem else 0

    ba = vis.get("behavioral_analytics", False)
    evidences.append(Evidence("vis.behavioral_analytics", ba, f"Behavioral analytics: {ba}", 20 if ba else 0))
    score += 20 if ba else 0

    rules = vis.get("detection_rules_count", 0)
    rules_ok = rules >= 100
    evidences.append(Evidence("vis.detection_rules_count", rules_ok, f"Detection rules: {rules}", 15 if rules_ok else (5 if rules > 0 else 0)))
    score += 15 if rules_ok else (5 if rules > 0 else 0)

    coverage = vis.get("log_coverage_pct", 0)
    cov_ok = coverage >= 80
    evidences.append(Evidence("vis.log_coverage_pct", cov_ok, f"Log coverage: {coverage}%", 20 if cov_ok else (5 if coverage > 0 else 0)))
    score += 20 if cov_ok else (5 if coverage > 0 else 0)

    score = min(score, 100)
    maturity = _maturity(score)
    return PillarResult(name="vis", score=score, maturity=maturity, evidences=evidences)


def _maturity(score: int) -> MaturityLevel:
    if score >= 80:
        return MaturityLevel.OPTIMAL
    if score >= 60:
        return MaturityLevel.ADVANCED
    if score >= 30:
        return MaturityLevel.INITIAL
    return MaturityLevel.TRADITIONAL
