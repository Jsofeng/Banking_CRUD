import pytest

@pytest.mark.asyncio
async def test_create_account(client, authenticated_user):
    response = await client.post(
        "/accounts",
        json={
            "owner_name": "Joe",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=authenticated_user["headers"]
    )

    assert response.status_code == 200

    body = response.json()

    assert body["owner_name"] == "Joe"
    assert body["account_type"] == "checking"
    assert body["balance"] == 1000.0

    assert body["id"] == authenticated_user["user_id"]


@pytest.mark.asyncio
async def test_create_account_without_token(client):
    response = await client.post(
        "/accounts",
        json={
            "owner_name": "Joe",
            "balance": 1000.0,
            "account_type": "checking"
        }
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_accounts(client, authenticated_user):
    headers = authenticated_user["headers"]
    
    await client.post(
        "/accounts",
        json={
            "owner_name": "user2",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=headers
    )

    await client.post(
        "/accounts",
        json={
            "owner_name": "user2",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=headers
    )

    response = await client.get(
        "/accounts",
        headers=headers
    )

    assert response.status_code == 200
    
    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 2

@pytest.mark.asyncio
async def test_account_ownership_privacy(client):

    #register user 1
    await client.post(
        "/register",
        json={
            "username": "user1",
            "email": "test1@example.com",
            "password": "password123"
        }
    )

    #login user 1
    login1 = await client.post(
        "/login",
        data={
            "username": "user1",
            "password": "password123"
        }
    )

    headers1 = {
        "Authorization": f"Bearer {login1.json()['access_token']}"
    }
    
    #register user 2
    await client.post(
        "/register",
        json={
            "username": "user2",
            "email": "test2@example.com",
            "password": "password123"
        }
    )

    #login as user 2
    login2 = await client.post(
        "/login",
        data={
            "username": "user2",
            "password": "password123"
        }
    )

    #User 2 auth token
    headers2 = {
        "Authorization": f"Bearer {login2.json()['access_token']}"
    }

    #User 1 creates account
    await client.post(
       "/accounts",
        json={
            "owner_name": "User One",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=headers1
    )

    response = await client.get(
        "/accounts",
        headers=headers2
    )

    assert response.status_code == 200
    
    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 0
