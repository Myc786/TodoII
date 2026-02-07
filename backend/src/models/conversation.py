"""Conversation model for AI chatbot feature."""
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
import uuid


class Conversation(SQLModel, table=True):
    """
    Represents a chat conversation between user and AI assistant.

    A conversation contains multiple messages and persists across
    page reloads and server restarts (stateless design).
    """
    __tablename__ = "conversation"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")

    def __init__(self, **data):
        super().__init__(**data)
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
