import uuid
from decimal import Decimal
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    CheckConstraint,
    func,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class Account(Base):
    __tablename__ = "accounts"  # tells SQLAlchemy what to call the table in postgres

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    owner_name: Mapped[str | None] = mapped_column(String(100))

    account_type: Mapped[str] = mapped_column(
        String(20), nullable=False, default="chequing"
    )

    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    frozen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    # retrives the user that this account is associated with
    owner: Mapped["User"] = relationship(back_populates="accounts")

    # retrieves a list of associated transactions this account made
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="account")

    __table_args__ = (
        CheckConstraint("balance >= 0", name="check_balance_non_negative"),
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    username: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False, index=True
    )

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    accounts: Mapped[list["Account"]] = relationship(back_populates="owner")


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False, index=True
    )

    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)

    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    balance_before: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    balance_after: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    status: Mapped[str] = mapped_column(String(12), nullable=False, default="pending")

    idempotency_key: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    account: Mapped["Account"] = relationship(back_populates="transactions")

    __table_args__ = (
        CheckConstraint("amount > 0", name="check_transaction_amount_positive"),
    )
