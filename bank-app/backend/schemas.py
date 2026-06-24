from pydantic import BaseModel
from datetime import datetime
"""
SQLAlchemy defines what the db table looks like
Pydantic defines what data coming in & out of your API looks like
"""

class AccountCreate(BaseModel):
    owner_name: str
    account_type: str = "chequing"
    balance: int


class AccountResponse(BaseModel): #what the api sends back
    id: int
    owner_name: str
    account_type: str
    balance: int
    created_at: datetime

    class Config: #This lets Pydantic read SQLAlchemy objects directly instead of only reading plain dictionaries.
        from_attributes = True