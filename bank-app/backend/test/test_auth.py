import pytest
from jose import jwt

from auth import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    hash_password,
    verify_password,
    verify_token,
)


def test_hash_password():
    password = "my_password123"

    hashed = hash_password(password)

    # The password should be hashed, Checks that the password was actually transformed if not assert would fail.
    assert hashed != password

    # Makes sure the function's return type is a str
    assert isinstance(hashed, str)


def test_verify_password():
    password = "my_secret_password"

    hashed_password = hash_password(password)

    result = verify_password(password, hashed_password)

    assert result is True


def test_verify_wrong_password():
    password = "my_secret_password"

    hashed_password = hash_password(password)

    result = verify_password("wrong_password", hashed_password)

    assert result is False


def test_create_access_token():

    token = create_access_token({"sub": "testuser"})

    assert isinstance(token, str)
    assert token != ""


def test_verify_token():
    username = "testuser"
    token = create_access_token({"sub": username})

    decode = verify_token(token)

    assert decode == username


"""
Tracing through your actual function: jwt.decode(...) will fail to parse "this_is_not_a_real_token" as a valid JWT,
which raises a JWTError internally. Your except JWTError: block catches that and re-raises
a plain Exception("Invalid or expired token"). Since pytest.raises(Exception) is watching for exactly that, the test passes.
"""


def test_verify_invalid_token():
    with pytest.raises(
        Exception
    ):  # verify_token returns an Exception if the token is invalid so this basically says (“pytest, pay attention. I expect an Exception to happen next.” returns true if it got what it expected)
        verify_token("this_is_not_a_real_token")


@pytest.mark.asyncio
async def test_verify_token_invalid_user(client):
    token = create_access_token({"sub": "ghost_user"})  # token is successfully created

    # "ghost_user" was never registered"
    response = await client.get(
        "/accounts", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token or user not found"


@pytest.mark.asyncio
async def test_verify_token_missing_username():
    # create a token
    token = jwt.encode({}, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(Exception):
        verify_token(token)


@pytest.mark.asyncio
async def test_register(client):

    response = await client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    data = response.json()
    assert response.status_code in [200, 201]
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_duplicate_register(client):

    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
    }

    # First registration should succeed
    response = await client.post("/register", json=user_data)

    assert response.status_code == 200

    # Second registration with same username should fail
    response = await client.post("/register", json=user_data)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_duplicate_email_register(client):

    user_data1 = {
        "username": "testuser1",
        "email": "test@example.com",
        "password": "password123",
    }

    user_data2 = {
        "username": "testuser2",
        "email": "test@example.com",
        "password": "password1234",
    }

    # First registration should succeed
    response = await client.post("/register", json=user_data1)

    assert response.status_code == 200

    # Second registration with same email should fail
    response = await client.post("/register", json=user_data2)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"


@pytest.mark.asyncio
async def test_login(client):
    # Register a user first
    await client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    # Login with the same credentials
    response = await client.post(
        "/login", data={"username": "testuser", "password": "password123"}
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client):

    await client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    response = await client.post(
        "/login", data={"username": "testuser", "password": "wrongpassword"}
    )

    assert response.status_code == 401
