from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Any
from datetime import timedelta
from ...models.user import User, UserCreate, UserRead
from ...auth_utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ...database.session import get_session
from ..deps import get_current_user
from jose import JWTError
import uuid
from ...core.security import (
    get_password_hash,
    verify_password,
    create_refresh_token,
    revoke_refresh_token,
    revoke_all_user_refresh_tokens,
    rotate_refresh_token,
    verify_refresh_token
)
import traceback


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
    try:
        # Check if user with this email already exists
        existing_user = db.query(User).filter(User.email == user_create.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists"
            )

        # Create new user instance with hashed password
        hashed_password = get_password_hash(user_create.password)
        from datetime import datetime
        import uuid
        db_user = User(
            id=uuid.uuid4(),
            email=user_create.email,
            name=user_create.name,
            password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Add user to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the full error for debugging
        print(f"Registration error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@router.post("/login")
def login_user(
    user_credentials: dict,  # Would typically be a Pydantic model like LoginRequest
    db: Session = Depends(get_session)
) -> Any:
    """
    Authenticate user and return JWT tokens (access + refresh).

    Args:
        user_credentials: User credentials (email and password)
        db: Database session dependency

    Returns:
        dict: Access token, refresh token, token type, and user info

    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        # Extract email and password from request
        email = user_credentials.get("email")
        password = user_credentials.get("password")
        device_info = user_credentials.get("device_info")  # Optional device information

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

        # Create refresh token
        refresh_token = create_refresh_token(
            str(user.id),
            db,
            device_info=device_info
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the full error for debugging
        print(f"Login error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.post("/refresh")
def refresh_token_endpoint(
    request_data: dict,
    db: Session = Depends(get_session)
) -> Any:
    """
    Refresh access token using a refresh token.
    Implements token rotation: old refresh token is revoked, new one is issued.

    Args:
        request_data: Contains refresh_token and optional device_info
        db: Database session dependency

    Returns:
        dict: New access token, new refresh token, token type, and user info

    Raises:
        HTTPException: If refresh token is invalid or expired
    """
    try:
        refresh_token = request_data.get("refresh_token")
        device_info = request_data.get("device_info")

        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token is required"
            )

        # Rotate the refresh token (validates, revokes old, creates new)
        result = rotate_refresh_token(refresh_token, db, device_info)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        new_refresh_token, user = result

        # Create new access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the full error for debugging
        print(f"Token refresh error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during token refresh"
        )


@router.post("/logout")
def logout_user(
    request_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Any:
    """
    Logout the current user by revoking refresh tokens.

    Args:
        request_data: Optional refresh_token to revoke specific token, or revoke_all flag
        current_user: The currently authenticated user (from JWT token)
        db: Database session dependency

    Returns:
        dict: Success message confirming logout
    """
    try:
        refresh_token = request_data.get("refresh_token")
        revoke_all = request_data.get("revoke_all", False)

        if revoke_all:
            # Revoke all refresh tokens for this user
            count = revoke_all_user_refresh_tokens(str(current_user.id), db)
            return {"message": f"Successfully logged out from all devices ({count} tokens revoked)"}
        elif refresh_token:
            # Revoke specific refresh token
            success = revoke_refresh_token(refresh_token, db)
            if success:
                return {"message": "Successfully logged out"}
            else:
                return {"message": "Refresh token not found or already revoked"}
        else:
            # If no refresh token provided, just acknowledge logout
            # (client should remove tokens from storage)
            return {"message": "Successfully logged out (client-side only)"}

    except Exception as e:
        print(f"Logout error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during logout"
        )


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
    try:
        return current_user
    except Exception as e:
        print(f"Get current user error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error retrieving user profile"
        )


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
    try:
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
    except HTTPException:
        raise
    except Exception as e:
        print(f"Forgot password error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during password reset request"
        )


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
    try:
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
    except HTTPException:
        raise
    except Exception as e:
        print(f"Reset password error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during password reset"
        )