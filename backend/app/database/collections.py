"""
Centralized MongoDB collection references used throughout HAI-SOC.
"""

from app.database.connection import MongoDB

db = MongoDB.get_database()

# Collections
logs_collection = db["logs"]

anomaly_scores_collection = db["anomaly_scores"]

incidents_collection = db["incidents"]

users_collection = db["users"]

audit_logs_collection = db["audit_logs"]