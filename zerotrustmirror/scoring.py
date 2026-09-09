"""Compute weighted ZTA scores and maturity levels."""
from __future__ import annotations

from zerotrustmirror.models import (
    MaturityLevel,
    PillarResult,
    PILLAR_WEIGHTS,
)

# Import all pillar evaluators
from zerotrustmirror.pillars import identity, devices, network, apps, data, automation, vis

EVALUATORS = {
    "identity": identity,
    "devices": devices,
    "network": network,
    "apps": apps,
    "data": data,
    "automation": automation,
    "vis": vis,
}


def evaluate_all(cfg: dict) -> list[PillarResult]:
    results = []
    for name, mod in EVALUATORS.items():
        results.append(mod.evaluate(cfg))
    return results


def compute_weighted_score(pillars: list[PillarResult]) -> float:
    total = 0.0
    for p in pillars:
        weight = PILLAR_WEIGHTS.get(p.name, 0.1)
        total += p.score * weight
    return round(total, 1)


def determine_maturity(score: float) -> MaturityLevel:
    if score >= 80:
        return MaturityLevel.OPTIMAL
    if score >= 60:
        return MaturityLevel.ADVANCED
    if score >= 30:
        return MaturityLevel.INITIAL
    return MaturityLevel.TRADITIONAL
