"""Strong environment pack — mature zero-trust posture."""
STRONG_ENV = {
    "org_name": "ExampleOrg-Strong",
    "identity": {
        "mfa_enabled": True,
        "mfa_coverage_pct": 98,
        "privileged_access_management": True,
        "identity_provisioning_automated": True,
        "sso_enabled": True,
        "service_account_rotation_days": 30,
    },
    "devices": {
        "device_compliance_required": True,
        "endpoint_posture_attestation": True,
        "unmanaged_device_access_allowed": False,
        "browser_isolation": True,
        "device_inventory_coverage_pct": 95,
    },
    "network": {
        "micro_segmentation": True,
        "east_west_policy": True,
        "network_visibility_tools": ["nids", "east-west-monitor", "dns-logs"],
        "remote_access_vpn_only": False,
        "zero_trust_network_access": True,
    },
    "apps": {
        "app_access_policy": "least-privilege",
        "least_privilege_delivery": True,
        "public_app_count": 50,
        "internal_app_count": 100,
        "externally_reachable_apps": 10,
        "api_gateway": True,
    },
    "data": {
        "data_classification_coverage_pct": 92,
        "encryption_at_rest": True,
        "encryption_in_transit": True,
        "dlp_controls": True,
        "data_sharing_policy": "need-to-know",
    },
    "automation": {
        "automated_policy_enforcement": True,
        "soar_platform": True,
        "incident_runbooks_automated": 9,
        "total_incident_runbooks": 10,
    },
    "vis": {
        "log_aggregation": True,
        "siem_present": True,
        "behavioral_analytics": True,
        "detection_rules_count": 250,
        "log_coverage_pct": 95,
    },
}
