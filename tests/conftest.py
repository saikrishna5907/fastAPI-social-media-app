import psycopg
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm import Session

from alembic import command
from app.config.app_settings import settings
from app.config.database import get_db
from app.entities.post_entity import Post
from app.entities.user_entity import User
from app.entities.vote_entity import Vote
from app.main import app
from app.schemas.token_schema import TokenData
from app.schemas.user_schema import CreateUserRequestDto, UserDto
from app.schemas.vote_schema import VoteDTO
from app.utils.jwt import create_access_token, get_current_token_payload

from .db_test_connection import TestingSessionLocal, alembic_config


class TestUsersResponse:
    def __init__(self, user: UserDto, status_code: int):
        self.user = user
        self.status_code = status_code

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
    
@fixture()
def test_users(request, test_client, test_db_session:Session):
    """Fixture to create one or more test users dynamically."""
    
    # Default user payloads if request.param is not provided
    default_payloads = [create_user_payload]
    
    # Use request.param if provided, otherwise use the default payload
    user_payloads = request.param if hasattr(request, "param") else default_payloads
    
    created_users: list[TestUsersResponse]= []

    for user_payload in user_payloads:
        response = test_client.post("/users", json=user_payload.model_dump())
        user_data = UserDto.model_validate(response.json())
        created_users.append(TestUsersResponse(user=user_data, status_code=response.status_code))

    yield created_users  # Returns a list of created users

    # Cleanup: Delete all test users after the test completes
    for user_payload in user_payloads:
        test_db_session.query(User).filter(User.email == user_payload.email).delete()
    test_db_session.commit()

@fixture()
def token(test_users):
    user = test_users[0].user
    token_data = TokenData(email=user.email, id=user.id)
    return create_access_token(token_data)

@fixture()
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

@fixture()
def test_posts(test_db_session, test_users):
    posts_to_create: list[Post] = []
    for user in test_users:
        posts_to_create.extend(posts_data(user.user.id))
        
    test_db_session.add_all(posts_to_create)
    
    test_db_session.commit()
    
    yield test_db_session.query(Post).all()
    
def vote_payload(post_id:int, flag:int = 0):
    return VoteDTO(post_id=post_id,flag=flag)

@fixture()
def create_vote_own_post(request, authorized_client, test_posts, test_db_session, token):
    vote_value = request.param if hasattr(request, "param") else 0
    token_payload = get_current_token_payload(token)
    payload = vote_payload(test_posts[0].id, vote_value)
    response = authorized_client.post("/vote",json=payload.model_dump())
    
    yield response
    
    # cleanup
    test_db_session.query(Vote).filter(Vote.post_id == payload.post_id, Vote.user_id == token_payload.id).delete()
    test_db_session.commit()

@fixture()
def create_new_vote_on_another_user_post(request, authorized_client, test_users, test_posts, token, test_db_session):
    user2 = test_users[1].user
    # get post of user 2
    user2_posts = list(filter(lambda post: post.user_id == user2.id, test_posts))
    vote_value = request.param if hasattr(request, "param") else 0
    votePayload = vote_payload(user2_posts[0].id, vote_value)
    token_payload = get_current_token_payload(token)
    response = authorized_client.post("/vote",json=votePayload.model_dump())
    
    yield response
    
    # cleanup
    test_db_session.query(Vote).filter(Vote.post_id == votePayload.post_id, Vote.user_id == token_payload.id).delete()
    test_db_session.commit()
