"""
backend/app/schemas/dashboard_schema.py

Pydantic schemas used by the Dashboard API.
"""

from pydantic import BaseModel


# =====================================================
# Dashboard Overview
# =====================================================

class DashboardOverviewResponse(BaseModel):
    total_logs: int
    todays_anomalies: int
    open_incidents: int
    critical_incidents: int

    logs_trend_pct: float
    anomalies_trend_pct: float
    incidents_trend_pct: float
    critical_trend_pct: float

    active_hospital: str
    system_health: str


# =====================================================
# Risk Distribution
# =====================================================

class RiskDistributionItem(BaseModel):
    category: str
    count: int
    percentage: float
    color: str


# =====================================================
# Source Distribution
# =====================================================

class SourceDistributionItem(BaseModel):
    source: str
    count: int
    color: str


# =====================================================
# Department Distribution
# =====================================================

class DepartmentDistributionItem(BaseModel):
    department: str
    count: int
    color: str


# =====================================================
# Model Usage
# =====================================================

class ModelDistributionItem(BaseModel):
    model: str
    count: int
    accuracy: float

# =====================================================
# Daily Trend
# =====================================================

class DailyTrendItem(BaseModel):
    hour: str
    anomalies: int
    baseline: int


# =====================================================
# System Health
# =====================================================

class SystemHealthResponse(BaseModel):
    mongodb: str
    backend: str
    ml_model: str
    api: str
    uptime: str


# =====================================================
# Recent Logs
# =====================================================

class RecentLogItem(BaseModel):
    id: str
    timestamp: str
    severity: str
    source: str
    message: str


# =====================================================
# Recent Incidents
# =====================================================

class RecentIncidentItem(BaseModel):
    id: str
    title: str
    severity: str
    status: str


# =====================================================
# Recent Anomalies
# =====================================================

class RecentAnomalyItem(BaseModel):
    id: str
    detector: str
    score: float
    prediction: int