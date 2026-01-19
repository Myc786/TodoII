"""
Chat Session Manager for Todo Chatbot Extension

This module manages chat sessions for users interacting with the AI chatbot.
"""

import uuid
import time
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum


class SessionStatus(Enum):
    """Enumeration for chat session statuses."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"


@dataclass
class ChatSession:
    """Represents a single chat session for a user."""
    id: str
    user_id: str
    created_at: datetime
    last_activity_at: datetime
    status: SessionStatus
    messages: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, message: Dict[str, Any]):
        """Add a message to the session."""
        self.messages.append(message)
        self.last_activity_at = datetime.utcnow()

    def is_expired(self, ttl_minutes: int = 30) -> bool:
        """Check if the session has expired based on TTL."""
        expiry_time = self.last_activity_at + timedelta(minutes=ttl_minutes)
        return datetime.utcnow() > expiry_time

    def update_status(self, status: SessionStatus):
        """Update the session status."""
        self.status = status


class ChatSessionManager:
    """
    Manages chat sessions for users interacting with the AI chatbot.
    """

    def __init__(self, session_ttl_minutes: int = 30):
        self.sessions: Dict[str, ChatSession] = {}
        self.session_ttl_minutes = session_ttl_minutes
        self.cleanup_interval = 60  # seconds
        self.last_cleanup = time.time()

    async def create_session(self, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> ChatSession:
        """
        Create a new chat session for a user.

        Args:
            user_id: ID of the user requesting the session
            metadata: Optional metadata to associate with the session

        Returns:
            Created ChatSession object
        """
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()

        session = ChatSession(
            id=session_id,
            user_id=user_id,
            created_at=now,
            last_activity_at=now,
            status=SessionStatus.ACTIVE,
            metadata=metadata or {}
        )

        self.sessions[session_id] = session
        return session

    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Retrieve a chat session by ID.

        Args:
            session_id: ID of the session to retrieve

        Returns:
            ChatSession object if found, None otherwise
        """
        await self._cleanup_expired_sessions()

        if session_id not in self.sessions:
            return None

        session = self.sessions[session_id]

        # Check if session is expired
        if session.is_expired(self.session_ttl_minutes):
            await self.expire_session(session_id)
            return None

        # Update last activity time
        session.last_activity_at = datetime.utcnow()
        return session

    async def get_user_session(self, user_id: str) -> Optional[ChatSession]:
        """
        Get the active session for a specific user.

        Args:
            user_id: ID of the user whose session to retrieve

        Returns:
            ChatSession object if found, None otherwise
        """
        await self._cleanup_expired_sessions()

        # Find active session for user
        for session in self.sessions.values():
            if (session.user_id == user_id and
                session.status == SessionStatus.ACTIVE and
                not session.is_expired(self.session_ttl_minutes)):

                session.last_activity_at = datetime.utcnow()
                return session

        return None

    async def add_message_to_session(self, session_id: str, message: Dict[str, Any]) -> bool:
        """
        Add a message to a chat session.

        Args:
            session_id: ID of the session to add message to
            message: Message object to add

        Returns:
            True if successful, False otherwise
        """
        session = await self.get_session(session_id)
        if not session:
            return False

        session.add_message(message)
        return True

    async def update_session_status(self, session_id: str, status: SessionStatus) -> bool:
        """
        Update the status of a chat session.

        Args:
            session_id: ID of the session to update
            status: New status for the session

        Returns:
            True if successful, False otherwise
        """
        session = await self.get_session(session_id)
        if not session:
            return False

        session.update_status(status)
        return True

    async def expire_session(self, session_id: str) -> bool:
        """
        Mark a session as expired and remove it from active sessions.

        Args:
            session_id: ID of the session to expire

        Returns:
            True if successful, False otherwise
        """
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.status = SessionStatus.EXPIRED
            del self.sessions[session_id]
            return True
        return False

    async def end_session(self, session_id: str) -> bool:
        """
        End a session by marking it as inactive.

        Args:
            session_id: ID of the session to end

        Returns:
            True if successful, False otherwise
        """
        session = await self.get_session(session_id)
        if not session:
            return False

        session.status = SessionStatus.INACTIVE
        return True

    async def get_user_sessions(self, user_id: str) -> List[ChatSession]:
        """
        Get all sessions for a specific user.

        Args:
            user_id: ID of the user whose sessions to retrieve

        Returns:
            List of ChatSession objects for the user
        """
        await self._cleanup_expired_sessions()

        user_sessions = []
        for session in self.sessions.values():
            if session.user_id == user_id:
                if not session.is_expired(self.session_ttl_minutes):
                    user_sessions.append(session)
                else:
                    # Clean up expired session
                    await self.expire_session(session.id)

        return user_sessions

    async def _cleanup_expired_sessions(self):
        """Remove expired sessions from memory."""
        current_time = time.time()
        if current_time - self.last_cleanup < self.cleanup_interval:
            return  # Don't cleanup too frequently

        expired_sessions = []
        for session_id, session in self.sessions.items():
            if session.is_expired(self.session_ttl_minutes):
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            del self.sessions[session_id]

        self.last_cleanup = current_time

    async def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get the message history for a session.

        Args:
            session_id: ID of the session to get history for
            limit: Optional limit on number of messages to return

        Returns:
            List of messages in the session
        """
        session = await self.get_session(session_id)
        if not session:
            return []

        messages = session.messages
        if limit:
            messages = messages[-limit:]  # Get last 'limit' messages

        return messages


# Global instance of the session manager
session_manager = ChatSessionManager()