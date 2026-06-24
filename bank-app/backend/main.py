from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Account
from schemas import AccountCreate, AccountResponse, AccountUpdate

Base.metadata.create_all(bind=engine) #Look at all SQLAlchemy models that inherit from Base, and create their tables in Postgres if they don’t exist.

"""
models.py inherits Base & creates this 

CREATE TABLE accounts (
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    account = db.query(Account).filter(Account.id == id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return account

@app.put("/accounts/{id}", response_model=AccountResponse)
def update_account(id: int, updated_data: AccountUpdate, db: Session = Depends(get_db)):
    
    account = db.query(Account).filter(Account.id == id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if updated_data.owner_name is not None:
        account.owner_name = updated_data.owner_name

    if updated_data.account_type is not None:
        account.account_type = updated_data.account_type

    if updated_data.balance is not None:
        account.balance = updated_data.balance

    db.commit()
    db.refresh(account)

    return account

@app.delete("/accounts/{id}")
def delete_account(id: int, db: Session = Depends(get_db)):
    
    account = db.query(Account).filter(Account.id == id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    db.delete(account)
    db.commit()

    return {"message": f"Account: {id} deleted successfully"}

