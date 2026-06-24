from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Account
from schemas import AccountCreate, AccountResponse


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

