"""
User Context Propagation for Todo Chatbot Extension

This module handles the propagation of user context across different MCP tools
to ensure proper authentication and authorization.
"""

import asyncio
import contextvars
from typing import Optional, Dict, Any, Callable
from contextlib import asynccontextmanager

from .auth_middleware import auth_middleware
from .session_manager import session_manager


# Context variables to store user context across async operations
user_context_var: contextvars.ContextVar[Optional[Dict[str, Any]]] = contextvars.ContextVar(
    "user_context", default=None
)
session_context_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "session_context", default=None
)
request_context_var: contextvars.ContextVar[Optional[Dict[str, Any]]] = contextvars.ContextVar(
    "request_context", default=None
)


class UserContextManager:
    """
    Manages user context propagation across MCP tools.
    """

    def __init__(self):
        self.auth_middleware = auth_middleware
        self.session_manager = session_manager

    async def set_user_context(self, token: str) -> bool:
        """
        Set the user context based on the provided JWT token.

        Args:
            token: JWT token to extract user context from

        Returns:
            True if context was set successfully, False otherwise
        """
        user_info = await self.auth_middleware.validate_token(token)
        if user_info:
            user_context_var.set(user_info)
            return True
        return False

    async def set_session_context(self, session_id: str):
        """
        Set the session context.

        Args:
            session_id: ID of the session to set as context
        """
        session_context_var.set(session_id)

    async def set_request_context(self, request_data: Dict[str, Any]):
        """
        Set the request context.

        Args:
            request_data: Dictionary containing request-specific data
        """
        request_context_var.set(request_data)

    def get_current_user_id(self) -> Optional[str]:
        """
        Get the user ID from the current context.

        Returns:
            User ID if available, None otherwise
        """
        user_context = user_context_var.get()
        if user_context:
            return user_context.get("user_id")
        return None

    def get_current_username(self) -> Optional[str]:
        """
        Get the username from the current context.

        Returns:
            Username if available, None otherwise
        """
        user_context = user_context_var.get()
        if user_context:
            return user_context.get("username")
        return None

    def get_current_session_id(self) -> Optional[str]:
        """
        Get the session ID from the current context.

        Returns:
            Session ID if available, None otherwise
        """
        return session_context_var.get()

    def get_current_request_context(self) -> Optional[Dict[str, Any]]:
        """
        Get the request context.

        Returns:
            Request context if available, None otherwise
        """
        return request_context_var.get()

    def get_current_user_context(self) -> Optional[Dict[str, Any]]:
        """
        Get the full user context.

        Returns:
            User context if available, None otherwise
        """
        return user_context_var.get()

    async def validate_user_authorization(self, resource_user_id: str) -> bool:
        """
        Validate that the current user is authorized to access a specific resource.

        Args:
            resource_user_id: ID of the user who owns the resource

        Returns:
            True if authorized, False otherwise
        """
        current_user_id = self.get_current_user_id()
        if not current_user_id:
            return False

        return await self.auth_middleware.authorize_user_for_resource(
            current_user_id, resource_user_id
        )

    @asynccontextmanager
    async def user_context(self, token: str, session_id: Optional[str] = None):
        """
        Async context manager to temporarily set user context.

        Args:
            token: JWT token to extract user context from
            session_id: Optional session ID to set as context
        """
        # Store original values to restore later
        original_user_context = user_context_var.get()
        original_session_context = session_context_var.get()

        try:
            # Set new context
            await self.set_user_context(token)
            if session_id:
                await self.set_session_context(session_id)

            yield self

        finally:
            # Restore original context
            user_context_var.set(original_user_context)
            session_context_var.set(original_session_context)

    @asynccontextmanager
    async def request_context(self, request_data: Dict[str, Any]):
        """
        Async context manager to temporarily set request context.

        Args:
            request_data: Dictionary containing request-specific data
        """
        original_request_context = request_context_var.get()

        try:
            # Set new request context
            await self.set_request_context(request_data)
            yield self

        finally:
            # Restore original context
            request_context_var.set(original_request_context)

    async def propagate_context_to_tool_call(self, tool_func: Callable, *args, **kwargs) -> Any:
        """
        Propagate the current context to a tool function call.

        Args:
            tool_func: The tool function to call
            *args: Arguments to pass to the tool function
            **kwargs: Keyword arguments to pass to the tool function

        Returns:
            Result of the tool function call
        """
        # Get current context
        current_user_context = user_context_var.get()
        current_session_context = session_context_var.get()
        current_request_context = request_context_var.get()

        # Create a new context with the current values
        ctx = contextvars.copy_context()

        # Call the tool function with the propagated context
        return await ctx.run(tool_func, *args, **kwargs)

    def clear_context(self):
        """Clear all context variables."""
        user_context_var.set(None)
        session_context_var.set(None)
        request_context_var.set(None)


# Global instance of the context manager
context_manager = UserContextManager()


# Convenience functions for easy access
def get_current_user_id() -> Optional[str]:
    """Get the current user ID from context."""
    return context_manager.get_current_user_id()


def get_current_session_id() -> Optional[str]:
    """Get the current session ID from context."""
    return context_manager.get_current_session_id()


def validate_user_authorization(resource_user_id: str) -> bool:
    """Validate that the current user is authorized to access a resource."""
    return asyncio.run(context_manager.validate_user_authorization(resource_user_id))


async def set_user_context(token: str) -> bool:
    """Set the user context from a token."""
    return await context_manager.set_user_context(token)


async def set_session_context(session_id: str):
    """Set the session context."""
    await context_manager.set_session_context(session_id)


@asynccontextmanager
async def user_context(token: str, session_id: Optional[str] = None):
    """Async context manager for user context."""
    async with context_manager.user_context(token, session_id):
        yield


@asynccontextmanager
async def request_context(request_data: Dict[str, Any]):
    """Async context manager for request context."""
    async with context_manager.request_context(request_data):
        yield