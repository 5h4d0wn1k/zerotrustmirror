"""Data models for ZTA evaluation."""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any


class MaturityLevel(enum.Enum):
    TRADITIONAL = "Traditional"
    INITIAL = "Initial"
    ADVANCED = "Advanced"
    OPTIMAL = "Optimal"


PILLAR_NAMES = [
    "identity",
    "devices",
    "network",
    "apps",
    "data",
    "automation",
    "vis",
]

PILLAR_WEIGHTS = {
    "identity": 0.20,
    "devices": 0.15,
    "network": 0.15,
    "apps": 0.15,
    "data": 0.15,
    "automation": 0.10,
    "vis": 0.10,
}


@dataclass
class Evidence:
    field: str
    present: bool
    detail: str
    contribution: int  # +/− contribution to score


@dataclass
class PillarResult:
    name: str
    score: int  # 0-100
    maturity: MaturityLevel
    evidences: list[Evidence] = field(default_factory=list)

    @property
    def evidence_fields(self) -> list[str]:
        return [e.field for e in self.evidences]


@dataclass
class CorrelationRecord:
    user: str
    channel: str
    timestamp: float
    event_type: str
    detail: str
    risk_score: float


@dataclass
class BehaviorRecord:
    user: str
    events: list[CorrelationRecord] = field(default_factory=list)
    risk_score: float = 0.0
    policy_finding: str = ""


@dataclass
class ZTAResult:
    overall_score: float
    maturity: MaturityLevel
    pillars: list[PillarResult] = field(default_factory=list)
    behaviors: list[BehaviorRecord] = field(default_factory=list)
    remediation: list[dict[str, Any]] = field(default_factory=list)
