"""
Chat History Manager for Todo Chatbot Extension

This module handles the preservation and management of chat history
during user sessions with the AI chatbot.
"""

import asyncio
import json
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from sqlmodel import select
import uuid

from ..database.session import get_session
from ..models.chat_message import ChatMessage, ChatMessageCreate, ChatSession, ChatSessionCreate
from .session_manager import session_manager


class ChatHistoryManager:
    """
    Manages chat history for user sessions with the AI chatbot.
    """

    def __init__(self):
        self.memory_limit = 50  # Limit the number of messages kept in memory per session
        self.preserved_sessions = {}  # In-memory cache of recent sessions

    async def save_message_to_history(
        self,
        session_id: str,
        user_id: str,
        content: str,
        sender: str,
        intent: Optional[str] = None,
        tool_call: Optional[Dict[str, Any]] = None
    ) -> Optional[ChatMessage]:
        """
        Save a message to the chat history.

        Args:
            session_id: ID of the chat session
            user_id: ID of the user sending the message
            content: Content of the message
            sender: Who sent the message ('user' or 'ai')
            intent: Recognized intent of the message (optional)
            tool_call: Details of any tool call made (optional)

        Returns:
            Saved ChatMessage object or None if saving failed
        """
        try:
            async with get_session() as db_session:
                # Create a new chat message
                chat_message = ChatMessageCreate(
                    content=content,
                    sender=sender,
                    session_id=session_id,
                    user_id=user_id,
                    intent=intent,
                    tool_call=tool_call
                )

                # Add to database
                db_chat_message = ChatMessage.model_validate(chat_message)
                db_session.add(db_chat_message)
                await db_session.commit()
                await db_session.refresh(db_chat_message)

                # Also add to the in-memory session if it exists
                session = await session_manager.get_session(session_id)
                if session:
                    message_dict = {
                        "id": str(db_chat_message.id),
                        "content": content,
                        "sender": sender,
                        "timestamp": datetime.utcnow(),
                        "intent": intent,
                        "tool_call": tool_call
                    }
                    session.add_message(message_dict)

                return db_chat_message

        except Exception as e:
            print(f"Error saving message to history: {e}")
            return None

    async def get_session_history(
        self,
        session_id: str,
        limit: Optional[int] = None,
        include_ai_messages: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Retrieve chat history for a specific session.

        Args:
            session_id: ID of the session to retrieve history for
            limit: Maximum number of messages to return (None for all)
            include_ai_messages: Whether to include AI messages in the result

        Returns:
            List of message dictionaries
        """
        try:
            # First, try to get from the session manager in memory
            session = await session_manager.get_session(session_id)
            if session:
                messages = session.messages
                if not include_ai_messages:
                    messages = [msg for msg in messages if msg.get('sender') != 'ai']
                if limit:
                    messages = messages[-limit:]
                return messages

            # If not in memory, fetch from database
            async with get_session() as db_session:
                statement = select(ChatMessage).where(
                    ChatMessage.session_id == session_id
                ).order_by(ChatMessage.timestamp.asc())

                if not include_ai_messages:
                    statement = statement.where(ChatMessage.sender != "ai")

                if limit:
                    statement = statement.limit(limit)

                results = await db_session.exec(statement)
                messages = results.all()

                # Convert to dictionaries
                message_dicts = []
                for msg in messages:
                    message_dicts.append({
                        "id": msg.id,
                        "content": msg.content,
                        "sender": msg.sender,
                        "timestamp": msg.timestamp,
                        "intent": msg.intent,
                        "tool_call": msg.tool_call
                    })

                return message_dicts

        except Exception as e:
            print(f"Error retrieving session history: {e}")
            return []

    async def get_user_conversation_history(
        self,
        user_id: str,
        session_count: int = 5,
        messages_per_session: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversation history across multiple sessions for a user.

        Args:
            user_id: ID of the user to retrieve history for
            session_count: Number of recent sessions to include
            messages_per_session: Number of recent messages per session

        Returns:
            List of conversation histories grouped by session
        """
        try:
            async with get_session() as db_session:
                # Get recent sessions for the user
                session_statement = select(ChatSession).where(
                    ChatSession.user_id == user_id
                ).order_by(ChatSession.last_activity_at.desc()).limit(session_count)

                session_results = await db_session.exec(session_statement)
                sessions = session_results.all()

                conversation_history = []
                for session in sessions:
                    # Get messages for this session
                    message_statement = select(ChatMessage).where(
                        ChatMessage.session_id == session.id
                    ).order_by(ChatMessage.timestamp.desc()).limit(messages_per_session)

                    message_results = await db_session.exec(message_statement)
                    messages = message_results.all()

                    session_history = {
                        "session_id": session.id,
                        "created_at": session.created_at,
                        "last_activity": session.last_activity_at,
                        "messages": []
                    }

                    for msg in reversed(messages):  # Reverse to get chronological order
                        session_history["messages"].append({
                            "id": msg.id,
                            "content": msg.content,
                            "sender": msg.sender,
                            "timestamp": msg.timestamp,
                            "intent": msg.intent,
                            "tool_call": msg.tool_call
                        })

                    conversation_history.append(session_history)

                return conversation_history

        except Exception as e:
            print(f"Error retrieving user conversation history: {e}")
            return []

    async def clear_session_history(self, session_id: str) -> bool:
        """
        Clear all messages from a specific session.

        Args:
            session_id: ID of the session to clear

        Returns:
            True if successful, False otherwise
        """
        try:
            # Remove from in-memory session if it exists
            session = await session_manager.get_session(session_id)
            if session:
                session.messages.clear()

            # Remove from database
            async with get_session() as db_session:
                statement = select(ChatMessage).where(ChatMessage.session_id == session_id)
                results = await db_session.exec(statement)
                messages = results.all()

                for msg in messages:
                    await db_session.delete(msg)

                await db_session.commit()
                return True

        except Exception as e:
            print(f"Error clearing session history: {e}")
            return False

    async def trim_session_history(self, session_id: str, keep_count: int = 20) -> bool:
        """
        Trim session history to keep only the most recent messages.

        Args:
            session_id: ID of the session to trim
            keep_count: Number of recent messages to keep

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get all messages for the session
            all_messages = await self.get_session_history(session_id, include_ai_messages=True)

            if len(all_messages) <= keep_count:
                return True  # Nothing to trim

            # Identify messages to delete (keep only the most recent)
            messages_to_delete = all_messages[:len(all_messages) - keep_count]

            # Remove from database
            async with get_session() as db_session:
                for msg_info in messages_to_delete:
                    # Delete by ID
                    statement = select(ChatMessage).where(ChatMessage.id == msg_info["id"])
                    result = await db_session.exec(statement)
                    msg = result.first()
                    if msg:
                        await db_session.delete(msg)

                await db_session.commit()

                # Also remove from in-memory session if it exists
                session = await session_manager.get_session(session_id)
                if session:
                    # Keep only the most recent messages in memory
                    session.messages = all_messages[-keep_count:]

                return True

        except Exception as e:
            print(f"Error trimming session history: {e}")
            return False

    async def export_session_history(self, session_id: str, format_type: str = "json") -> Optional[Union[str, bytes]]:
        """
        Export session history in a specific format.

        Args:
            session_id: ID of the session to export
            format_type: Format to export in ('json', 'text')

        Returns:
            Exported history as string or bytes, or None if failed
        """
        try:
            messages = await self.get_session_history(session_id, include_ai_messages=True)

            if format_type.lower() == "json":
                return json.dumps(messages, default=str, indent=2)
            elif format_type.lower() == "text":
                text_content = ""
                for msg in messages:
                    sender = "You" if msg["sender"] == "user" else "AI Assistant"
                    timestamp = msg["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                    text_content += f"[{timestamp}] {sender}: {msg['content']}\n"
                return text_content
            else:
                raise ValueError(f"Unsupported format: {format_type}")

        except Exception as e:
            print(f"Error exporting session history: {e}")
            return None

    async def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Get a summary of a chat session.

        Args:
            session_id: ID of the session to summarize

        Returns:
            Dictionary containing session summary information
        """
        try:
            # Try to get from session manager first
            session = await session_manager.get_session(session_id)
            if session:
                return {
                    "session_id": session.id,
                    "user_id": session.user_id,
                    "created_at": session.created_at,
                    "last_activity_at": session.last_activity_at,
                    "status": session.status.value,
                    "message_count": len(session.messages),
                    "metadata": session.metadata
                }

            # If not in memory, fetch from database
            async with get_session() as db_session:
                statement = select(ChatSession).where(ChatSession.id == session_id)
                result = await db_session.exec(statement)
                db_session_obj = result.first()

                if not db_session_obj:
                    return {}

                # Count messages for this session
                message_statement = select(ChatMessage).where(ChatMessage.session_id == session_id)
                message_result = await db_session.exec(message_statement)
                message_count = len(message_result.all())

                return {
                    "session_id": db_session_obj.id,
                    "user_id": db_session_obj.user_id,
                    "created_at": db_session_obj.created_at,
                    "last_activity_at": db_session_obj.last_activity_at,
                    "status": "active" if db_session_obj.is_active else "inactive",
                    "message_count": message_count,
                    "metadata": {}  # Metadata not stored in DB in our model
                }

        except Exception as e:
            print(f"Error getting session summary: {e}")
            return {}


# Global instance of the chat history manager
chat_history_manager = ChatHistoryManager()