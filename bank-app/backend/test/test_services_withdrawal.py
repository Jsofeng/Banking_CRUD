from decimal import Decimal
from uuid import uuid4
from services import withdrawal
import pytest


def test_services_withdrawal(db, create_account):
    account = create_account

    transaction = withdrawal(
        db=db,
        account_id=account.id,
        amount=Decimal("100.00"),
        idempotency_key="test-withdrawal-001",
    )

    assert transaction.amount == Decimal("100.00")
    assert transaction.transaction_type == "withdrawal"
    assert transaction.balance_before == Decimal("100.00")
    assert transaction.balance_after == Decimal("0.00")
    assert transaction.status == "completed"
    assert transaction.idempotency_key == "test-withdrawal-001"

    db.refresh(account)
    assert account.balance == Decimal("0.00")


def test_services_withdrawal_insufficient_amount(db, create_account):
    account = create_account
    with pytest.raises(ValueError, match="Insufficient funds"):
        withdrawal(
            db=db,
            account_id=account.id,
            amount=Decimal("101.00"),
            idempotency_key="test-withdrawal-001",
        )
