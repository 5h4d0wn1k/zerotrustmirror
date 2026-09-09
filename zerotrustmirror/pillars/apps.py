"""Apps pillar evaluator."""
from __future__ import annotations

from zerotrustmirror.models import Evidence, MaturityLevel, PillarResult


def evaluate(cfg: dict) -> PillarResult:
    apps = cfg.get("apps", {})
    evidences: list[Evidence] = []
    score = 0

    policy = apps.get("app_access_policy", "allow-all")
    policy_ok = policy in ("least-privilege", "zero-trust", "deny-by-default")
    evidences.append(Evidence("apps.app_access_policy", policy_ok, f"Access policy: {policy}", 25 if policy_ok else 0))
    score += 25 if policy_ok else 0

    lpd = apps.get("least_privilege_delivery", False)
    evidences.append(Evidence("apps.least_privilege_delivery", lpd, f"Least-privilege delivery: {lpd}", 20 if lpd else 0))
    score += 20 if lpd else 0

    pub = apps.get("public_app_count", 0)
    internal = apps.get("internal_app_count", 0)
    reachable = apps.get("externally_reachable_apps", 0)
    total = pub + internal if (pub + internal) > 0 else 1
    exposure_ratio = reachable / total
    exposure_ok = exposure_ratio <= 0.15
    evidences.append(Evidence("apps.externally_reachable_apps", exposure_ok, f"Exposure: {reachable}/{total} ({exposure_ratio:.0%})", 25 if exposure_ok else (10 if exposure_ratio <= 0.30 else 0)))
    score += 25 if exposure_ok else (10 if exposure_ratio <= 0.30 else 0)

    gw = apps.get("api_gateway", False)
    evidences.append(Evidence("apps.api_gateway", gw, f"API gateway: {gw}", 15 if gw else 0))
    score += 15 if gw else 0

    # remaining: bonus for clean policy
    if policy_ok and lpd:
        score += 15
        evidences.append(Evidence("apps.policy_lpd_bonus", True, "Policy+LPD bonus", 15))

    score = min(score, 100)
    maturity = _maturity(score)
    return PillarResult(name="apps", score=score, maturity=maturity, evidences=evidences)


def _maturity(score: int) -> MaturityLevel:
    if score >= 80:
        return MaturityLevel.OPTIMAL
    if score >= 60:
        return MaturityLevel.ADVANCED
    if score >= 30:
        return MaturityLevel.INITIAL
    return MaturityLevel.TRADITIONAL
