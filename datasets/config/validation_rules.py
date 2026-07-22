REQUIRED_FIELDS = {

    "EHR": [
        "timestamp",
        "source",
        "event_type",
        "user",
        "role",
        "department",
        "asset",
        "severity",
        "status",
        "source_ip",
        "destination_ip",
        "description",
        "extra"
    ],

    "VPN": [
        "timestamp",
        "source",
        "event_type",
        "user",
        "severity",
        "status",
        "source_ip",
        "destination_ip",
        "description",
        "extra"
    ],

    "FIREWALL": [
        "timestamp",
        "source",
        "event_type",
        "severity",
        "status",
        "source_ip",
        "destination_ip",
        "description",
        "extra"
    ]
}

VALID_SEVERITIES = {
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL"
}

VALID_STATUS = {

    "EHR": {
        "SUCCESS",
        "FAILED"
    },

    "VPN": {
        "SUCCESS",
        "FAILED"
    },

    "FIREWALL": {
        "SUCCESS",
        "BLOCKED",
    }
}

VALID_SOURCES = {
    "EHR",
    "VPN",
    "FIREWALL"
}