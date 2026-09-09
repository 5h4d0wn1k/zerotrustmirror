"""Identity pillar evaluator."""
from __future__ import annotations

from zerotrustmirror.models import Evidence, MaturityLevel, PillarResult


def evaluate(cfg: dict) -> PillarResult:
    ident = cfg.get("identity", {})
    evidences: list[Evidence] = []
    score = 0

    mfa = ident.get("mfa_enabled", False)
    mfa_cov = ident.get("mfa_coverage_pct", 0)
    evidences.append(Evidence("identity.mfa_enabled", mfa, f"MFA enabled: {mfa}", 15 if mfa else 0))
    score += 15 if mfa else 0
    evidences.append(Evidence("identity.mfa_coverage_pct", mfa_cov > 80, f"MFA coverage {mfa_cov}%", 10 if mfa_cov > 80 else (5 if mfa_cov > 0 else 0)))
    score += 10 if mfa_cov > 80 else (5 if mfa_cov > 0 else 0)

    pam = ident.get("privileged_access_management", False)
    evidences.append(Evidence("identity.privileged_access_management", pam, f"PAM: {pam}", 20 if pam else 0))
    score += 20 if pam else 0

    prov = ident.get("identity_provisioning_automated", False)
    evidences.append(Evidence("identity.identity_provisioning_automated", prov, f"Automated provisioning: {prov}", 15 if prov else 0))
    score += 15 if prov else 0

    sso = ident.get("sso_enabled", False)
    evidences.append(Evidence("identity.sso_enabled", sso, f"SSO: {sso}", 10 if sso else 0))
    score += 10 if sso else 0

    rot = ident.get("service_account_rotation_days", 365)
    rot_ok = rot <= 90
    evidences.append(Evidence("identity.service_account_rotation_days", rot_ok, f"Rotation: {rot}d (threshold 90d)", 10 if rot_ok else (5 if rot <= 180 else 0)))
    score += 10 if rot_ok else (5 if rot <= 180 else 0)

    score = min(score, 100)
    maturity = _maturity(score)
    return PillarResult(name="identity", score=score, maturity=maturity, evidences=evidences)


def _maturity(score: int) -> MaturityLevel:
    if score >= 80:
        return MaturityLevel.OPTIMAL
    if score >= 60:
        return MaturityLevel.ADVANCED
    if score >= 30:
        return MaturityLevel.INITIAL
    return MaturityLevel.TRADITIONAL
