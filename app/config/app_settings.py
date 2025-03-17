import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    POSTGRES_USER: str 
    POSTGRES_HOST: str 
    POSTGRES_PORT: str 
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str
    POSTGRES_DB_TEST: str = 'test_db'
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_SECRET_KEY_EXPIRE_MINUTES: str
    ENV: str
    
    def get_db_name(self) -> str:
        """Return the database name based on the environment."""
        if os.getenv("ENV", "production") == "dev":
            # If ENV is dev, use the test database
            return self.POSTGRES_DB_TEST
        # Else use the database set in environment variables
        return self.POSTGRES_DB

settings = Settings()