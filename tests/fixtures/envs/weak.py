"""Weak environment pack — minimal zero-trust posture."""
WEAK_ENV = {
    "org_name": "ExampleOrg-Weak",
    "identity": {
        "mfa_enabled": False,
        "mfa_coverage_pct": 0,
        "privileged_access_management": False,
        "identity_provisioning_automated": False,
        "sso_enabled": False,
        "service_account_rotation_days": 365,
    },
    "devices": {
        "device_compliance_required": False,
        "endpoint_posture_attestation": False,
        "unmanaged_device_access_allowed": True,
        "browser_isolation": False,
        "device_inventory_coverage_pct": 10,
    },
    "network": {
        "micro_segmentation": False,
        "east_west_policy": False,
        "network_visibility_tools": [],
        "remote_access_vpn_only": True,
        "zero_trust_network_access": False,
    },
    "apps": {
        "app_access_policy": "allow-all",
        "least_privilege_delivery": False,
        "public_app_count": 50,
        "internal_app_count": 100,
        "externally_reachable_apps": 80,
        "api_gateway": False,
    },
    "data": {
        "data_classification_coverage_pct": 0,
        "encryption_at_rest": False,
        "encryption_in_transit": True,
        "dlp_controls": False,
        "data_sharing_policy": "unrestricted",
    },
    "automation": {
        "automated_policy_enforcement": False,
        "soar_platform": False,
        "incident_runbooks_automated": 0,
        "total_incident_runbooks": 10,
    },
    "vis": {
        "log_aggregation": False,
        "siem_present": False,
        "behavioral_analytics": False,
        "detection_rules_count": 0,
        "log_coverage_pct": 5,
    },
}
