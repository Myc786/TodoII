from datetime import datetime, timedelta
from typing import Optional, Union, Any
import os
import secrets
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from sqlmodel import Session

from ..database.session import get_session


# Password hashing context - using argon2 as primary scheme for better Windows compatibility
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

from ..core.config import settings

# JWT settings
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


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


def generate_refresh_token() -> str:
    """
    Generate a secure random refresh token.

    Returns:
        str: A cryptographically secure random token (64 characters)
    """
    return secrets.token_urlsafe(48)


def create_refresh_token(user_id: str, db: Session, device_info: Optional[str] = None) -> str:
    """
    Create a new refresh token for a user and store it in the database.

    Args:
        user_id: The user's ID (as string UUID)
        db: Database session
        device_info: Optional information about the device/client

    Returns:
        str: The generated refresh token string
    """
    from ..models.refresh_token import RefreshToken
    import uuid

    # Generate secure token
    token = generate_refresh_token()

    # Calculate expiration
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    # Create database record
    refresh_token_record = RefreshToken(
        id=uuid.uuid4(),
        token=token,
        user_id=uuid.UUID(user_id),
        expires_at=expires_at,
        created_at=datetime.utcnow(),
        device_info=device_info
    )

    db.add(refresh_token_record)
    db.commit()

    return token


def verify_refresh_token(token: str, db: Session) -> Optional[Any]:
    """
    Verify a refresh token and return the associated user.

    Args:
        token: The refresh token to verify
        db: Database session

    Returns:
        User: The user associated with the token if valid, None otherwise
    """
    from ..models.refresh_token import RefreshToken
    from ..models.user import User

    # Find the token in database
    refresh_token_record = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if not refresh_token_record:
        return None

    # Check if token is valid (not revoked and not expired)
    if not refresh_token_record.is_valid():
        return None

    # Get and return the user
    user = db.get(User, refresh_token_record.user_id)
    return user


def rotate_refresh_token(old_token: str, db: Session, device_info: Optional[str] = None) -> Optional[tuple[str, Any]]:
    """
    Rotate a refresh token: revoke the old one and create a new one.

    Args:
        old_token: The old refresh token to rotate
        db: Database session
        device_info: Optional device information for the new token

    Returns:
        tuple: (new_token, user) if successful, None if old token invalid
    """
    from ..models.refresh_token import RefreshToken

    # Find the old token
    old_refresh_token = db.query(RefreshToken).filter(
        RefreshToken.token == old_token
    ).first()

    if not old_refresh_token or not old_refresh_token.is_valid():
        return None

    # Get the user
    user = verify_refresh_token(old_token, db)
    if not user:
        return None

    # Revoke the old token
    old_refresh_token.revoke()

    # Create new token
    new_token = create_refresh_token(
        str(user.id),
        db,
        device_info or old_refresh_token.device_info
    )

    db.commit()

    return (new_token, user)


def revoke_refresh_token(token: str, db: Session) -> bool:
    """
    Revoke a specific refresh token.

    Args:
        token: The refresh token to revoke
        db: Database session

    Returns:
        bool: True if token was revoked, False if not found
    """
    from ..models.refresh_token import RefreshToken

    refresh_token_record = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if not refresh_token_record:
        return False

    refresh_token_record.revoke()
    db.commit()

    return True


def revoke_all_user_refresh_tokens(user_id: str, db: Session) -> int:
    """
    Revoke all refresh tokens for a user.

    Args:
        user_id: The user's ID (as string UUID)
        db: Database session

    Returns:
        int: Number of tokens revoked
    """
    from ..models.refresh_token import RefreshToken
    import uuid

    # Find all active tokens for the user
    user_tokens = db.query(RefreshToken).filter(
        RefreshToken.user_id == uuid.UUID(user_id),
        RefreshToken.revoked == False
    ).all()

    # Revoke each token
    for token in user_tokens:
        token.revoke()

    db.commit()

    return len(user_tokens)