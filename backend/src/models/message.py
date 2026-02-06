"""Message model for AI chatbot feature."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Message(SQLModel, table=True):
    """
    Represents a single message in a conversation.

    Messages are immutable once created (audit trail).
    Tool calls stored as JSON string for debugging/UI display.
    """
    __tablename__ = "message"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role: str = Field(...)  # "user" | "assistant" | "system"
    content: str = Field(...)
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
