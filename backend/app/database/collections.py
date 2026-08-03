"""
Centralized MongoDB collection references used throughout HAI-SOC.
"""

from backend.app.database.connection import MongoDB

db = MongoDB.get_database()

# Collections
users_collection = db["users"]

logs_collection = db["logs"]

incidents_collection = db["incidents"]

anomaly_scores_collection = db["anomaly_scores"]