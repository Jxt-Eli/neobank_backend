from passlib.context import CryptContext
import hashlib
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os



load_dotenv()
# ------password context-------

pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto", 
)
# ---sha256 + bcrypt password hashing---
def hash_password(password: str) -> str:
    pre_hashed = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(pre_hashed)

# ---verify password by hashing and comparing to stored hash---
def verify_password(plain_password: str, hashed_password: str)-> bool:
    pre_hashed = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(pre_hashed, hashed_password)



# ---JWT configuration---

SECRET_KEY = os.getenv("SECRET_KEY")  # HACK: TEMPORARY FIX, WILL USE ENVIRONMENT VARIABLES LATER
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict):
    """creates a JWT token with expiration time"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """decodes and verifies a jwt token and returns the user_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None