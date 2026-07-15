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
async def test_create_account_with_no_auth_headers(client):
    response = await client.post(
        "/accounts",
        json={
            "owner_name": "Joe",
            "balance": 1000.0,
            "account_type": "checking"
        }
    )

    assert response.status_code == 401

