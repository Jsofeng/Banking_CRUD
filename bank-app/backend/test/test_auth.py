import pytest
from auth import hash_password, verify_password, create_access_token, verify_token

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

    assert result == True


def test_verify_wrong_password():
    password = "my_secret_password"

    hashed_password = hash_password(password)

    result = verify_password("wrong_password", hashed_password)

    assert result == False


def test_create_access_token():

    token = create_access_token({"sub": "testuser"})

    assert isinstance(token, str)
    assert token != ""


def test_verify_token():
    username = "testuser"
    token = create_access_token({"sub": username})

    decode = verify_token(token)

    assert decode == username

def test_verify_invalid_token():
    with pytest.raises(Exception): #verify_token returns an Exception if the token is invalid so this basically says (“pytest, pay attention. I expect an Exception to happen next.” returns true if it got what it expected)
        verify_token("this_is_not_a_real_token")


@pytest.mark.asyncio
async def test_register(client):

    response = await client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    data = response.json()
    assert response.status_code in [200, 201]
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data

