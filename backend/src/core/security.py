from datetime import datetime, timedelta
from typing import Optional, Union, TYPE_CHECKING
import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from sqlmodel import Session

if TYPE_CHECKING:
    from ..models.user import User

from ..database.session import get_session


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    return pwd_context.hash(password)


def authenticate_user(db_user: User, password: str) -> Optional[User]:
    """
    Authenticate a user by verifying their password.
    Note: In our current implementation, we're not storing password hashes in the User model
    since the spec didn't explicitly require it. This function is kept for extensibility.

    Args:
        db_user: The user object from the database
        password: The plain text password to verify (not used in current implementation)

    Returns:
        User: The user object if authentication would succeed
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


def get_current_user(
    token: str = Depends(lambda: None),  # Placeholder for actual dependency
    db: Session = Depends(get_session)
) -> 'User':
    """
    Get the current user from the JWT token.

    Args:
        token: The JWT token from the request
        db: Database session

    Returns:
        User: The authenticated user

    Raises:
        HTTPException: If the token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None:
        raise credentials_exception

    # Remove 'Bearer ' prefix if present
    if token.startswith("Bearer "):
        token = token[7:]

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    # Import here to avoid circular import issues
    from ..models.user import User

    # Assuming username is the email for our implementation
    user = db.query(User).filter(User.email == username).first()
    if user is None:
        raise credentials_exception

    return user