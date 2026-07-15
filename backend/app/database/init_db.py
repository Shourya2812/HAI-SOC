"""
Initializes the MongoDB database for HAI-SOC by creating
collections and indexes.

"""

from pymongo import ASCENDING, DESCENDING

from app.database.connection import MongoDB


def init_collections(db):
    """
    Create MongoDB collections if they do not already exist.
    """

    collections = [
        "logs",
        "anomaly_scores",
        "incidents",
        "users",
        "audit_logs",
    ]

    existing = db.list_collection_names()

    for collection in collections:
        if collection not in existing:
            db.create_collection(collection)

    print(f"✅ Collections ready: {db.list_collection_names()}")


def init_indexes(db):
    """
    Create indexes for faster queries.
    """

    # ==========================================================
    # Logs
    # ==========================================================
    db.logs.create_index([("timestamp", DESCENDING)])
    db.logs.create_index([("user_id", ASCENDING)])
    db.logs.create_index([("severity", ASCENDING)])
    db.logs.create_index([("source", ASCENDING)])

    # ==========================================================
    # Anomaly Scores
    # ==========================================================
    db.anomaly_scores.create_index([("log_id", ASCENDING)])
    db.anomaly_scores.create_index([("severity", ASCENDING)])
    db.anomaly_scores.create_index([("scored_at", DESCENDING)])

    # ==========================================================
    # Incidents
    # ==========================================================
    db.incidents.create_index([("status", ASCENDING)])
    db.incidents.create_index([("risk_level", ASCENDING)])
    db.incidents.create_index([("created_at", DESCENDING)])
    db.incidents.create_index([("mitre_technique_id", ASCENDING)])

    # ==========================================================
    # Users
    # ==========================================================
    db.users.create_index(
        [("email", ASCENDING)],
        unique=True,
    )

    # ==========================================================
    # Audit Logs
    # ==========================================================
    db.audit_logs.create_index([("timestamp", DESCENDING)])
    db.audit_logs.create_index([("user_id", ASCENDING)])
    db.audit_logs.create_index([("action", ASCENDING)])

    print("✅ Indexes created successfully.")


def main():
    """
    Initialize MongoDB database.
    """

    try:
        MongoDB.connect()

        db = MongoDB.get_database()

        init_collections(db)
        init_indexes(db)

        print("🎉 HAI-SOC MongoDB initialized successfully.")

    except Exception as e:
        print(f"❌ Database initialization failed: {e}")

    finally:
        MongoDB.close()


if __name__ == "__main__":
    main()