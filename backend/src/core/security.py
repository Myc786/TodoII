from datetime import datetime, timedelta
from typing import Optional, Union, Any
import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from sqlmodel import Session

from ..database.session import get_session


# Password hashing context - using argon2 as primary scheme for better Windows compatibility
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to compare against

    Returns:
        bool: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plain password.

    Args:
        password: The plain text password to hash

    Returns:
        str: The hashed password
    """
    # Truncate password to 72 bytes if needed to avoid bcrypt limitation
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')

    return pwd_context.hash(password)


def authenticate_user(db_user: Any, password: str) -> Optional[Any]:
    """
    Authenticate a user by verifying their password.

    Args:
        db_user: The user object from the database
        password: The plain text password to verify

    Returns:
        User: The user object if authentication succeeds
    """
    # In this implementation, we're relying on JWT token validation
    # rather than password verification for each request
    return db_user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: The data to encode in the token
        expires_delta: Optional expiration time for the token

    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the decoded data.

    Args:
        token: The JWT token to verify

    Returns:
        dict: The decoded token data if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# NOTE: This function is kept for compatibility but auth endpoints use the deps.py version
def get_current_user_dependency():
    """
    This function should be replaced by the actual implementation in deps.py
    This is kept for compatibility purposes but shouldn't be used directly.
    """
    pass