"""Report generation — JSON and Markdown scorecards + remediation roadmap."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from zerotrustmirror.models import BehaviorRecord, MaturityLevel, PillarResult, ZTAResult


REMEDIATION_TEMPLATES: dict[str, list[dict[str, Any]]] = {
    "identity": [
        {"action": "Enable MFA for all users", "priority": "high", "pillar": "identity"},
        {"action": "Deploy privileged access management (PAM)", "priority": "high", "pillar": "identity"},
        {"action": "Automate identity provisioning/deprovisioning", "priority": "medium", "pillar": "identity"},
        {"action": "Enable SSO across all applications", "priority": "medium", "pillar": "identity"},
        {"action": "Enforce service account rotation ≤90 days", "priority": "medium", "pillar": "identity"},
    ],
    "devices": [
        {"action": "Require device compliance for all access", "priority": "high", "pillar": "devices"},
        {"action": "Deploy endpoint posture attestation", "priority": "high", "pillar": "devices"},
        {"action": "Block unmanaged device access", "priority": "high", "pillar": "devices"},
        {"action": "Enable browser isolation for sensitive apps", "priority": "medium", "pillar": "devices"},
        {"action": "Achieve ≥80% device inventory coverage", "priority": "medium", "pillar": "devices"},
    ],
    "network": [
        {"action": "Implement micro-segmentation", "priority": "high", "pillar": "network"},
        {"action": "Define east-west traffic policies", "priority": "high", "pillar": "network"},
        {"action": "Deploy ≥2 network visibility tools", "priority": "medium", "pillar": "network"},
        {"action": "Replace VPN with ZTNA", "priority": "high", "pillar": "network"},
    ],
    "apps": [
        {"action": "Enforce least-privilege app access policy", "priority": "high", "pillar": "apps"},
        {"action": "Reduce externally reachable apps to ≤15%", "priority": "high", "pillar": "apps"},
        {"action": "Deploy API gateway", "priority": "medium", "pillar": "apps"},
        {"action": "Implement least-privilege delivery model", "priority": "medium", "pillar": "apps"},
    ],
    "data": [
        {"action": "Classify ≥80% of data assets", "priority": "high", "pillar": "data"},
        {"action": "Enable encryption at rest", "priority": "high", "pillar": "data"},
        {"action": "Deploy DLP controls", "priority": "high", "pillar": "data"},
        {"action": "Enforce need-to-know data sharing policy", "priority": "medium", "pillar": "data"},
    ],
    "automation": [
        {"action": "Enable automated policy enforcement", "priority": "high", "pillar": "automation"},
        {"action": "Deploy SOAR platform", "priority": "high", "pillar": "automation"},
        {"action": "Automate ≥70% of incident runbooks", "priority": "medium", "pillar": "automation"},
    ],
    "vis": [
        {"action": "Deploy SIEM with log aggregation", "priority": "high", "pillar": "vis"},
        {"action": "Enable behavioral analytics", "priority": "high", "pillar": "vis"},
        {"action": "Achieve ≥80% log coverage", "priority": "medium", "pillar": "vis"},
        {"action": "Create ≥100 detection rules", "priority": "medium", "pillar": "vis"},
    ],
}


def generate_remediation(pillars: list[PillarResult]) -> list[dict[str, Any]]:
    roadmap = []
    for p in pillars:
        if p.score < 80:
            for item in REMEDIATION_TEMPLATES.get(p.name, []):
                # Only include items that are actually failing
                failed_fields = {e.field for e in p.evidences if not e.present}
                field_suffix = item["pillar"] + "."
                if any(f.startswith(field_suffix) for f in failed_fields) or p.score < 40:
                    roadmap.append(item)
    return roadmap


def build_result(
    pillars: list[PillarResult],
    overall_score: float,
    maturity: MaturityLevel,
    behaviors: list[BehaviorRecord] | None = None,
) -> ZTAResult:
    behaviors = behaviors or []
    remediation = generate_remediation(pillars)
    return ZTAResult(
        overall_score=overall_score,
        maturity=maturity,
        pillars=pillars,
        behaviors=behaviors,
        remediation=remediation,
    )


def to_json(result: ZTAResult) -> str:
    data = {
        "overall_score": result.overall_score,
        "maturity": result.maturity.value,
        "pillars": [],
        "correlations": [],
        "remediation": result.remediation,
    }
    for p in result.pillars:
        data["pillars"].append({
            "name": p.name,
            "score": p.score,
            "maturity": p.maturity.value,
            "evidences": [
                {"field": e.field, "present": e.present, "detail": e.detail, "contribution": e.contribution}
                for e in p.evidences
            ],
        })
    for b in result.behaviors:
        data["correlations"].append({
            "user": b.user,
            "risk_score": b.risk_score,
            "policy_finding": b.policy_finding,
            "event_count": len(b.events),
            "channels": list(set(e.channel for e in b.events)),
        })
    return json.dumps(data, indent=2)


def to_markdown(result: ZTAResult) -> str:
    lines = [
        "# Zero-Trust Readiness Report",
        "",
        f"**Overall Score:** {result.overall_score}/100",
        f"**Maturity Level:** {result.maturity.value}",
        "",
        "## Per-Pillar Scores",
        "",
        "| Pillar | Score | Maturity | Evidence Fields |",
        "|--------|-------|----------|-----------------|",
    ]
    for p in result.pillars:
        fields = ", ".join(p.evidence_fields[:3]) + ("..." if len(p.evidence_fields) > 3 else "")
        lines.append(f"| {p.name} | {p.score} | {p.maturity.value} | {fields} |")

    if result.behaviors:
        lines.extend(["", "## Correlation Findings", ""])
        for b in result.behaviors:
            lines.append(f"- **{b.user}** (risk {b.risk_score}): {b.policy_finding}")
            lines.append(f"  Events: {len(b.events)}, Channels: {', '.join(sorted(set(e.channel for e in b.events)))}")

    if result.remediation:
        lines.extend(["", "## Remediation Roadmap", ""])
        for i, item in enumerate(result.remediation, 1):
            lines.append(f"{i}. [{item['priority'].upper()}] {item['action']} ({item['pillar']})")

    lines.append("")
    return "\n".join(lines)


def write_report(result: ZTAResult, out_dir: str | Path, prefix: str = "zta") -> dict[str, str]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{prefix}.json"
    md_path = out_dir / f"{prefix}.md"
    json_path.write_text(to_json(result), encoding="utf-8")
    md_path.write_text(to_markdown(result), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}
