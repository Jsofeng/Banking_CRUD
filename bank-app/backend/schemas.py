from datetime import datetime
from typing import Optional
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

"""
SQLAlchemy defines what the db table looks like
Pydantic defines what data coming in & out of your API looks like
"""


class AccountCreate(BaseModel):
    owner_name: str = Field(min_length=1)
    account_type: str = "chequing"
    balance: Decimal = Field(ge=0)


"""
You don’t require all fields
User can update only what they want
"""

# <---------------- ACCOUNT CLASS ---------------->


class AccountUpdate(BaseModel):
    owner_name: Optional[str] = None
    account_type: Optional[str] = None
    balance: Optional[Decimal] = None
    frozen: Optional[bool] = None


class AccountResponse(BaseModel):  # what the api sends back
    id: UUID
    owner_name: str
    account_type: str
    balance: Decimal
    frozen: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AccountTransaction(BaseModel):
    amount: Decimal = Field(ge=0)
    transaction_type: str


class DepositRequest(BaseModel):
    amount: Decimal = Field(gt=0)
    idempotency_key: str


class WithdrawalRequest(BaseModel):
    amount: Decimal = Field(gt=0)
    idempotency_key: str


class TransferRequest(BaseModel):
    from_account: UUID
    to_account: UUID
    amount: Decimal
    idempotency_key: str


class TransactionResponse(BaseModel):
    id: UUID
    account_id: UUID
    transaction_type: str
    amount: Decimal
    balance_before: Decimal
    balance_after: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AccountFreeze(BaseModel):
    freeze: bool


# <---------------- USER CLASS ---------------->


class UserCreate(BaseModel):
    username: str = Field(min_length=1)
    email: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# <---------------- TOKEN ---------------->


class Token(BaseModel):  # response after login
    access_token: str
    token_type: str = "bearer"


class TokenData(
    BaseModel
):  # decoded JWT info OPTIONAL bc token might be invalid * or missing "sub"
    username: Optional[str] = None
