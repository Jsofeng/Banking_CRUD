# A fixture is just a function decorated with @pytest.fixture. pytest automatically calls it before each test that requests it.
import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app, get_db
from models import User

load_dotenv()

# test databse
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql://postgres:password@localhost:5432/bank_app_test"
)

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")  # This fixture runs before every test.
def db():
    # Create fresh tables before each test
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def override_get_db():  # for endpoints in main they call bank_app's database but for testing we want to call bank_app_test's database
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# Tell FastAPI to use the test database
app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture
async def client(
    db,
):  # <-- depend on db fixture here #This creates a fake browser/Postman that talks directly to FastAPI.
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture  # allows pytest to automatically injects fixtures by name
async def authenticated_user(client: AsyncClient, db):
    await client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    user = db.query(User).filter(User.username == "testuser").first()

    login_response = await client.post(
        "/login", data={"username": "testuser", "password": "password123"}
    )

    token = login_response.json()["access_token"]

    return {"headers": {"Authorization": f"Bearer {token}"}, "user_id": user.id}
