"""
backend/app/database/connection.py

Creates and manages the MongoDB connection used across HAI-SOC.
"""

from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import settings


class MongoDB:
    """
    Singleton-style MongoDB connection manager.
    """

    client: MongoClient | None = None
    database: Database | None = None

    @classmethod
    def connect(cls):
        """
        Establish connection to MongoDB.
        """

        if cls.client is None:
            cls.client = MongoClient(settings.MONGO_URI)

            # Verify connection
            cls.client.admin.command("ping")

            cls.database = cls.client[settings.MONGO_DB_NAME]

            print("✅ Connected to MongoDB")

    @classmethod
    def get_database(cls) -> Database:
        """
        Return database instance.
        """

        if cls.database is None:
            cls.connect()

        return cls.database

    @classmethod
    def close(cls):
        """
        Close MongoDB connection.
        """

        if cls.client:
            cls.client.close()

            print("🔴 MongoDB connection closed")