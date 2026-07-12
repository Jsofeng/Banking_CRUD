# A fixture is just a function decorated with @pytest.fixture. pytest automatically calls it before each test that requests it. 
import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base

#test databse
TEST_DATABASE_URL = "postgresql://postgres:password@db:5432/bank_app_test"

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture(scope="function") #This fixture runs before every test.
def db():
    # Create fresh tables before each test
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def override_get_db(): #for endpoints in main they call bank_app's database but for testing we want to call bank_app_test's database
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

# Tell FastAPI to use the test database
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
async def client(): #This gives every test its own fake browser.
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

