from jose import JWTError, jwt
from fastapi import HTTPException, status
from typing import Optional, Dict, Any
import os
from datetime import datetime, timedelta
from .models.user import User


# JWT Configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback-secret-key-for-development")
if not os.getenv("BETTER_AUTH_SECRET"):
    print("WARNING: BETTER_AUTH_SECRET environment variable not set, using fallback. This should be set for production!")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with the provided data.

    Args:
        data: Dictionary containing the claims to be included in the token
        expires_delta: Optional timedelta for token expiration (defaults to 30 minutes)

    Returns:
        Encoded JWT token as string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT token and return the payload if valid.

    Args:
        token: JWT token string to verify

    Returns:
        Dictionary containing the token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_token_http_exception(token: str) -> Dict[str, Any]:
    """
    Verify a JWT token and raise HTTPException if invalid.

    Args:
        token: JWT token string to verify

    Returns:
        Dictionary containing the token payload if valid

    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    return payload


def get_current_user_from_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Extract user information from a JWT token.

    Args:
        token: JWT token string to extract user info from

    Returns:
        Dictionary containing user information if token is valid, None otherwise
    """
    payload = verify_token(token)
    if payload is None:
        return None

    user_id = payload.get("sub")
    if user_id is None:
        return None

    return {
        "id": user_id,
        "email": payload.get("email"),
        "name": payload.get("name")
    }