from decimal import Decimal
from uuid import uuid4
from models import Account, Transfer
from datetime import datetime
from services import transfer
import pytest


def test_services_transfer(db, create_account, create_user):
    from_account = create_account

    to_account = Account(
        id=uuid4(),
        owner_name="test_user_2",
        account_type="chequing",
        balance=Decimal("100.00"),
        created_at=datetime.utcnow(),
        frozen=False,
        owner_id=create_user.id,
    )

    db.add(to_account)
    db.commit()
    db.refresh(to_account)

    e_transfer = transfer(
        db=db,
        from_account=from_account.id,
        to_account=to_account.id,
        amount=Decimal("100.00"),
        idempotency_key="test_transfer_001",
    )

    assert len(e_transfer) == 2

    sent_transaction = e_transfer[0]
    received_transaction = e_transfer[1]

    assert sent_transaction.transaction_type == "transfer"
    assert sent_transaction.amount == Decimal("100.00")
    assert sent_transaction.balance_before == Decimal("100.00")
    assert sent_transaction.balance_after == Decimal("0.00")
    assert sent_transaction.status == "completed"

    assert received_transaction.transaction_type == "transfer"
    assert received_transaction.amount == Decimal("100.00")
    assert received_transaction.balance_before == Decimal("100.00")
    assert received_transaction.balance_after == Decimal("200.00")
    assert received_transaction.status == "completed"

    assert sent_transaction.transfer_id == received_transaction.transfer_id

    transfer_record = (
        db.query(Transfer).filter(Transfer.id == sent_transaction.transfer_id).first()
    )

    assert transfer_record is not None
    assert transfer_record.idempotency_key == "test_transfer_001"
    assert transfer_record.from_account_id == from_account.id
    assert transfer_record.to_account_id == to_account.id
    assert transfer_record.amount == Decimal("100.00")
    assert transfer_record.status == "completed"

    assert to_account.balance == Decimal("200.00")
    assert from_account.balance == Decimal("0.00")
