from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime

from database import Base


class Account(Base):
    __tablename__ = "accounts"  #tells SQLAlchemy what to call the table in postgres

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) #index=True means create an index on this column
    owner_name = Column(String(100))
    account_type = Column(String(20), nullable=False, default="chequing")
    balance = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    frozen = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    role = Column(
        String,
        nullable=False,
        default="user"   # "user" or "admin"
    )

    created_at = Column(DateTime, default=datetime.utcnow)

class Transactions(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    transaction_type = Column(String) #deposit or withdrawl for now
    amount = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    

