from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine, Base
from models import Account, User
from schemas import AccountCreate, AccountResponse, AccountUpdate, AccountTransaction, AccountFreeze, UserCreate, UserResponse, Token, TokenData
from auth import hash_password, verify_password, create_access_token

Base.metadata.drop_all(bind=engine) #keep this for temporary use
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


@app.patch("/accounts/{id}/set_freeze", response_model=AccountResponse) #allows for partial updates instead of whole object updating like PUT
def set_frozen(id: int, request: AccountFreeze, db: Session = Depends(get_db)):
    account = get_account(id, db)

    freeze = request.freeze

    if account.frozen == freeze: #if we did "if account.frozen and freeze" and both are False then it would skip the condition therefore == is a safer & clean approach
        raise HTTPException(status_code=400, detail="No State Change Needed")
    
    account.frozen = freeze


    db.commit()
    db.refresh(account)

    return account


@app.patch("/accounts/{id}/transaction", response_model=AccountResponse)
def transaction(id, transaction: AccountTransaction, db: Session = Depends(get_db)):
    account = get_account(id, db)

    if transaction.transaction_type == "deposit":
        account.balance+=transaction.amount

    elif transaction.transaction_type == "withdrawal":
        if transaction.amount > account.balance:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        
        account.balance-=transaction.amount

    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")
    

    db.commit()
    db.refresh(account)

    return account

@app.post("/register", response_model=UserResponse)

def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pw = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        role="user"
    )
    db.add(new_user)
    db.commit()

    return new_user

@app.post("/login", response_model=Token)

def login(db: Session = Depends(get_db), form_data: OAuth2AuthorizationCodeBearer = Depends()): # form_data: OAuth2AuthorizationCodeBearer = Depends() automatically reads username=... password=...
    user = db.query(User).filter(User.username == form_data.username).first() #basically SELECT * FROM USERS WHERE username = form_data.username LIMIT 1

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub" : user.username}) #in the form of what create_access_token is supposed to take in

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



