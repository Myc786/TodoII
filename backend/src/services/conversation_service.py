"""Conversation service for managing chat conversations and message history."""
from datetime import datetime
from typing import List, Optional, Union
from sqlmodel import Session, select
import uuid
from ..models.conversation import Conversation
from ..models.message import Message


class ConversationService:
    """
    Service for conversation and message CRUD operations.

    Implements stateless design - loads full history per request.
    """

    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, user_id: uuid.UUID) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            user_id: User ID from JWT authentication

        Returns:
            Created Conversation object
        """
        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation(self, conversation_id: int, user_id: uuid.UUID) -> Optional[Conversation]:
        """
        Get a conversation by ID with ownership validation.

        Args:
            conversation_id: Conversation ID
            user_id: User ID for ownership check

        Returns:
            Conversation object or None if not found/unauthorized
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = self.session.exec(statement).first()
        return conversation

    def get_conversation_history(self, conversation_id: int, user_id: uuid.UUID, limit: int = 100) -> List[Message]:
        """
        Load conversation message history with ownership validation.

        Implements stateless design - reloads full history per request.
        Database indexes ensure < 1 second query time for 100 messages.

        Args:
            conversation_id: Conversation ID
            user_id: User ID for ownership check
            limit: Maximum messages to load (default 100)

        Returns:
            List of Message objects ordered by created_at ASC
        """
        statement = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id
            )
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        messages = self.session.exec(statement).all()
        return list(messages)

    def add_message(
        self,
        conversation_id: int,
        user_id: uuid.UUID,
        role: str,
        content: str,
        tool_calls: Optional[str] = None
    ) -> Message:
        """
        Add a message to a conversation.

        Messages are immutable once created (audit trail).

        Args:
            conversation_id: Conversation ID
            user_id: User ID
            role: Message role ("user", "assistant", "system")
            content: Message content text
            tool_calls: Optional JSON string of tool calls (for assistant messages)

        Returns:
            Created Message object
        """
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)

        # Update conversation updated_at timestamp
        conversation = self.get_conversation(conversation_id, user_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            self.session.commit()

        return message

    def list_user_conversations(self, user_id: int, limit: int = 50) -> List[Conversation]:
        """
        List all conversations for a user, ordered by most recent.

        Args:
            user_id: User ID
            limit: Maximum conversations to return (default 50)

        Returns:
            List of Conversation objects ordered by updated_at DESC
        """
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
        )
        conversations = self.session.exec(statement).all()
        return list(conversations)
