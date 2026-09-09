"""Multichannel correlation engine — ties same-user activity across web/net/host."""
from __future__ import annotations

from zerotrustmirror.models import BehaviorRecord, CorrelationRecord

DEFAULT_WINDOW_SECONDS = 120.0


def _to_record(raw: dict) -> CorrelationRecord:
    return CorrelationRecord(
        user=raw.get("user", "unknown"),
        channel=raw.get("channel", "unknown"),
        timestamp=float(raw.get("timestamp", 0)),
        event_type=raw.get("event_type", "unknown"),
        detail=raw.get("detail", ""),
        risk_score=0.0,
    )


RISK_WEIGHTS = {
    "login_success": 0.05,
    "file_download": 0.15,
    "dns_query": 0.05,
    "lateral_movement_attempt": 0.70,
    "process_execution": 0.20,
    "privilege_escalation": 0.80,
}


def _event_risk(event_type: str) -> float:
    return RISK_WEIGHTS.get(event_type, 0.10)


def correlate(
    channel_logs: list[list[dict]],
    window: float = DEFAULT_WINDOW_SECONDS,
) -> list[BehaviorRecord]:
    """Correlate same-user events across multiple channels within a time window."""
    all_records: list[CorrelationRecord] = []
    for logs in channel_logs:
        for raw in logs:
            all_records.append(_to_record(raw))

    # Group by user
    user_events: dict[str, list[CorrelationRecord]] = {}
    for rec in all_records:
        user_events.setdefault(rec.user, []).append(rec)

    behaviors: list[BehaviorRecord] = []
    for user, events in user_events.items():
        events.sort(key=lambda e: e.timestamp)
        # Sliding window correlation
        used = set()
        for i, ev in enumerate(events):
            if i in used:
                continue
            cluster = [ev]
            used.add(i)
            for j in range(i + 1, len(events)):
                if j in used:
                    continue
                if events[j].timestamp - ev.timestamp <= window:
                    cluster.append(events[j])
                    used.add(j)

            if len(cluster) >= 2:
                channels = set(e.channel for e in cluster)
                # Risk = max event risk * channel multiplier
                max_risk = max(_event_risk(e.event_type) for e in cluster)
                channel_mult = 1.0 + 0.15 * (len(channels) - 1)
                risk = round(min(max_risk * channel_mult, 1.0), 2)
                for e in cluster:
                    e.risk_score = risk
                finding = _generate_finding(cluster, channels, risk)
                br = BehaviorRecord(user=user, events=cluster, risk_score=risk, policy_finding=finding)
                behaviors.append(br)

    behaviors.sort(key=lambda b: b.risk_score, reverse=True)
    return behaviors


def _generate_finding(events: list[CorrelationRecord], channels: set, risk: float) -> str:
    event_types = [e.event_type for e in events]
    ch_str = "+".join(sorted(channels))
    if "privilege_escalation" in event_types:
        return f"CRITICAL: privilege escalation correlated across {ch_str} — risk {risk}"
    if "lateral_movement_attempt" in event_types:
        return f"HIGH: lateral movement attempt correlated across {ch_str} — risk {risk}"
    if risk >= 0.5:
        return f"Medium-High: suspicious multi-channel activity ({ch_str}) — risk {risk}"
    return f"Info: correlated activity across {ch_str} — risk {risk}"
