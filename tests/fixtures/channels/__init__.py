"""Correlation fixtures — multi-channel logs for alice@example.com."""
import json

WEB_LOGS = [
    {"channel": "web", "timestamp": 1000.0, "user": "alice@example.com", "event_type": "login_success", "src_ip": "198.51.100.23", "detail": "SSO login via browser"},
    {"channel": "web", "timestamp": 1005.0, "user": "alice@example.com", "event_type": "file_download", "src_ip": "198.51.100.23", "detail": "Downloaded quarterly-report.xlsx"},
    {"channel": "web", "timestamp": 1012.0, "user": "bob@example.com", "event_type": "login_success", "src_ip": "203.0.113.7", "detail": "Direct login"},
]

NETWORK_LOGS = [
    {"channel": "network", "timestamp": 1001.0, "user": "alice@example.com", "event_type": "dns_query", "src_ip": "198.51.100.23", "detail": "query internal-db.corp"},
    {"channel": "network", "timestamp": 1008.0, "user": "alice@example.com", "event_type": "lateral_movement_attempt", "src_ip": "198.51.100.23", "detail": "SSH to 10.0.0.55 blocked"},
    {"channel": "network", "timestamp": 1020.0, "user": "charlie@example.com", "event_type": "dns_query", "src_ip": "192.0.2.44", "detail": "query external-api.com"},
]

HOST_LOGS = [
    {"channel": "host", "timestamp": 1003.0, "user": "alice@example.com", "event_type": "process_execution", "src_ip": "198.51.100.23", "detail": "powershell.exe -enc ..."},
    {"channel": "host", "timestamp": 1010.0, "user": "alice@example.com", "event_type": "privilege_escalation", "src_ip": "198.51.100.23", "detail": "attempted UAC bypass"},
    {"channel": "host", "timestamp": 1030.0, "user": "dave@example.com", "event_type": "process_execution", "src_ip": "198.51.100.99", "detail": "notepad.exe"},
]


def write_channel_fixtures(tmpdir):
    """Write channel log fixtures to disk and return paths."""
    paths = {}
    for name, data in [("web.json", WEB_LOGS), ("network.json", NETWORK_LOGS), ("host.json", HOST_LOGS)]:
        p = tmpdir / name
        p.write_text(json.dumps(data, indent=2))
        paths[name.split(".")[0]] = str(p)
    return paths
