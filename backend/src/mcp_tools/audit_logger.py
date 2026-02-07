"""
Audit Logger for Security Events

This module implements comprehensive audit logging for security-related events
in the AI chatbot extension.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import logging
import json
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
import asyncio


class SecurityEventType(Enum):
    """Enumeration of security event types."""
    AUTHENTICATION_SUCCESS = "authentication_success"
    AUTHENTICATION_FAILURE = "authentication_failure"
    AUTHORIZATION_SUCCESS = "authorization_success"
    AUTHORIZATION_FAILURE = "authorization_failure"
    PROMPT_INJECTION_ATTEMPT = "prompt_injection_attempt"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    DATA_ACCESS_ATTEMPT = "data_access_attempt"
    UNAUTHORIZED_ACCESS_ATTEMPT = "unauthorized_access_attempt"
    INPUT_SANITIZATION_TRIGGERED = "input_sanitization_triggered"
    SESSION_CREATED = "session_created"
    SESSION_DESTROYED = "session_destroyed"
    TOKEN_REFRESH = "token_refresh"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"


@dataclass
class AuditLogEntry:
    """Structure for audit log entries."""
    timestamp: datetime
    event_type: SecurityEventType
    user_id: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    resource_id: Optional[str]
    action: Optional[str]
    details: Dict[str, Any]
    severity: str  # INFO, WARNING, ERROR, CRITICAL


class AuditLogger:
    """
    Implements comprehensive audit logging for security events.
    """

    def __init__(self, log_file_path: str = "security_audit.log"):
        self.logger = logging.getLogger(self.__class__.__name__)

        # Set up file handler for audit logs
        self.log_file_path = log_file_path
        self.file_handler = logging.FileHandler(log_file_path)
        self.file_handler.setLevel(logging.INFO)

        # Create formatter for audit logs
        formatter = logging.Formatter(
            '%(asctime)s - AUDIT - %(levelname)s - %(message)s'
        )
        self.file_handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(self.file_handler)
        self.logger.setLevel(logging.INFO)

    async def log_security_event(
        self,
        event_type: SecurityEventType,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        resource_id: Optional[str] = None,
        action: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        severity: str = "INFO"
    ):
        """
        Log a security-related event.

        Args:
            event_type: Type of security event
            user_id: ID of the user involved (if applicable)
            ip_address: IP address of the request (if available)
            user_agent: User agent string (if available)
            resource_id: ID of the resource involved (if applicable)
            action: Specific action that triggered the event
            details: Additional details about the event
            severity: Severity level of the event
        """
        if details is None:
            details = {}

        log_entry = AuditLogEntry(
            timestamp=datetime.utcnow(),
            event_type=event_type,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            resource_id=resource_id,
            action=action,
            details=details,
            severity=severity
        )

        # Create structured log message
        log_data = {
            "timestamp": log_entry.timestamp.isoformat(),
            "event_type": log_entry.event_type.value,
            "user_id": log_entry.user_id,
            "ip_address": log_entry.ip_address,
            "user_agent": log_entry.user_agent,
            "resource_id": log_entry.resource_id,
            "action": log_entry.action,
            "details": log_entry.details,
            "severity": log_entry.severity
        }

        # Log the event
        log_message = f"AUDIT_EVENT: {json.dumps(log_data)}"

        if severity == "CRITICAL":
            self.logger.critical(log_message)
        elif severity == "ERROR":
            self.logger.error(log_message)
        elif severity == "WARNING":
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)

    async def log_authentication_success(
        self,
        user_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """Log successful authentication event."""
        await self.log_security_event(
            event_type=SecurityEventType.AUTHENTICATION_SUCCESS,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            severity="INFO"
        )

    async def log_authentication_failure(
        self,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        reason: str = "unknown"
    ):
        """Log authentication failure event."""
        await self.log_security_event(
            event_type=SecurityEventType.AUTHENTICATION_FAILURE,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details={"reason": reason},
            severity="WARNING"
        )

    async def log_authorization_success(
        self,
        user_id: str,
        resource_id: str,
        action: str,
        ip_address: Optional[str] = None
    ):
        """Log successful authorization event."""
        await self.log_security_event(
            event_type=SecurityEventType.AUTHORIZATION_SUCCESS,
            user_id=user_id,
            resource_id=resource_id,
            action=action,
            ip_address=ip_address,
            severity="INFO"
        )

    async def log_authorization_failure(
        self,
        user_id: str,
        resource_id: str,
        action: str,
        ip_address: Optional[str] = None,
        reason: str = "access_denied"
    ):
        """Log authorization failure event."""
        await self.log_security_event(
            event_type=SecurityEventType.AUTHORIZATION_FAILURE,
            user_id=user_id,
            resource_id=resource_id,
            action=action,
            ip_address=ip_address,
            details={"reason": reason},
            severity="WARNING"
        )

    async def log_prompt_injection_attempt(
        self,
        user_id: Optional[str],
        input_text: str,
        detected_pattern: str,
        ip_address: Optional[str] = None
    ):
        """Log prompt injection attempt."""
        await self.log_security_event(
            event_type=SecurityEventType.PROMPT_INJECTION_ATTEMPT,
            user_id=user_id,
            ip_address=ip_address,
            details={
                "detected_pattern": detected_pattern,
                "input_preview": input_text[:100] + "..." if len(input_text) > 100 else input_text
            },
            severity="WARNING"
        )

    async def log_rate_limit_exceeded(
        self,
        user_id: str,
        action: str,
        ip_address: Optional[str] = None
    ):
        """Log rate limit exceeded event."""
        await self.log_security_event(
            event_type=SecurityEventType.RATE_LIMIT_EXCEEDED,
            user_id=user_id,
            action=action,
            ip_address=ip_address,
            severity="WARNING"
        )

    async def log_unauthorized_access_attempt(
        self,
        user_id: str,
        resource_id: str,
        action: str,
        ip_address: Optional[str] = None
    ):
        """Log unauthorized access attempt."""
        await self.log_security_event(
            event_type=SecurityEventType.UNAUTHORIZED_ACCESS_ATTEMPT,
            user_id=user_id,
            resource_id=resource_id,
            action=action,
            ip_address=ip_address,
            severity="WARNING"
        )

    async def log_input_sanitization_triggered(
        self,
        user_id: Optional[str],
        original_input: str,
        sanitized_input: str,
        ip_address: Optional[str] = None
    ):
        """Log when input sanitization is triggered."""
        await self.log_security_event(
            event_type=SecurityEventType.INPUT_SANITIZATION_TRIGGERED,
            user_id=user_id,
            ip_address=ip_address,
            details={
                "original_input_preview": original_input[:100] + "..." if len(original_input) > 100 else original_input,
                "sanitized_input_preview": sanitized_input[:100] + "..." if len(sanitized_input) > 100 else sanitized_input
            },
            severity="INFO"
        )

    async def get_recent_events(
        self,
        event_type: Optional[SecurityEventType] = None,
        limit: int = 100
    ) -> list:
        """
        Retrieve recent audit events (for monitoring purposes).

        Args:
            event_type: Filter by specific event type (optional)
            limit: Maximum number of events to return

        Returns:
            List of recent audit events
        """
        try:
            if not Path(self.log_file_path).exists():
                return []

            events = []
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                # Process lines in reverse to get most recent first
                for line in reversed(lines[-limit:]):
                    if "AUDIT_EVENT:" in line:
                        try:
                            # Extract JSON part from the log line
                            json_part = line.split("AUDIT_EVENT:")[1].strip()
                            event_data = json.loads(json_part)

                            if event_type is None or event_data["event_type"] == event_type.value:
                                events.append(event_data)
                        except (json.JSONDecodeError, IndexError):
                            continue

                        if len(events) >= limit:
                            break

            return events
        except Exception as e:
            self.logger.error(f"Error reading audit log: {str(e)}")
            return []

    async def cleanup_old_logs(self, days_to_keep: int = 30):
        """
        Clean up old audit log files.

        Args:
            days_to_keep: Number of days of logs to keep
        """
        try:
            log_path = Path(self.log_file_path)
            if log_path.exists():
                # For this simple implementation, we just keep one file
                # In a production system, you might implement log rotation
                pass
        except Exception as e:
            self.logger.error(f"Error cleaning up old logs: {str(e)}")


# Global instance of the audit logger
audit_logger = AuditLogger()