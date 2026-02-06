"""Conversation model for AI chatbot feature."""
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class Conversation(SQLModel, table=True):
    """
    Represents a chat conversation between user and AI assistant.

    A conversation contains multiple messages and persists across
    page reloads and server restarts (stateless design).
    """
    __tablename__ = "conversation"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
