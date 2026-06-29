from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

"""
SQLAlchemy defines what the db table looks like
Pydantic defines what data coming in & out of your API looks like
"""

class AccountCreate(BaseModel):
    owner_name: str = Field(min_length=1)
    account_type: str = "chequing"
    balance: int = Field(ge=0)

"""
You don’t require all fields
User can update only what they want
"""

# <---------------- ACCOUNT CLASS ---------------->

class AccountUpdate(BaseModel):
    owner_name: Optional[str] = None
    account_type: Optional[str] = None
    balance: Optional[int] = None
    frozen: Optional[bool] = None

    
class AccountResponse(BaseModel): #what the api sends back
    id: int
    owner_name: str
    account_type: str
    balance: int
    frozen: bool
    created_at: datetime
    

    class Config: #This lets Pydantic read SQLAlchemy objects directly instead of only reading plain dictionaries.
        from_attributes = True

class AccountTransaction(BaseModel):
    amount: int = Field(ge=0)
    transaction_type: str

class AccountFreeze(BaseModel):
    freeze: bool

# <---------------- USER CLASS ---------------->

class UserCreate(BaseModel):
    username: str = Field(min_length=1)
    email: str 
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

# <---------------- TOKEN ---------------->

class Token(BaseModel): #response after login
    access_token: str
    token_type: str =  "bearer"

class TokenData(BaseModel): #decoded JWT info OPTIONAL bc token might be invalid * or missing "sub"
    username: Optional[str] = None



"""
useful for reusability can just do AccountSomething(AccountBase): pass

class AccountBase(BaseModel):
    owner_name: str
    account_type: str = "chequing"
    balance: int

"""
