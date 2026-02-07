"""
Base MCP Tool Class for Todo Chatbot Extension

This module defines the base class for all MCP tools that includes
authentication validation and common functionality.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, ValidationError
import jwt
from datetime import datetime
import logging

from ..core.config import settings
from ..database.session import get_session
from ..services.task_service import TaskService


class MCPToolError(Exception):
    """Custom exception for MCP tool errors."""
    pass


class AuthenticationError(MCPToolError):
    """Exception raised for authentication failures."""
    pass


class AuthorizationError(MCPToolError):
    """Exception raised for authorization failures."""
    pass


class BaseMCPTask:
    """
    Base class for all MCP tools that require authentication and user context.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    async def validate_and_execute(self, params: Dict[str, Any], token: str) -> Dict[str, Any]:
        """
        Validate the input parameters and execute the tool with authenticated user context.

        Args:
            params: Parameters for the tool execution
            token: JWT token for user authentication

        Returns:
            Result of the tool execution
        """
        try:
            # Validate input parameters
            validated_params = await self.validate_input(params)

            # Authenticate and get user context
            user_id = await self.authenticate_user(token)

            # Execute the specific tool logic
            result = await self.execute(validated_params, user_id)

            return {
                "success": True,
                "data": result
            }
        except AuthenticationError as e:
            self.logger.warning(f"Authentication failed: {str(e)}")
            return {
                "success": False,
                "error": "Authentication failed",
                "details": str(e)
            }
        except AuthorizationError as e:
            self.logger.warning(f"Authorization failed: {str(e)}")
            return {
                "success": False,
                "error": "Authorization failed",
                "details": str(e)
            }
        except ValidationError as e:
            self.logger.warning(f"Input validation failed: {str(e)}")
            return {
                "success": False,
                "error": "Invalid input parameters",
                "details": str(e)
            }
        except MCPToolError as e:
            self.logger.error(f"MCP tool error: {str(e)}")
            return {
                "success": False,
                "error": "Tool execution failed",
                "details": str(e)
            }
        except Exception as e:
            self.logger.error(f"Unexpected error in tool execution: {str(e)}")
            return {
                "success": False,
                "error": "Unexpected error occurred",
                "details": str(e)
            }

    async def authenticate_user(self, token: str) -> str:
        """
        Authenticate user using JWT token and return user ID.

        Args:
            token: JWT token to authenticate

        Returns:
            User ID of the authenticated user

        Raises:
            AuthenticationError: If token is invalid or expired
        """
        try:
            # Decode the JWT token
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )

            user_id = payload.get("sub")
            if not user_id:
                raise AuthenticationError("Invalid token: no user ID found")

            # Check if token is expired
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
                raise AuthenticationError("Token has expired")

            return user_id

        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
        except Exception as e:
            raise AuthenticationError(f"Authentication error: {str(e)}")

    async def validate_input(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input parameters. Override this method in subclasses.

        Args:
            params: Input parameters to validate

        Returns:
            Validated parameters (possibly transformed)
        """
        # Default implementation - just return the parameters as-is
        # Subclasses should override this method for specific validation
        return params

    @abstractmethod
    async def execute(self, params: Dict[str, Any], user_id: str) -> Any:
        """
        Execute the specific tool logic. This method must be implemented by subclasses.

        Args:
            params: Validated input parameters
            user_id: ID of the authenticated user

        Returns:
            Result of the tool execution
        """
        pass

    async def get_task_service(self):
        """
        Get an instance of the task service with a database session.

        Returns:
            TaskService instance
        """
        session = get_session()
        return TaskService(session)


class MCPTaskValidator(BaseModel):
    """
    Base validator for MCP task parameters.
    Subclasses should inherit from this to define specific parameter schemas.
    """
    pass