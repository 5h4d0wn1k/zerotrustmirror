"""Data pillar evaluator."""
from __future__ import annotations

from zerotrustmirror.models import Evidence, MaturityLevel, PillarResult


def evaluate(cfg: dict) -> PillarResult:
    data = cfg.get("data", {})
    evidences: list[Evidence] = []
    score = 0

    classification = data.get("data_classification_coverage_pct", 0)
    cls_ok = classification >= 80
    evidences.append(Evidence("data.data_classification_coverage_pct", cls_ok, f"Classification: {classification}%", 25 if cls_ok else (10 if classification > 0 else 0)))
    score += 25 if cls_ok else (10 if classification > 0 else 0)

    enc_rest = data.get("encryption_at_rest", False)
    evidences.append(Evidence("data.encryption_at_rest", enc_rest, f"Encryption at rest: {enc_rest}", 20 if enc_rest else 0))
    score += 20 if enc_rest else 0

    enc_transit = data.get("encryption_in_transit", False)
    evidences.append(Evidence("data.encryption_in_transit", enc_transit, f"Encryption in transit: {enc_transit}", 15 if enc_transit else 0))
    score += 15 if enc_transit else 0

    dlp = data.get("dlp_controls", False)
    evidences.append(Evidence("data.dlp_controls", dlp, f"DLP controls: {dlp}", 20 if dlp else 0))
    score += 20 if dlp else 0

    sharing = data.get("data_sharing_policy", "unrestricted")
    sharing_ok = sharing in ("need-to-know", "restricted", "encrypted-only")
    evidences.append(Evidence("data.data_sharing_policy", sharing_ok, f"Sharing policy: {sharing}", 20 if sharing_ok else 0))
    score += 20 if sharing_ok else 0

    score = min(score, 100)
    maturity = _maturity(score)
    return PillarResult(name="data", score=score, maturity=maturity, evidences=evidences)


def _maturity(score: int) -> MaturityLevel:
    if score >= 80:
        return MaturityLevel.OPTIMAL
    if score >= 60:
        return MaturityLevel.ADVANCED
    if score >= 30:
        return MaturityLevel.INITIAL
    return MaturityLevel.TRADITIONAL
