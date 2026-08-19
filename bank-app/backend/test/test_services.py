from decimal import Decimal
from uuid import uuid4
from datetime import datetime

from models import Account, Transaction, User
from services import deposit


def test_service_deposit(db):  # tests deposit() directly
    user = User(
        id=uuid4(),
        username="testuser",
        email="test@example.com",
        hashed_password="password",
        role="user",
        created_at=datetime.utcnow(),
    )

    db.add(user)
    db.commit()

    account = Account(
        id=uuid4(),
        owner_name="test_user",
        account_type="checking",
        balance=Decimal("100.00"),
        owner_id=user.id,
    )

    db.add(account)
    db.commit()
    db.refresh(account)

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
