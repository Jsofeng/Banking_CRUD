from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session
from models import Account, Transaction


def deposit(db: Session, account_id: UUID, amount: Decimal, idempotency_key: str):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise ValueError("Account not found")

    existing_transaction = (
        db.query(Transaction)
        .filter(Transaction.idempotency_key == idempotency_key)
        .first()
    )

    if existing_transaction:
        return existing_transaction

    if amount <= 0:
        raise ValueError("Amount must be positive")

    balance_before = account.balance
    balance_after = account.balance + amount

    account.balance = balance_after

    transaction = Transaction(
        account_id=account.id,
        transaction_type="deposit",
        amount=amount,
        balance_before=balance_before,
        balance_after=balance_after,
        status="completed",
        idempotency_key=idempotency_key,
    )

    db.add(transaction)
    db.commit()

    return transaction


def withdrawal(db: Session, account_id: UUID, amount: Decimal, idempotency_key: str):
    account = db.query(Account).filter(Account.id == account_id).first()

    existing_transaction = (
        db.query(Transaction)
        .filter(Transaction.idempotency_key == idempotency_key)
        .first()
    )

    if existing_transaction:
        return existing_transaction

    if account.balance < amount:
        raise ValueError("Insufficient funds")

    balance_before = account.balance
    balance_after = account.balance - amount

    account.balance = balance_after

    transaction = Transaction(
        account_id=account.id,
        transaction_type="withdrawal",
        amount=amount,
        balance_before=balance_before,
        balance_after=balance_after,
        status="completed",
        idempotency_key=idempotency_key,
    )

    db.add(transaction)
    db.commit()

    return transaction
