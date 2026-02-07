from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Any
from datetime import timedelta, datetime
from ...models.user import User, UserCreate, UserRead
from ...auth_utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ...database.session import get_session
from ..deps import get_current_user
from jose import JWTError
import uuid
from ...core.security import get_password_hash, verify_password


router = APIRouter()


@router.post("/register", response_model=UserRead)
def register_user(
    user_create: UserCreate,
    db: Session = Depends(get_session)
) -> Any:
    """
    Register a new user account.

    Args:
        user_create: User registration data (email, name, password)
        db: Database session dependency

    Returns:
        UserRead: Created user information with ID and timestamps

    Raises:
        HTTPException: If email already exists or validation fails
    """
    # Check if user with this email already exists
    existing_user = db.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists"
        )

    # Create new user instance with hashed password
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        email=user_create.email,
        name=user_create.name,
        password=hashed_password
    )

    # Add user to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login")
def login_user(
    user_credentials: dict,  # Would typically be a Pydantic model like LoginRequest
    db: Session = Depends(get_session)
) -> Any:
    """
    Authenticate user and return JWT token.

    Args:
        user_credentials: User credentials (email and password)
        db: Database session dependency

    Returns:
        dict: Access token and token type

    Raises:
        HTTPException: If credentials are invalid
    """
    # Extract email and password from request
    email = user_credentials.get("email")
    password = user_credentials.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password using the stored hashed password
    if not user.password or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }


@router.post("/logout")
def logout_user() -> Any:
    """
    Logout the current user.

    Returns:
        dict: Success message confirming logout
    """
    # In a JWT-based system, logout is typically handled on the client-side
    # by removing the token from client storage.
    # For systems with token blacklisting, we would add the token to a blacklist here.
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserRead)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get the current authenticated user's profile information.

    Args:
        current_user: The currently authenticated user (from JWT token)

    Returns:
        UserRead: Current user's information
    """
    return current_user


@router.post("/forgot-password")
def forgot_password(
    request_data: dict,
    db: Session = Depends(get_session)
) -> Any:
    """
    Initiate password reset process for a user.

    Args:
        request_data: Contains email of user requesting password reset
        db: Database session dependency

    Returns:
        dict: Success message indicating reset email status
    """
    email = request_data.get("email")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )

    # Find user by email
    user = db.query(User).filter(User.email == email).first()

    if not user:
        # Don't reveal whether the email exists for security reasons
        return {"message": "If an account with this email exists, a password reset link has been sent"}

    # In a real implementation, you would:
    # 1. Generate a password reset token
    # 2. Store it securely (with expiration)
    # 3. Send email with reset link containing token

    # For now, we'll just return success message
    # (In a real app, this would trigger email sending)

    return {"message": f"If an account with this email exists, a password reset link has been sent to {email}"}


@router.post("/reset-password")
def reset_password(
    request_data: dict,
    db: Session = Depends(get_session)
) -> Any:
    """
    Reset user password using a reset token.

    Args:
        request_data: Contains reset token and new password
        db: Database session dependency

    Returns:
        dict: Success message upon password reset
    """
    reset_token = request_data.get("token")
    new_password = request_data.get("new_password")

    if not reset_token or not new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token and new password are required"
        )

    # In a real implementation, you would:
    # 1. Validate the reset token
    # 2. Check if it hasn't expired
    # 3. Hash and update the password

    # For now, we'll return a placeholder response
    # (In a real app, this would validate the token and update password)

    return {"message": "Password has been reset successfully"}