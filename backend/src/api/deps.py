from fastapi import Depends, HTTPException, status, Request
from typing import Generator, Optional
from sqlmodel import Session
import uuid
from ..database.session import get_session
from ..auth_utils import verify_token_http_exception, get_current_user_from_token
from ..models.user import User


def get_current_user(
    request: Request,
    db: Session = Depends(get_session)
) -> User:
    """
    Dependency to get the current authenticated user from the JWT token.

    Args:
        request: The incoming request containing the Authorization header
        db: Database session

    Returns:
        The authenticated user object

    Raises:
        HTTPException: If the token is invalid or user not found
    """
    # Extract the token from the Authorization header
    auth_header = request.headers.get("Authorization")

    # Debug logging
    print(f"[DEBUG get_current_user] Path: {request.url.path}")
    print(f"[DEBUG get_current_user] Auth header present: {auth_header is not None}")
    print(f"[DEBUG get_current_user] Auth header value: {auth_header[:50] if auth_header else 'None'}...")

    if not auth_header or not auth_header.startswith("Bearer "):
        print(f"[DEBUG get_current_user] FAIL: Invalid or missing header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ")[1]  # Extract token after "Bearer "
    print(f"[DEBUG get_current_user] Token extracted: {token[:30]}...")

    # Verify the token and get user info
    try:
        payload = verify_token_http_exception(token)
        user_id = payload.get("sub")
        print(f"[DEBUG get_current_user] Token valid, user_id: {user_id}")
    except Exception as e:
        print(f"[DEBUG get_current_user] Token verification failed: {e}")
        raise

    # Retrieve the user from the database
    # Convert string ID back to UUID for database lookup
    try:
        user = db.get(User, uuid.UUID(user_id))
        print(f"[DEBUG get_current_user] User lookup: {'found' if user else 'not found'}")
    except Exception as e:
        print(f"[DEBUG get_current_user] Database error: {e}")
        raise

    if not user:
        print(f"[DEBUG get_current_user] FAIL: User not found in database")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"[DEBUG get_current_user] SUCCESS: User authenticated - {user.email}")
    return user


def get_optional_current_user(
    request: Request,
    db: Session = Depends(get_session)
) -> Optional[User]:
    """
    Dependency to get the current user if authenticated, or None if not.

    Args:
        request: The incoming request containing the Authorization header
        db: Database session

    Returns:
        The authenticated user object, or None if no valid token
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]

    # Try to verify the token
    try:
        payload = verify_token_http_exception(token)
        user_id = payload.get("sub")

        # Retrieve the user from the database
        # Convert string ID back to UUID for database lookup
        user = db.get(User, uuid.UUID(user_id))
        return user
    except HTTPException:
        # If token verification fails, return None
        return None


# For backward compatibility or if we need just the token payload
def get_current_user_payload(request: Request) -> dict:
    """
    Dependency to get the current user's JWT payload.

    Args:
        request: The incoming request containing the Authorization header

    Returns:
        The JWT payload containing user information
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ")[1]
    payload = verify_token_http_exception(token)
    return payload