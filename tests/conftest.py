import psycopg
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm import Session

from alembic import command
from app.config.app_settings import settings
from app.config.database import get_db
from app.entities.post_entity import Post
from app.entities.user_entity import User
from app.main import app
from app.schemas.token_schema import TokenData
from app.schemas.user_schema import CreateUserRequestDto, UserDto
from app.utils.jwt import create_access_token

from .db_test_connection import TestingSessionLocal, alembic_config

create_user_payload = CreateUserRequestDto(
    email= "sai23@gmail.com",
            password= "test123",
            phone= "+447824603561",
            first_name= "Saikrishna",
            last_name= "Sangishetty"
)

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
        
@fixture()
def test_db_session():
    if settings.ENV == "dev":
        # this is called in only in dev mode as dev mode configured to use two databases one is for the application and the other is for testing
        check_and_create_dev_env_test_db()
    
    # code that runs before the test function    
    command.upgrade(alembic_config,'head')
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
    # code that runs after the test function / cleanup code
    command.downgrade(alembic_config,'base')

@fixture()
def test_client(test_db_session):
    def override_get_db():
        try:
            yield test_db_session
        finally:
            test_db_session.close()
    # Override the get_db dependency to use the TestingSessionLocal
    app.dependency_overrides[get_db] = override_get_db
    # returns the client to the test function and db session
    yield TestClient(app) 
    
@fixture
def test_user(request, test_client, test_db_session:Session):
    """Fixture to create a test user with an optional custom payload."""
    user_payload = request.param if hasattr(request, "param") else create_user_payload
    response = test_client.post(
        "/users",
        json=user_payload.model_dump()
    )
    data = UserDto.model_validate(response.json())
    yield data, response.status_code
    
    # Cleanup: Delete the test user after the test completes
    test_db_session.query(User).filter(User.email == user_payload.email).delete()
    test_db_session.commit()

@fixture
def token(test_user):
    user = test_user[0]
    token_data = TokenData(email=user.email, id=user.id)
    return create_access_token(token_data)

@fixture
def authorized_client(test_client, token):
    test_client.headers = {
        **test_client.headers,
        "Authorization": f"Bearer {token}"
    }
    return test_client

def posts_data(userId:int):
    return [
        Post(user_id=userId, title="Post 1", content="Content 1", published=True),
        Post(user_id=userId, title="Post 2", content="Content 2", published=True),
        Post(user_id=userId, title="Post 3", content="Content 3", published=False),
    ]

@fixture
def test_posts(test_db_session, test_user):
    user = test_user[0]
    test_db_session.add_all(posts_data(user.id))
    
    test_db_session.commit()
    
    yield test_db_session.query(Post).all()