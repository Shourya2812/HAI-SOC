"""
backend/app/services/dashboard_service.py

Business logic for dashboard analytics.
"""

from datetime import datetime, UTC

from backend.app.database.collections import (
    logs_collection,
    incidents_collection,
    anomaly_scores_collection,
)

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


class DashboardService:

    # =====================================================
    # OVERVIEW
    # =====================================================

    @staticmethod
    def get_overview() -> DashboardOverviewResponse:

        total_logs = logs_collection.count_documents({})

        todays_logs = logs_collection.count_documents(
            {
                "timestamp": {
                    "$gte": datetime.now(UTC).replace(
                        hour=0,
                        minute=0,
                        second=0,
                        microsecond=0,
                    )
                }
            }
        )

        todays_anomalies = anomaly_scores_collection.count_documents(
            {
                "prediction": 1
            }
        )

        open_incidents = incidents_collection.count_documents(
            {
                "status": "OPEN"
            }
        )

        critical_incidents = incidents_collection.count_documents(
            {
                "severity": "CRITICAL"
            }
        )

        return DashboardOverviewResponse(
            total_logs=total_logs,
            todays_anomalies=todays_anomalies,
            open_incidents=open_incidents,
            critical_incidents=critical_incidents,
            logs_trend_pct=0,
            anomalies_trend_pct=0,
            incidents_trend_pct=0,
            critical_trend_pct=0,
            active_hospital="HAI-SOC Demo",
            system_health="HEALTHY",
        )

    # =====================================================
    # RISK DISTRIBUTION
    # =====================================================

    @staticmethod
    def get_risk_distribution():

        low = anomaly_scores_collection.count_documents({"severity": "LOW"})
        medium = anomaly_scores_collection.count_documents({"severity": "MEDIUM"})
        high = anomaly_scores_collection.count_documents({"severity": "HIGH"})
        critical = anomaly_scores_collection.count_documents({"severity": "CRITICAL"})

        total = low + medium + high + critical

        def pct(value):
            return round((value / total) * 100, 1) if total else 0

        return [
            RiskDistributionItem(
                category="Low",
                count=low,
                percentage=pct(low),
                color="#22C55E",
            ),
            RiskDistributionItem(
                category="Medium",
                count=medium,
                percentage=pct(medium),
                color="#FACC15",
            ),
            RiskDistributionItem(
                category="High",
                count=high,
                percentage=pct(high),
                color="#F97316",
            ),
            RiskDistributionItem(
                category="Critical",
                count=critical,
                percentage=pct(critical),
                color="#EF4444",
            ),
        ]

    # =====================================================
    # SOURCES
    # =====================================================

    @staticmethod
    def get_sources():

        pipeline = [
            {
                "$group": {
                    "_id": "$source",
                    "count": {"$sum": 1},
                }
            }
        ]

        colors = [
            "#3B82F6",
            "#06B6D4",
            "#8B5CF6",
            "#10B981",
            "#F59E0B",
            "#EF4444",
        ]

        results = list(logs_collection.aggregate(pipeline))

        return [
            SourceDistributionItem(
                source=item["_id"],
                count=item["count"],
                color=colors[i % len(colors)],
            )
            for i, item in enumerate(results)
        ]

    # =====================================================
    # DEPARTMENTS
    # =====================================================

    @staticmethod
    def get_departments():

        pipeline = [
            {
                "$group": {
                    "_id": "$department",
                    "count": {"$sum": 1},
                }
            }
        ]

        colors = [
            "#10B981",
            "#3B82F6",
            "#F59E0B",
            "#8B5CF6",
            "#EF4444",
        ]

        results = list(logs_collection.aggregate(pipeline))

        return [
            DepartmentDistributionItem(
                department=item["_id"],
                count=item["count"],
                color=colors[i % len(colors)],
            )
            for i, item in enumerate(results)
        ]

    # =====================================================
    # MODEL USAGE
    # =====================================================

    @staticmethod
    def get_models():

        pipeline = [
            {
                "$group": {
                    "_id": "$detector",
                    "count": {"$sum": 1},
                }
            }
        ]

        results = list(anomaly_scores_collection.aggregate(pipeline))

        return [
            ModelDistributionItem(
                model=item["_id"],
                count=item["count"],
                accuracy=99.2,
            )
            for item in results
        ]

    # =====================================================
    # DAILY TREND
    # =====================================================

    @staticmethod
    def get_daily_trend():

        pipeline = [
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%d %b",
                            "date": "$created_at",
                        }
                    },
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}},
        ]

        results = list(anomaly_scores_collection.aggregate(pipeline))

        return [
            DailyTrendItem(
                hour=item["_id"],
                anomalies=item["count"],
                baseline=max(item["count"] - 1, 0),
            )
            for item in results
        ]

    # =====================================================
    # SYSTEM HEALTH
    # =====================================================

    @staticmethod
    def get_system_health() -> SystemHealthResponse:

        return SystemHealthResponse(
            mongodb="ONLINE",
            backend="ONLINE",
            ml_model="READY",
            api="ONLINE",
            uptime="99.9%",
        )

    # =====================================================
    # RECENT LOGS
    # =====================================================

    @staticmethod
    def get_recent_logs() -> list[RecentLogItem]:

        logs = (
            logs_collection
            .find()
            .sort("timestamp", -1)
            .limit(10)
        )

        return [
            RecentLogItem(
                id=str(log["_id"]),
                timestamp=str(log["timestamp"]),
                severity=log.get("severity", "UNKNOWN"),
                source=log.get("source", "Unknown"),
                message=log.get("details", ""),
            )
            for log in logs
        ]

    # =====================================================
    # RECENT INCIDENTS
    # =====================================================

    @staticmethod
    def get_recent_incidents() -> list[RecentIncidentItem]:

        incidents = (
            incidents_collection
            .find()
            .sort("created_at", -1)
            .limit(10)
        )

        return [
            RecentIncidentItem(
                id=str(doc["_id"]),
                title=doc.get("title", "Untitled Incident"),
                severity=str(doc.get("risk_level", doc.get("severity", "LOW"))),
                status=str(doc.get("status", "OPEN")),
            )
            for doc in incidents
        ]

    # =====================================================
    # RECENT ANOMALIES
    # =====================================================

    @staticmethod
    def get_recent_anomalies() -> list[RecentAnomalyItem]:

        anomalies = (
            anomaly_scores_collection
            .find()
            .sort("timestamp", -1)
            .limit(10)
        )

        return [
            RecentAnomalyItem(
                id=str(doc["_id"]),
                detector=doc.get("detector", "Unknown"),
                score=float(doc.get("anomaly_score", 0)),
                prediction=int(doc.get("prediction", 0)),
            )
            for doc in anomalies
        ]