from enum import Enum


class LogSource(str, Enum):
    EHR = "EHR"
    VPN = "VPN"
    FIREWALL = "FIREWALL"
    IDS = "IDS"
    MEDICAL_IOT = "MEDICAL_IOT"
    CLOUD = "CLOUD"


class EventSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class EventStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class UserRole(str, Enum):
    DOCTOR = "DOCTOR"
    NURSE = "NURSE"
    ADMIN = "ADMIN"
    SYSTEM = "SYSTEM"