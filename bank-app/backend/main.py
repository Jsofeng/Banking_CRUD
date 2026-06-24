from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine, Base
from models import Account
from schemas import AccountCreate, AccountResponse, AccountUpdate

Base.metadata.create_all(bind=engine) #Look at all SQLAlchemy models that inherit from Base, and create their tables in Postgres if they don’t exist.

"""
models.py inherits Base & creates this 

CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    owner_name VARCHAR,
    account_type VARCHAR,
    balance INTEGER,
    created_at TIMESTAMP
);


"""
"""

With yield

✔ automatic setup
✔ automatic cleanup
✔ no connection leaks
✔ clean FastAPI integration

Think of it like renting a car:

* SessionLocal() → you pick up the car 🚗
* yield db → you drive it around
* route finishes → FastAPI returns car
* finally → you return the car

"""


app = FastAPI()

#react runs on port 5173 & fastapi runs on port 8000 using CORSMiddleware (Cross origin resource sharing)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#HELPER FUNCTION
def get_account(id: int, db: Session) -> Account:
    account = db.query(Account).filter(Account.id == id).first()
    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )
    
    return account

@app.post("/accounts", response_model=AccountResponse)
def create_account(accounts: AccountCreate, db: Session = Depends(get_db)):
    new_account = Account(
        owner_name = accounts.owner_name,
        account_type = accounts.account_type,
        balance = accounts.balance
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

@app.get("/accounts", response_model=list[AccountResponse])
def get_accounts(db: Session = Depends(get_db)):
    accounts = db.query(Account).all() #“SELECT * FROM accounts”
    return accounts

@app.get("/accounts/{id}", response_model=AccountResponse)
def get_account_id(id: int, db: Session = Depends(get_db)):
    account = get_account(id, db)
    
    return account

@app.put("/accounts/{id}", response_model=AccountResponse)
def update_account(id: int, updated_data: AccountUpdate, db: Session = Depends(get_db)):
    
    account = get_account(id, db)

    if updated_data.owner_name is not None:
        account.owner_name = updated_data.owner_name

    if updated_data.account_type is not None:
        account.account_type = updated_data.account_type

    if updated_data.balance is not None:
        account.balance = updated_data.balance

    if updated_data.frozen is not None:
        account.frozen = updated_data.frozen
    
    db.commit()
    db.refresh(account)

    return account

@app.delete("/accounts/{id}")
def delete_account(id: int, db: Session = Depends(get_db)):
    
    account = get_account(id, db)

    db.delete(account)
    db.commit()

    return {"message": f"Account: {id} deleted successfully"}


@app.patch("/accounts/{id}/freeze", response_model=AccountResponse) #allows for partial updates instead of whole object updating like PUT
def set_frozen(id: int, db: Session = Depends(get_db)):
    account = get_account(id, db)

    if account.frozen:
        raise HTTPException(status_code=400, detail="Account already frozen")

    account.frozen = True
    db.commit()
    db.refresh(account)

    return account

@app.patch("/accounts/{id}/unfreeze", response_model=AccountResponse) #allows for partial updates instead of whole object updating like PUT
def set_unfrozen(id: int, db: Session = Depends(get_db)):
    account = get_account(id, db)
    
    if not account.frozen:
        raise HTTPException(status_code=400, detail="Account is already unfrozen")

    
    account.frozen = False
    db.commit()
    db.refresh(account)

    return account

