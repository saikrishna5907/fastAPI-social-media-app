import os
from urllib.parse import quote

import psycopg
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from alembic import command, config
from app.config.app_settings import settings
from app.config.database import get_db
from app.main import app

encoded_password = quote(settings.POSTGRES_PASSWORD) # URL encode the password to handle special characters in the password ex: @, #, $, etc.

TEST_SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.POSTGRES_USER}:{encoded_password}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.get_db_name()}"

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

alembic_config = config.Config(os.path.join(os.path.dirname(__file__), '../alembic.ini'))

# Check if the test DB exists
def check_and_create_dev_env_test_db():
    conn = psycopg.connect(
        dbname='postgres',  # Connect to the default database to check
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    try:
        # Use double quotes around the database name if it contains special characters like '-'
        db_name = f'"{settings.get_db_name()}"'
        
        # Check if the database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
        exists = cursor.fetchone()
        if not exists:
            print(f"Database {db_name} does not exist. Creating it.")
            cursor.execute(f"CREATE DATABASE {db_name};")
            print(f"Database {db_name} created.")
    except Exception as e:
        print(f"An error occurred while checking or creating the database: {e}")
    finally:
        cursor.close()
        conn.close()

@fixture(scope="module")
def test_client():
    if settings.ENV == "dev":
        # this is called in only in dev mode as dev mode configured to use two databases one is for the application and the other is for testing
        check_and_create_dev_env_test_db()

    command.upgrade(alembic_config,'head')

    yield TestClient(app) # returns the client to the test function
    
    # code that runs after the test function / cleanup code
    command.downgrade(alembic_config,'base')

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the get_db dependency to use the TestingSessionLocal
app.dependency_overrides[get_db] = override_get_db