"""
Shared constants used by all synthetic healthcare log generators.

This module defines the hospital environment that is simulated
throughout the HAI-SOC project.
"""


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
    {
        "username": "dr_smith",
        "role": "DOCTOR",
        "department": "Cardiology",
    },
    {
        "username": "nurse_adams",
        "role": "NURSE",
        "department": "ICU",
    },
    {
        "username": "lab_taylor",
        "role": "LAB_TECHNICIAN",
        "department": "Laboratory",
    },
]

ASSETS = [
    "EHR Server",
    "Patient Database",
    "Prescription Service",
    "Laboratory Information System",
    "Radiology PACS",
    "Authentication Server",
]

EVENT_TYPES = [
    "LOGIN",
    "LOGOUT",
    "VIEW_RECORD",
    "UPDATE_RECORD",
    "CREATE_RECORD",
    "DOWNLOAD_RECORD",
    "PRINT_RECORD",
    "PASSWORD_RESET",
]

STATUS = [
    "SUCCESS",
    "FAILED"
]

EVENT_SEVERITY = {
    "LOGIN": "LOW",
    "LOGOUT": "LOW",
    "VIEW_RECORD": "LOW",
    "UPDATE_RECORD": "MEDIUM",
    "CREATE_RECORD": "MEDIUM",
    "PRINT_RECORD": "LOW",
    "DOWNLOAD_RECORD": "HIGH",
    "PASSWORD_RESET": "HIGH",
}

EVENT_DESCRIPTIONS = {
    "LOGIN": "User logged into the EHR system.",
    "LOGOUT": "User logged out of the EHR system.",
    "VIEW_RECORD": "Patient medical record accessed.",
    "UPDATE_RECORD": "Patient medical record updated.",
    "CREATE_RECORD": "New patient medical record created.",
    "DOWNLOAD_RECORD": "Patient medical record downloaded.",
    "PRINT_RECORD": "Patient medical record printed.",
    "PASSWORD_RESET": "User password reset requested.",
}