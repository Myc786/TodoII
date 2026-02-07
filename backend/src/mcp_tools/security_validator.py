"""
Security Validator for Todo Chatbot Extension

This module implements security validation for the AI chatbot
to ensure all operations are properly authenticated and authorized.
"""

from typing import Dict, Any, Optional
import jwt
import logging
from datetime import datetime
from enum import Enum

from ..core.config import settings
from ..database.session import get_session
from ..models.user import User
from ..models.task import Task
from .input_sanitizer import input_sanitizer
from .rate_limiter import rate_limiter, RateLimitType
from .audit_logger import audit_logger, SecurityEventType


class SecurityLevel(Enum):
    """Enumeration of security levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SecurityValidator:
    """
    Validates security for chatbot operations.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    async def validate_jwt_token(self, token: str, ip_address: Optional[str] = None,
                                user_agent: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Validate a JWT token and return user information.

        Args:
            token: JWT token to validate
            ip_address: IP address of the request (for audit logging)
            user_agent: User agent string (for audit logging)

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
                await self.log_auth_failure(user_id, ip_address, user_agent, "token_expired")
                return None

            # Validate required fields
            if not user_id:
                self.logger.warning("Token missing user ID")
                await self.log_auth_failure(None, ip_address, user_agent, "missing_user_id")
                return None

            # Log successful authentication
            await self.log_auth_success(user_id, ip_address, user_agent)

            return {
                "user_id": user_id,
                "username": username,
                "email": email,
                "exp": exp
            }

        except jwt.ExpiredSignatureError:
            self.logger.warning("Token has expired")
            await self.log_auth_failure(None, ip_address, user_agent, "expired_signature")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("Invalid token provided")
            await self.log_auth_failure(None, ip_address, user_agent, "invalid_token")
            return None
        except Exception as e:
            self.logger.error(f"Error validating token: {str(e)}")
            await self.log_auth_failure(None, ip_address, user_agent, f"validation_error: {str(e)}")
            return None

    async def validate_user_access(self, user_id: str, resource_owner_id: str) -> bool:
        """
        Validate that a user has access to a specific resource.

        Args:
            user_id: ID of the requesting user
            resource_owner_id: ID of the resource owner

        Returns:
            True if user has access, False otherwise
        """
        # For now, implement a simple check - users can only access their own resources
        return user_id == resource_owner_id

    async def validate_task_access(self, user_id: str, task_id: str, ip_address: Optional[str] = None,
                                  action: str = "read") -> bool:
        """
        Validate that a user has access to a specific task.

        Args:
            user_id: ID of the requesting user
            task_id: ID of the task to access
            ip_address: IP address of the request (for audit logging)
            action: Action being performed on the task (for audit logging)

        Returns:
            True if user has access to the task, False otherwise
        """
        try:
            async with get_session() as session:
                # Get the task
                task = await session.get(Task, task_id)
                if not task:
                    self.logger.warning(f"Task {task_id} not found")
                    await self.log_unauthorized_access_attempt(user_id, task_id, action, ip_address)
                    return False

                # Check if the user is the owner of the task
                if str(task.owner_id) != user_id:
                    self.logger.warning(f"User {user_id} attempted to access task {task_id} owned by {task.owner_id}")
                    await self.log_unauthorized_access_attempt(user_id, task_id, action, ip_address)
                    return False

                # Log successful authorization
                await self.log_authz_success(user_id, task_id, action, ip_address)
                return True

        except Exception as e:
            self.logger.error(f"Error validating task access: {str(e)}")
            await self.log_authz_failure(user_id, task_id, action, ip_address, f"validation_error: {str(e)}")
            return False

    async def validate_input_sanitization(self, user_input: str, user_id: Optional[str] = None,
                                       ip_address: Optional[str] = None) -> str:
        """
        Sanitize user input to prevent injection attacks.

        Args:
            user_input: Raw user input
            user_id: ID of the user (for audit logging)
            ip_address: IP address of the request (for audit logging)

        Returns:
            Sanitized user input
        """
        if not user_input or not isinstance(user_input, str):
            return ""

        # Remove potentially dangerous characters/sequences
        sanitized = user_input

        # Remove potential SQL injection patterns
        dangerous_sql_patterns = [
            "DROP TABLE",
            "UNION SELECT",
            "INSERT INTO",
            "DELETE FROM",
            "UPDATE SET",
            "--",
            "/*",
            "*/",
            "xp_",
            "sp_"
        ]

        for pattern in dangerous_sql_patterns:
            if pattern.lower() in sanitized.lower():
                sanitized = sanitized.replace(pattern, "[FILTERED]")
                # Log the sanitization event
                await self.log_input_sanitization_triggered(user_id, user_input, sanitized, ip_address)

        # Remove potential XSS patterns
        dangerous_xss_patterns = [
            "<script",
            "</script>",
            "javascript:",
            "vbscript:",
            "onload=",
            "onerror=",
            "onclick=",
            "onmouseover=",
            "onmouseout="
        ]

        for pattern in dangerous_xss_patterns:
            if pattern.lower() in sanitized.lower():
                sanitized = sanitized.replace(pattern, "[FILTERED]")
                # Log the sanitization event
                await self.log_input_sanitization_triggered(user_id, user_input, sanitized, ip_address)

        # Additional sanitization could include:
        # - Limiting input length
        # - Validating against expected patterns
        # - Escaping special characters

        return sanitized

    async def validate_rate_limit(self, user_id: str, action: str = "chat") -> bool:
        """
        Validate that a user has not exceeded rate limits.

        Args:
            user_id: ID of the user
            action: Action being performed (used for rate limiting buckets)

        Returns:
            True if within rate limit, False otherwise
        """
        try:
            # Map action to rate limit type
            action_mapping = {
                "chat": RateLimitType.CHAT,
                "create_task": RateLimitType.TASK_CREATION,
                "list_tasks": RateLimitType.TASK_LIST,
                "update_task": RateLimitType.TASK_UPDATE,
                "complete_task": RateLimitType.TASK_COMPLETION,
                "delete_task": RateLimitType.TASK_DELETION,
            }

            rate_limit_type = action_mapping.get(action, RateLimitType.CHAT)

            # Check rate limit using the rate limiter
            is_allowed, remaining, reset_time = await rate_limiter.check_rate_limit(
                user_id, rate_limit_type
            )

            if not is_allowed:
                self.logger.warning(
                    f"Rate limit exceeded for user {user_id} on action {action}. "
                    f"Limit reset in {reset_time} seconds."
                )
                return False

            return True
        except Exception as e:
            self.logger.error(f"Error checking rate limit: {str(e)}")
            return True  # Fail open for rate limiting to prevent blocking legitimate requests

    async def validate_security_headers(self, headers: Dict[str, str]) -> bool:
        """
        Validate security-related headers.

        Args:
            headers: Request headers

        Returns:
            True if headers are valid, False otherwise
        """
        # Check for presence of security headers
        required_headers = ["authorization"]
        for header in required_headers:
            if header.lower() not in [h.lower() for h in headers.keys()]:
                self.logger.warning(f"Missing required header: {header}")
                return False

        # Additional security header validation could go here
        return True

    async def validate_prompt_injection(self, user_input: str, user_id: Optional[str] = None,
                                   ip_address: Optional[str] = None) -> bool:
        """
        Check for potential prompt injection attempts.

        Args:
            user_input: User input to check
            user_id: ID of the user (for audit logging)
            ip_address: IP address of the request (for audit logging)

        Returns:
            True if input appears safe, False if potential injection detected
        """
        # Use the enhanced prompt injection detection from input sanitizer
        detected_pattern = input_sanitizer.detect_prompt_injection_with_details(user_input)

        if detected_pattern:
            self.logger.warning(f"Prompt injection detected in input: {user_input[:100]}...")
            await self.log_prompt_injection_detected(user_id, user_input, detected_pattern, ip_address)
            return False

        return True

    async def log_security_event(self, event_type: str, user_id: Optional[str] = None,
                                details: Optional[Dict[str, Any]] = None):
        """
        Log a security-related event (legacy method maintained for compatibility).

        Args:
            event_type: Type of security event
            user_id: ID of the user involved (if applicable)
            details: Additional details about the event
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "details": details or {}
        }

        self.logger.info(f"Security Event: {log_entry}")

    async def log_auth_success(self, user_id: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None):
        """Log successful authentication event."""
        await audit_logger.log_authentication_success(user_id, ip_address, user_agent)

    async def log_auth_failure(self, user_id: Optional[str] = None, ip_address: Optional[str] = None,
                              user_agent: Optional[str] = None, reason: str = "unknown"):
        """Log authentication failure event."""
        await audit_logger.log_authentication_failure(user_id, ip_address, user_agent, reason)

    async def log_authz_success(self, user_id: str, resource_id: str, action: str, ip_address: Optional[str] = None):
        """Log successful authorization event."""
        await audit_logger.log_authorization_success(user_id, resource_id, action, ip_address)

    async def log_authz_failure(self, user_id: str, resource_id: str, action: str,
                               ip_address: Optional[str] = None, reason: str = "access_denied"):
        """Log authorization failure event."""
        await audit_logger.log_authorization_failure(user_id, resource_id, action, ip_address, reason)

    async def log_prompt_injection_detected(self, user_id: Optional[str], input_text: str,
                                          detected_pattern: str, ip_address: Optional[str] = None):
        """Log prompt injection attempt."""
        await audit_logger.log_prompt_injection_attempt(user_id, input_text, detected_pattern, ip_address)

    async def log_rate_limit_exceeded(self, user_id: str, action: str, ip_address: Optional[str] = None):
        """Log rate limit exceeded event."""
        await audit_logger.log_rate_limit_exceeded(user_id, action, ip_address)

    async def log_unauthorized_access_attempt(self, user_id: str, resource_id: str, action: str,
                                           ip_address: Optional[str] = None):
        """Log unauthorized access attempt."""
        await audit_logger.log_unauthorized_access_attempt(user_id, resource_id, action, ip_address)

    async def log_input_sanitization_triggered(self, user_id: Optional[str], original_input: str,
                                            sanitized_input: str, ip_address: Optional[str] = None):
        """Log when input sanitization is triggered."""
        await audit_logger.log_input_sanitization_triggered(user_id, original_input, sanitized_input, ip_address)

    async def validate_user_session(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate a user's session using their token.

        Args:
            token: User's authentication token

        Returns:
            Session information if valid, None otherwise
        """
        # Validate the token
        user_info = await self.validate_jwt_token(token)
        if not user_info:
            return None

        # Additional session validation could go here
        # For example, checking if the user is suspended, etc.

        return {
            "user_id": user_info["user_id"],
            "username": user_info.get("username"),
            "session_valid": True,
            "token_expires": user_info.get("exp")
        }


# Global instance of the security validator
security_validator = SecurityValidator()