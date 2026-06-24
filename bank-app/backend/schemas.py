from pydantic import BaseModel
from datetime import datetime
from typing import Optional

"""
SQLAlchemy defines what the db table looks like
Pydantic defines what data coming in & out of your API looks like
"""

class AccountCreate(BaseModel):
    owner_name: str
    account_type: str = "chequing"
    balance: int


"""
You don’t require all fields
User can update only what they want
"""
class AccountUpdate(BaseModel):
    owner_name: Optional[str] = None
    account_type: Optional[str] = None
    balance: Optional[int] = None

    
class AccountResponse(BaseModel): #what the api sends back
    id: int
    owner_name: str
    account_type: str
    balance: int
    created_at: datetime

    class Config: #This lets Pydantic read SQLAlchemy objects directly instead of only reading plain dictionaries.
        from_attributes = True

