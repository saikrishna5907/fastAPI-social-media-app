from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str 
    POSTGRES_HOST: str 
    POSTGRES_PORT: str 
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_SECRET_KEY_EXPIRE_MINUTES: str


settings = Settings()
