from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine, Base
from models import Account, User, Transaction
from schemas import AccountCreate, AccountResponse, AccountUpdate, AccountTransaction, AccountFreeze, UserCreate, UserResponse, Token, TokenData, TransactionResponse
from auth import hash_password, verify_password, create_access_token, verify_token

#Base.metadata.drop_all(bind=engine) #keep this for temporary use
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

"""
oauth2_scheme = security guard at the door

He:
- checks for ID (token)
- pulls it out of your header
- hands it to your code
"""

oauth2_scheme = (OAuth2PasswordBearer(tokenUrl="login")) #Look for a JWT token in the Authorization header -> frontend sends -> Authorization: Bearer <token>


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = verify_token(token)

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or user not found"
        )
    
    return user

def require_admin(current_user: User = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return current_user
        

#HELPER FUNCTION
def get_account(id: int, db: Session, current_user: User) -> Account:
    account = db.query(Account).filter(Account.id == id, Account.owner_id == current_user.id).first()
    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )
    
    return account

@app.post("/accounts", response_model=AccountResponse)
def create_account(accounts: AccountCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_account = Account(
        owner_name = accounts.owner_name,
        account_type = accounts.account_type,
        balance = accounts.balance,
        owner_id = current_user.id
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

@app.get("/accounts", response_model=list[AccountResponse])
def get_accounts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    accounts = db.query(Account).filter(Account.owner_id == current_user.id).all() #“SELECT * FROM accounts INNER JOIN ON accounts.owner_id = current_user.id (Now each user only sees their own accounts)
    return accounts

@app.get("/accounts/{id}", response_model=AccountResponse)
def get_account_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = get_account(id, db current_user)
    
    return account

@app.put("/accounts/{id}", response_model=AccountResponse)
def update_account(id: int, updated_data: AccountUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    account = get_account(id, db, current_user)

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
def delete_account(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    account = get_account(id, db, current_user)

    db.delete(account)
    db.commit()

    return {"message": f"Account: {id} deleted successfully"}


@app.patch("/accounts/{id}/set_freeze", response_model=AccountResponse) #allows for partial updates instead of whole object updating like PUT
def set_frozen(id: int, request: AccountFreeze, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = get_account(id, db, current_user)

    freeze = request.freeze

    if account.frozen == freeze: #if we did "if account.frozen and freeze" and both are False then it would skip the condition therefore == is a safer & clean approach
        raise HTTPException(status_code=400, detail="No State Change Needed")
    
    account.frozen = freeze


    db.commit()
    db.refresh(account)

    return account


@app.patch("/accounts/{id}/transaction", response_model=TransactionResponse)
def transaction(id: int, transaction: AccountTransaction, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = get_account(id, db, current_user)

    if account.frozen:
        raise HTTPException(status_code=400, detail="Account is currently frozen")

    if transaction.transaction_type == "deposit":
        account.balance+=transaction.amount

    elif transaction.transaction_type == "withdrawal":
        if transaction.amount > account.balance:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        
        account.balance-=transaction.amount

    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    new_transaction = Transaction(
        account_id=account.id,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(account)
    
    return new_transaction

@app.get("/accounts/{id}/transaction", response_model=list[TransactionResponse])
def get_transactions(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = get_account(id, db, current_user)
    
    transactions = db.query(Transaction).filter(Transaction.account_id == account.id).all()    
    return transactions

@app.post("/register", response_model=UserResponse)

def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    existing_email = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    
    hashed_pw = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login", response_model=Token)

def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()): # form_data: OAuth2PasswordRequestForm = Depends() automatically reads username=... password=...
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

@app.get("/admin/accounts", response_model=list[AccountResponse])
def admin_dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_admin)): # Depends(require_admin) means this function can only run when this is successful
    accounts = db.query(Account).all()
    return accounts



