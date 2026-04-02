from pydantic_settings import BaseSettings
from pydantic import ConfigDict


# Create a Settings class that inherits from BaseSettings
class Settings(BaseSettings):

    # Database connection URL
    DATABASE_URL: str = "postgresql+psycopg2://postgres:root@localhost:5432/MarketMentor_AI_DB"

    # Secret key used for security purposes
    SECRET_KEY: str = "your_super_secret_key_here"

    # Algorithm used for JWT token encoding/decoding
    ALGORITHM: str = "HS256"


    # Pydantic configuration settings
    model_config = ConfigDict(
        # Load environment variables from .env file
        env_file=".env",

        # Ignore extra environment variables that are not defined in this class
        extra="ignore"
    )


# Create a settings object
settings = Settings()