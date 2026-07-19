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


@pytest.mark.asyncio
async def test_account_id_match(client, authenticated_user):
    headers = authenticated_user["headers"]

    created_response = await client.post(
        "/accounts",
        json={
            "owner_name": "test_user",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=headers
    )

    assert created_response.status_code == 200

    created_account = created_response.json()
    account_id = created_account["id"]

    # Fetch account by ID
    response = await client.get(
        f"/accounts/{account_id}",
        headers=headers
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == account_id
    assert body["owner_name"] == "test_user"
    assert body["balance"] == 1000.0
    assert body["account_type"] == "checking"
    assert body["id"] == authenticated_user["user_id"]


@pytest.mark.asyncio
async def test_invalid_account_id(client, authenticated_user):
    headers = authenticated_user["headers"]

    response = await client.get(
        "/accounts/99999",
        headers=headers
    )

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_account_owner_name(client, authenticated_user):
    headers = authenticated_user["headers"]

    created_response = await client.post(
        "/accounts",
        json={
            "owner_name": "test_user",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=headers
    )

    assert created_response.status_code == 200
    account_id = created_response.json()["id"]

    response = await client.put(
        f"/accounts/{account_id}",
        json={
            "owner_name": "new_user"
        },
        headers=headers
    )

    assert response.status_code == 200

    owner_name = response.json()["owner_name"]

    assert owner_name == "new_user"


@pytest.mark.asyncio
async def test_update_account_type(client, authenticated_user):
    headers = authenticated_user["headers"]

    created_response = await client.post(
        "/accounts",
        json={
            "owner_name": "test_user",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=headers
    )

    assert created_response.status_code == 200
    account_id = created_response.json()["id"]

    response = await client.put(
        f"/accounts/{account_id}",
        json={
            "account_type": "savings"
        },
        headers=headers
    )

    assert response.status_code == 200

    account_type = response.json()["account_type"]

    assert account_type == "savings"


@pytest.mark.asyncio
async def test_update_account_balance(client, authenticated_user):
    headers = authenticated_user["headers"]

    #create account
    created_response = await client.post(
        "/accounts",
        json={
            "owner_name": "test_user",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=headers
    )

    assert created_response.status_code == 200

    account_id = created_response.json()["id"]

    response = await client.put(
        f"/accounts/{account_id}",
        json={
            "balance": 100000.0,
        },
        headers=headers
    )

    assert response.status_code == 200

    new_balance = response.json()["balance"]

    assert new_balance == 100000.0


@pytest.mark.asyncio
async def test_update_account_frozen(client, authenticated_user):
    headers = authenticated_user["headers"]

    created_response = await client.post(
        "/accounts",
        json={
            "owner_name": "test_user",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=headers
    )

    assert created_response.status_code == 200
    account_id = created_response.json()["id"]

    response = await client.put(
        f"/accounts/{account_id}",
        json={
            "frozen": True
        },
        headers=headers
    )

    assert response.status_code == 200

    isfrozen = response.json()["frozen"]

    assert isfrozen == True


@pytest.mark.asyncio
async def test_delete_account(client, authenticated_user):
    headers = authenticated_user["headers"]

    #create account
    created_response = await client.post(
        "/accounts",
        json={
            "owner_name": "test_user",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=headers
    )

    assert created_response.status_code == 200

    account_id = created_response.json()["id"]

    #delete account
    delete_response = await client.delete(
        f"/accounts/{account_id}",
        headers=headers
    )

    assert delete_response.status_code == 200

    #fetch for the deleted account
    response = await client.get(
        f"/accounts/{account_id}",
        headers=headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_set_frozen_not_frozen(client, authenticated_user):
    headers = authenticated_user["headers"]

    created_response = await client.post(
        "/accounts",
        json={
            "owner_name": "test_user",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=headers
    )

    assert created_response.status_code == 200

    account_id = created_response.json()["id"]

    response = await client.patch(
        f"/accounts/{account_id}/set_freeze",
        json={
            "freeze": True
        },
        headers=headers
    )

    assert response.status_code == 200
    body = response.json()

    assert body["id"] == account_id
    assert body["frozen"] == True


@pytest.mark.asyncio
async def test_set_frozen_unfreeze(client, authenticated_user):
    headers = authenticated_user["headers"]

    created_response = await client.post(
        "/accounts",
        json={
            "owner_name": "test_user",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=headers
    )

    assert created_response.status_code == 200

    account_id = created_response.json()["id"]

    await client.patch(
        f"/accounts/{account_id}/set_freeze",
        json={
            "freeze": True
        },
        headers=headers
    )

    response = await client.patch(
        f"/accounts/{account_id}/set_freeze",
        json={
            "freeze": False
        },
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["frozen"] == False


@pytest.mark.asyncio
async def test_set_frozen_already_frozen_or_unfrozen(client, authenticated_user):
    headers = authenticated_user["headers"]

    created_response = await client.post(
        "/accounts",
        json={
            "owner_name": "test_user",
            "balance": 1000.0,
            "account_type": "checking"
        },
        headers=headers
    )

    assert created_response.status_code == 200

    account_id = created_response.json()["id"]

    response = await client.patch(
        f"/accounts/{account_id}/set_freeze",
        json={
            "freeze": False
        },
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "No State Change Needed"

