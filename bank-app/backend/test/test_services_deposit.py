from decimal import Decimal
from uuid import uuid4
from datetime import datetime
import pytest

from models import Transaction
from services import deposit


def test_service_deposit(db, create_account):  # tests deposit() directly

    account = create_account

    transaction = deposit(
        db=db,
        account_id=account.id,
        amount=Decimal("50.00"),
        idempotency_key="deposit-test-001",
    )

    assert transaction.amount == Decimal("50.00")
    assert transaction.transaction_type == "deposit"
    assert transaction.balance_before == Decimal("100.00")
    assert transaction.balance_after == Decimal("150.00")
    assert transaction.status == "completed"
    assert transaction.idempotency_key == "deposit-test-001"

    db.refresh(account)

    assert account.balance == Decimal("150.00")


def test_service_deposit_account_not_found(db):
    fake_account_id = uuid4()

    with pytest.raises(ValueError, match="Account not found"):
        deposit(
            db=db,
            account_id=fake_account_id,
            amount=Decimal("100.00"),
            idempotency_key="test-deposit-account-not-found-001",
        )


def test_service_deposit_same_idempotency_key(db, create_account):
    account = create_account

    first_transaction = deposit(
        db=db,
        account_id=account.id,
        amount=Decimal("50.00"),
        idempotency_key="deposit-idempotency-001",
    )

    second_transaction = deposit(
        db=db,
        account_id=account.id,
        amount=Decimal("50.00"),
        idempotency_key="deposit-idempotency-001",
    )

    assert first_transaction.id == second_transaction.id

    assert account.balance == Decimal("150.00")

    transactions = (
        db.query(Transaction).filter(Transaction.account_id == account.id).all()
    )

    assert len(transactions) == 1
