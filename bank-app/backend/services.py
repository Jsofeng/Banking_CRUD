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


def transfer(
    db: Session,
    from_account: UUID,
    to_account: UUID,
    amount: Decimal,
    idempotency_key: str,
):
    f_acc = db.query(Account).filter(Account.id == from_account).first()
    t_acc = db.query(Account).filter(Account.id == to_account).first()

    if from_account == to_account:
        raise ValueError("Cannot fund same account")

    existing_transaction = (
        db.query(Transaction)
        .filter(Transaction.idempotency_key == idempotency_key)
        .all()
    )

    if existing_transaction:
        return existing_transaction

    f_acc_balance_before = f_acc.balance
    t_acc_balance_before = t_acc.balance

    if f_acc_balance_before < amount:
        raise ValueError("Insufficient funds")

    f_acc_balance_after = f_acc_balance_before - amount
    t_acc_balance_after = t_acc_balance_before + amount

    f_acc.balance = f_acc_balance_after
    t_acc.balance = t_acc_balance_after

    transaction_sent = Transaction(
        account_id=f_acc.id,
        transaction_type="transfer",
        amount=amount,
        balance_before=f_acc_balance_before,
        balance_after=f_acc_balance_after,
        status="completed",
        idempotency_key=idempotency_key,
    )

    transaction_received = Transaction(
        account_id=t_acc.id,
        transaction_type="transfer",
        amount=amount,
        balance_before=t_acc_balance_before,
        balance_after=t_acc_balance_after,
        status="completed",
        idempotency_key=idempotency_key,
    )

    db.add(transaction_sent)
    db.add(transaction_received)
    db.commit()

    return [transaction_sent, transaction_received]
