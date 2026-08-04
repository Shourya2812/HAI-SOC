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
    RiskDistributionResponse,
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
    def get_risk_distribution() -> RiskDistributionResponse:

        pipeline = [
            {
                "$group": {
                    "_id": "$severity",
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]

        result = list(logs_collection.aggregate(pipeline))

        counts = {
            "LOW": 0,
            "MEDIUM": 0,
            "HIGH": 0,
            "CRITICAL": 0,
        }

        for item in result:

            severity = item["_id"]

            if severity in counts:
                counts[severity] = item["count"]

        return RiskDistributionResponse(
            low=counts["LOW"],
            medium=counts["MEDIUM"],
            high=counts["HIGH"],
            critical=counts["CRITICAL"],
        )

    # =====================================================
    # SOURCES
    # =====================================================

    @staticmethod
    def get_sources() -> list[SourceDistributionItem]:

        pipeline = [
            {
                "$group": {
                    "_id": "$source",
                    "count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            }
        ]

        result = logs_collection.aggregate(pipeline)

        return [
            SourceDistributionItem(
                source=item["_id"] or "Unknown",
                count=item["count"],
            )
            for item in result
        ]

    # =====================================================
    # DEPARTMENTS
    # =====================================================

    @staticmethod
    def get_departments() -> list[DepartmentDistributionItem]:

        pipeline = [
            {
                "$group": {
                    "_id": "$department",
                    "count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            }
        ]

        result = logs_collection.aggregate(pipeline)

        return [
            DepartmentDistributionItem(
                department=item["_id"] or "Unknown",
                count=item["count"],
            )
            for item in result
        ]

    # =====================================================
    # MODEL USAGE
    # =====================================================

    @staticmethod
    def get_models() -> list[ModelDistributionItem]:

        pipeline = [
            {
                "$group": {
                    "_id": "$detector",
                    "count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            }
        ]

        result = anomaly_scores_collection.aggregate(pipeline)

        return [
            ModelDistributionItem(
                detector=item["_id"] or "Unknown",
                count=item["count"],
            )
            for item in result
        ]

    # =====================================================
    # DAILY TREND
    # =====================================================

    @staticmethod
    def get_daily_trend() -> list[DailyTrendItem]:
        """
        Return anomaly trend grouped by day.
        """

        pipeline = [
            {
                "$match": {
                    "created_at": {
                        "$exists": True,
                        "$ne": None,
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$created_at",
                        }
                    },
                    "count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "_id": 1
                }
            }
        ]

        result = anomaly_scores_collection.aggregate(pipeline)

        return [
            DailyTrendItem(
                date=str(item["_id"]),
                count=item["count"],
            )
            for item in result
            if item["_id"] is not None
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
                message=log.get("message", ""),
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
                severity=doc.get("severity", "LOW"),
                status=doc.get("status", "OPEN"),
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