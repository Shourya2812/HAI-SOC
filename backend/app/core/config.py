from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ==========================================================
    # Application
    # ==========================================================
    APP_NAME: str = "HAI-SOC"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Healthcare AI Security Operations Center"

    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    API_V1_PREFIX: str = "/api/v1"

    # ==========================================================
    # MongoDB
    # ==========================================================
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "hai_soc"

    # ==========================================================
    # Authentication
    # ==========================================================
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ==========================================================
    # LLM
    # ==========================================================
    LLM_PROVIDER: str = "gemini"

    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # ==========================================================
    # Redis
    # ==========================================================
    REDIS_URL: str = "redis://localhost:6379"

    # ==========================================================
    # Qdrant
    # ==========================================================
    QDRANT_URL: str = "http://localhost:6333"

    # ==========================================================
    # Logging
    # ==========================================================
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()