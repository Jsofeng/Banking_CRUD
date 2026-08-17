import pytest


@pytest.mark.asyncio
async def test_get_transactions(client, authenticated_user):
    headers = authenticated_user["headers"]

    created_response = await client.post(
        "/accounts",
        json={"owner_name": "test_user", "balance": 1000.0, "account_type": "chequing"},
        headers=headers,
    )

    assert created_response.status_code == 200

    account_id = created_response.json()["id"]

    transaction1_headers = {
        **headers,
        "Idempotency-Key": "test-deposit-001",
    }

    transaction1 = await client.patch(
        f"/accounts/{account_id}/transaction",
        json={"amount": 1000.0, "transaction_type": "deposit"},
        headers=transaction1_headers,
    )

    assert transaction1.status_code == 200

    transaction2_headers = {
        **headers,
        "Idempotency-Key": "test-deposit-002",
    }

    transaction2 = await client.patch(
        f"/accounts/{account_id}/transaction",
        json={"amount": 100.0, "transaction_type": "withdrawal"},
        headers=transaction2_headers,
    )

    assert transaction2.status_code == 200

    response = await client.get(f"/accounts/{account_id}/transaction", headers=headers)

    transactions = response.json()

    assert len(transactions) == 2
    assert transactions[0]["amount"] == 1000.0
    assert transactions[0]["transaction_type"] == "deposit"
    assert transactions[0]["account_id"] == account_id
    assert transactions[0]["balance_before"] == 1000.0
    assert transactions[0]["balance_after"] == 2000.0

    assert transactions[1]["amount"] == 100.0
    assert transactions[1]["transaction_type"] == "withdrawal"
    assert transactions[1]["account_id"] == account_id
    assert transactions[1]["balance_before"] == 2000.0
    assert transactions[1]["balance_after"] == 1900.0


@pytest.mark.asyncio
async def test_transactions_with_frozen_account(client, authenticated_user):
    headers = authenticated_user["headers"]

    created_response = await client.post(
        "/accounts",
        json={"owner_name": "test_user", "balance": 1000.0, "account_type": "checking"},
        headers=headers,
    )

    assert created_response.status_code == 200

    account_id = created_response.json()["id"]

    frozen = await client.patch(
        f"/accounts/{account_id}/set_freeze", json={"freeze": True}, headers=headers
    )

    assert frozen.status_code == 200
    assert frozen.json()["frozen"] is True

    transaction_header = {**headers, "Idempotency-Key": "test-deposit-001"}

    transaction = await client.patch(
        f"/accounts/{account_id}/transaction",
        json={"amount": 1000.0, "transaction_type": "deposit"},
        headers=transaction_header,
    )

    assert transaction.status_code == 400
    assert transaction.json()["detail"] == "Account is currently frozen"
