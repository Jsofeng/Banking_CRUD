from sqlalchemy import Column, Integer, String, Boolean, DateTime
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


