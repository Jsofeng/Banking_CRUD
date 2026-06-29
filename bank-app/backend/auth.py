from passlib.context import CryptContext #Passlib uses a "context" object to handle hashing
import os
import hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt, JWTError


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------------- AUTHENTICATION & AUTHORIZATION --------------------------

def hash_password(password: str):
    password = hashlib.sha256(password.encode()).hexdigest() # pre-hash to avoid bcrypt 72-byte limit
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    password = hashlib.sha256(plain.encode()).hexdigest()
    return pwd_context.verify(password, hashed) #if the password the user typed and the one that got hashed are == then return True


# -------------------------- JWT TOKEN  --------------------------

def create_access_token(data: dict):
    to_encode = data.copy() #usually {"sub": "jonathan"} sub = subject 
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    to_encode.update({"exp": expire}) #add the expiry time

    return jwt.encode(to_encode, SECRET_KEY, algorithms=ALGORITHM)

def verify_token(token):
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username : str = payload.get("sub")

        if username is None:
            raise JWTError("Token missing subject")
        
        return username
    
    except JWTError:
        # token is invalid, expired, or tampered with
        raise Exception("Invalid or expired token")
