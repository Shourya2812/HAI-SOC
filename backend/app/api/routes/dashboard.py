"""
backend/app/api/routes/dashboard.py

REST endpoints for dashboard analytics.
"""

from fastapi import APIRouter

from backend.app.schemas.dashboard_schema import (
    DashboardOverviewResponse,
    RiskDistributionItem,
    SourceDistributionItem,
    DepartmentDistributionItem,
    ModelDistributionItem,
    DailyTrendItem,
    SystemHealthResponse,
    RecentLogItem,
    RecentIncidentItem,
    RecentAnomalyItem,
)

from backend.app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

# =====================================================
# OVERVIEW
# =====================================================

@router.get(
    "/overview",
    response_model=DashboardOverviewResponse,
)
def get_dashboard_overview():

    return DashboardService.get_overview()


# =====================================================
# RISK DISTRIBUTION
# =====================================================

@router.get(
    "/risk-distribution",
    response_model=list[RiskDistributionItem],
)
def get_risk_distribution():

    return DashboardService.get_risk_distribution()


# =====================================================
# SOURCE DISTRIBUTION
# =====================================================

@router.get(
    "/sources",
    response_model=list[SourceDistributionItem],
)
def get_sources():

    return DashboardService.get_sources()


# =====================================================
# DEPARTMENT DISTRIBUTION
# =====================================================

@router.get(
    "/departments",
    response_model=list[DepartmentDistributionItem],
)
def get_departments():

    return DashboardService.get_departments()


# =====================================================
# MODEL USAGE
# =====================================================

@router.get(
    "/models",
    response_model=list[ModelDistributionItem],
)
def get_models():

    return DashboardService.get_models()


# =====================================================
# DAILY ANOMALY TREND
# =====================================================

@router.get(
    "/anomaly-trend",
    response_model=list[DailyTrendItem],
)
def get_anomaly_trend():

    return DashboardService.get_daily_trend()


# =====================================================
# SYSTEM HEALTH
# =====================================================

@router.get(
    "/system-health",
    response_model=SystemHealthResponse,
)
def get_system_health():

    return DashboardService.get_system_health()


# =====================================================
# RECENT LOGS
# =====================================================

@router.get(
    "/recent-logs",
    response_model=list[RecentLogItem],
)
def get_recent_logs():

    return DashboardService.get_recent_logs()


# =====================================================
# RECENT INCIDENTS
# =====================================================

@router.get(
    "/recent-incidents",
    response_model=list[RecentIncidentItem],
)
def get_recent_incidents():

    return DashboardService.get_recent_incidents()


# =====================================================
# RECENT ANOMALIES
# =====================================================

@router.get(
    "/recent-anomalies",
    response_model=list[RecentAnomalyItem],
)
def get_recent_anomalies():

    return DashboardService.get_recent_anomalies()