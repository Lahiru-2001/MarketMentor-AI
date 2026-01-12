from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:root@localhost:5432/MarketMentor_AI_DB"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
