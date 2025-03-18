import os
from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from alembic import config
from app.config.app_settings import settings
from app.config.database import get_db
from app.main import app

encoded_password = quote(settings.POSTGRES_PASSWORD) # URL encode the password to handle special characters in the password ex: @, #, $, etc.

TEST_SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.POSTGRES_USER}:{encoded_password}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.get_db_name()}"

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

alembic_config = config.Config(os.path.join(os.path.dirname(__file__), '../alembic.ini'))

    
    


