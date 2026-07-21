"""
Shared constants used by all synthetic healthcare log generators.

This module defines the hospital environment simulated
throughout the HAI-SOC project.
"""

# ==========================================================
# Hospital Environment
# ==========================================================

DEPARTMENTS = [
    "Cardiology",
    "Neurology",
    "Radiology",
    "Emergency",
    "ICU",
    "Oncology",
    "Orthopedics",
    "Pediatrics",
    "Pharmacy",
    "Laboratory",
]

USERS = [

    # Doctors
    {
        "username": "dr_smith",
        "role": "DOCTOR",
        "department": "Cardiology",
    },
    {
        "username": "dr_jones",
        "role": "DOCTOR",
        "department": "Neurology",
    },
    {
        "username": "dr_clark",
        "role": "DOCTOR",
        "department": "Oncology",
    },

    # Nurses
    {
        "username": "nurse_adams",
        "role": "NURSE",
        "department": "ICU",
    },
    {
        "username": "nurse_williams",
        "role": "NURSE",
        "department": "Emergency",
    },
    {
        "username": "nurse_johnson",
        "role": "NURSE",
        "department": "Pediatrics",
    },

    # Lab Technicians
    {
        "username": "lab_taylor",
        "role": "LAB_TECHNICIAN",
        "department": "Laboratory",
    },
    {
        "username": "lab_walker",
        "role": "LAB_TECHNICIAN",
        "department": "Laboratory",
    },

    # Radiologists
    {
        "username": "radio_lee",
        "role": "RADIOLOGIST",
        "department": "Radiology",
    },
    {
        "username": "radio_white",
        "role": "RADIOLOGIST",
        "department": "Radiology",
    },

    # Admin
    {
        "username": "admin_green",
        "role": "ADMIN",
        "department": "Administration",
    },
]

ASSETS = [
    "EHR Server",
    "Patient Database",
    "Prescription Service",
    "Laboratory Information System",
    "Radiology PACS",
    "Authentication Server",
    "VPN Gateway",
    "Firewall",
    "IDS Sensor",
    "Core Switch",
    "Backup Server",
]

# ==========================================================
# Generic Events
# ==========================================================

EVENT_TYPES = [

    # EHR
    "LOGIN",
    "LOGOUT",
    "VIEW_RECORD",
    "UPDATE_RECORD",
    "CREATE_RECORD",
    "DOWNLOAD_RECORD",
    "PRINT_RECORD",
    "PASSWORD_RESET",

    # VPN
    "VPN_LOGIN",
    "VPN_CONNECTED",
    "VPN_LOGOUT",

    # Firewall
    "ALLOW",
    "DENY",
    "BLOCKED_PORT_SCAN",
    "BLOCKED_IP",
]

STATUS = [
    "SUCCESS",
    "FAILED",
    "BLOCKED",
]

# ==========================================================
# Network Constants
# ==========================================================

PROTOCOLS = [
    "TCP",
    "UDP",
]

COMMON_PORTS = [
    22,     # SSH
    53,     # DNS
    80,     # HTTP
    443,    # HTTPS
    3306,   # MySQL
    5432,   # PostgreSQL
    8080,   # Alternate HTTP
]

FIREWALL_RULE_IDS = [
    "FW-101",
    "FW-102",
    "FW-201",
    "FW-301",
]

VPN_GATEWAYS = [
    "VPN-GW-01",
    "VPN-GW-02",
]

# ==========================================================
# Event Severity
# ==========================================================

EVENT_SEVERITY = {

    # ---------------- EHR ----------------
    "LOGIN": "LOW",
    "LOGOUT": "LOW",
    "VIEW_RECORD": "LOW",
    "UPDATE_RECORD": "MEDIUM",
    "CREATE_RECORD": "MEDIUM",
    "PRINT_RECORD": "LOW",
    "DOWNLOAD_RECORD": "HIGH",
    "PASSWORD_RESET": "HIGH",

    # ---------------- VPN ----------------
    "VPN_LOGIN": "LOW",
    "VPN_CONNECTED": "LOW",
    "VPN_LOGOUT": "LOW",

    # ---------------- Firewall ----------------
    "ALLOW": "LOW",
    "DENY": "MEDIUM",
    "BLOCKED_PORT_SCAN": "HIGH",
    "BLOCKED_IP": "HIGH",
}

# ==========================================================
# Event Descriptions
# ==========================================================

EVENT_DESCRIPTIONS = {

    # ---------------- EHR ----------------
    "LOGIN": "User logged into the EHR system.",
    "LOGOUT": "User logged out of the EHR system.",
    "VIEW_RECORD": "Patient medical record accessed.",
    "UPDATE_RECORD": "Patient medical record updated.",
    "CREATE_RECORD": "New patient medical record created.",
    "DOWNLOAD_RECORD": "Patient medical record downloaded.",
    "PRINT_RECORD": "Patient medical record printed.",
    "PASSWORD_RESET": "User password reset requested.",

    # ---------------- VPN ----------------
    "VPN_LOGIN": "User initiated VPN authentication.",
    "VPN_CONNECTED": "VPN tunnel established successfully.",
    "VPN_LOGOUT": "VPN session terminated.",

    # ---------------- Firewall ----------------
    "ALLOW": "Network traffic allowed by firewall.",
    "DENY": "Network traffic denied by firewall.",
    "BLOCKED_PORT_SCAN": "Port scan blocked by firewall.",
    "BLOCKED_IP": "Traffic blocked from blacklisted IP.",
}