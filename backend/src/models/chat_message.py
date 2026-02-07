"""
Chat Message Entity for Todo Chatbot Extension

This module defines the ChatMessage entity for storing chat conversations
between users and the AI chatbot.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
import uuid


class ChatMessageBase(SQLModel):
    """Base class for ChatMessage with common fields."""
    content: str = Field(min_length=1, max_length=10000)
    sender: str = Field(regex=r"^(user|ai)$")  # Either 'user' or 'ai'
    session_id: str = Field(foreign_key="chatsession.id")
    user_id: str = Field(foreign_key="user.id")
    intent: Optional[str] = Field(default=None, max_length=100)
    tool_call: Optional[Dict[str, Any]] = Field(default=None, sa_column_kwargs={"nullable": True})
    response_metadata: Optional[Dict[str, Any]] = Field(default=None, sa_column_kwargs={"nullable": True})


class ChatMessage(ChatMessageBase, table=True):
    """ChatMessage entity that represents a single message in a chat conversation."""
    __tablename__ = "chat_messages"

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship with User and ChatSession
    # Note: We're assuming User model exists and ChatSession will be defined


class ChatMessageCreate(ChatMessageBase):
    """Schema for creating a new ChatMessage."""
    pass


class ChatMessageRead(ChatMessageBase):
    """Schema for reading a ChatMessage with additional fields."""
    id: str
    timestamp: datetime


class ChatMessageUpdate(SQLModel):
    """Schema for updating a ChatMessage."""
    content: Optional[str] = Field(default=None, min_length=1, max_length=10000)
    intent: Optional[str] = Field(default=None, max_length=100)
    tool_call: Optional[Dict[str, Any]] = Field(default=None)


# Chat Session entity to go along with ChatMessage
class ChatSessionBase(SQLModel):
    """Base class for ChatSession with common fields."""
    user_id: str = Field(foreign_key="user.id")
    is_active: bool = Field(default=True)


class ChatSession(ChatSessionBase, table=True):
    """ChatSession entity that represents a single chat session."""
    __tablename__ = "chatsessions"

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to chat messages
    messages: list["ChatMessage"] = Relationship(back_populates="session")


class ChatSessionCreate(ChatSessionBase):
    """Schema for creating a new ChatSession."""
    pass


class ChatSessionRead(ChatSessionBase):
    """Schema for reading a ChatSession with additional fields."""
    id: str
    created_at: datetime
    last_activity_at: datetime


class ChatSessionUpdate(SQLModel):
    """Schema for updating a ChatSession."""
    is_active: Optional[bool] = Field(default=None)