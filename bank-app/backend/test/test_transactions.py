import pytest

@pytest.mark.asyncio
async def test_get_transactions(client, authenticated_user):
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

    transaction = await client.patch(
        f"/accounts/{account_id}/transaction",
        json={
            "amount": 1000.0,
            "transaction_type": "deposit"
        },
        headers=headers
    )

    assert transaction.status_code == 200

    response = await client.get(
        f"/accounts/{account_id}/transaction",
        headers=headers
    )

    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["amount"] == 1000.0
    assert transactions[0]["transaction_type"] == "deposit"
    assert transactions[0]["account_id"] == account_id


@pytest.mark.asyncio
async def test_transactions_with_frozen_account(client, authenticated_user):
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

    frozen = await client.patch(
        f"/accounts/{account_id}/set_freeze",
        json={
            "freeze": True
        },
        headers=headers
    )

    assert frozen.status_code == 200
    assert frozen.json()["frozen"] == True

    transaction = await client.patch(
        f"/accounts/{account_id}/transaction",
        json={
            "amount": 1000.0,
            "transaction_type": "deposit"
        },
        headers=headers
    )

    assert transaction.status_code == 400
    assert transaction.json()["detail"] == "Account is currently frozen"