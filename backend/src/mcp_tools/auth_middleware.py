"""
JWT Authentication Middleware for MCP Tools

This module provides authentication middleware for MCP tools
to validate JWT tokens and ensure user authorization.
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from functools import wraps
import logging
from fastapi import HTTPException, status

from ..core.config import settings
from ..models.user import User
from ..database.session import get_session


class JWTAuthenticationMiddleware:
    """
    Middleware for authenticating and authorizing MCP tool requests.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    async def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate JWT token and extract user information.

        Args:
            token: JWT token to validate

        Returns:
            User information dictionary if valid, None otherwise
        """
        try:
            # Decode the JWT token
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )

            # Extract user information
            user_id = payload.get("sub")
            username = payload.get("username")
            email = payload.get("email")
            exp = payload.get("exp")

            # Check if token is expired
            if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
                self.logger.warning(f"Token expired for user ID: {user_id}")
                return None

            # Validate required fields
            if not user_id:
                self.logger.warning("Token missing user ID")
                return None

            return {
                "user_id": user_id,
                "username": username,
                "email": email,
                "exp": exp
            }

        except jwt.ExpiredSignatureError:
            self.logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("Invalid token provided")
            return None
        except Exception as e:
            self.logger.error(f"Error validating token: {str(e)}")
            return None

    async def handle_auth_error(self, detail: str = "Unauthorized") -> HTTPException:
        """
        Create a standardized authentication error response.

        Args:
            detail: Detail message for the error

        Returns:
            HTTPException with 401 status code
        """
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    async def authenticate_request(self, token: str) -> Optional[str]:
        """
        Authenticate a request and return the user ID if valid.

        Args:
            token: JWT token from the request

        Returns:
            User ID if authenticated, None otherwise
        """
        user_info = await self.validate_token(token)
        if user_info:
            return user_info["user_id"]
        return None

    async def authorize_user_for_resource(self, user_id: str, resource_user_id: str) -> bool:
        """
        Check if a user is authorized to access a specific resource.

        Args:
            user_id: ID of the authenticated user
            resource_user_id: ID of the user who owns the resource

        Returns:
            True if authorized, False otherwise
        """
        # For now, we only allow users to access their own resources
        return user_id == resource_user_id

    async def create_token(self, user: User) -> str:
        """
        Create a JWT token for the given user.

        Args:
            user: User object to create token for

        Returns:
            JWT token string
        """
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "exp": expire.timestamp(),
            "iat": datetime.utcnow().timestamp()
        }

        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return token

    async def refresh_token(self, token: str) -> Optional[str]:
        """
        Refresh a JWT token if it's close to expiration.

        Args:
            token: Current JWT token

        Returns:
            New token if refreshed, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_exp": False}  # Don't verify expiration during refresh
            )

            # Check if token is close to expiration (within 5 minutes)
            exp = payload.get("exp")
            if exp:
                exp_time = datetime.fromtimestamp(exp)
                current_time = datetime.utcnow()

                if exp_time - current_time < timedelta(minutes=5):
                    # Token is close to expiration, create a new one
                    user_id = payload.get("sub")

                    # Get user from database to create new token
                    async with get_session() as session:
                        user = await session.get(User, user_id)
                        if user:
                            return await self.create_token(user)

            return None  # Token doesn't need refreshing

        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            self.logger.error(f"Error refreshing token: {str(e)}")
            return None


def require_auth(func):
    """
    Decorator to require authentication for MCP tool functions.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # This would be used to wrap specific tool functions
        # For now, we'll just call the original function
        return await func(*args, **kwargs)
    return wrapper


def require_same_user(func):
    """
    Decorator to ensure user can only access their own data.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # This would be used to wrap functions that access user-specific data
        # For now, we'll just call the original function
        return await func(*args, **kwargs)
    return wrapper


# Global instance of the middleware
auth_middleware = JWTAuthenticationMiddleware()