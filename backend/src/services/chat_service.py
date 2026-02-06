"""Chat service for orchestrating AI agent conversations."""
import json
from typing import Dict, Any, Optional
from sqlmodel import Session
from ..services.conversation_service import ConversationService
from ..ai.agent import ChatAgent


class ChatService:
    """
    Service for processing chat messages with AI agent.

    Implements stateless design:
    1. Load/create conversation
    2. Load message history
    3. Process message with agent
    4. Persist messages
    5. Return response
    """

    def __init__(self, session: Session):
        self.session = session
        self.conversation_service = ConversationService(session)
        self.agent = ChatAgent()

    def process_message(
        self,
        user_id: int,
        message: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process user message and return agent response.

        Args:
            user_id: User ID from JWT
            message: User message text
            conversation_id: Optional conversation ID (creates new if None)

        Returns:
            Dict with conversation_id, response, and tool_calls
        """
        try:
            # Step 1: Load or create conversation
            if conversation_id:
                conversation = self.conversation_service.get_conversation(conversation_id, user_id)
                if not conversation:
                    return {
                        "error": "CONVERSATION_NOT_FOUND",
                        "message": "Conversation not found or access denied"
                    }
            else:
                conversation = self.conversation_service.create_conversation(user_id)
                conversation_id = conversation.id

            # Step 2: Load message history (stateless design)
            messages = self.conversation_service.get_conversation_history(conversation_id, user_id)
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            # Step 3: Process message with agent
            agent_result = self.agent.process_message(
                user_id=str(user_id),
                message=message,
                history=history
            )

            # Step 4: Persist user message
            self.conversation_service.add_message(
                conversation_id=conversation_id,
                user_id=user_id,
                role="user",
                content=message
            )

            # Step 5: Persist assistant response
            tool_calls_json = None
            if agent_result.get("tool_calls"):
                tool_calls_json = json.dumps(agent_result["tool_calls"])

            self.conversation_service.add_message(
                conversation_id=conversation_id,
                user_id=user_id,
                role="assistant",
                content=agent_result["response"],
                tool_calls=tool_calls_json
            )

            # Step 6: Return response
            return {
                "conversation_id": conversation_id,
                "response": agent_result["response"],
                "tool_calls": agent_result.get("tool_calls", [])
            }

        except Exception as e:
            return {
                "error": "PROCESSING_FAILED",
                "message": f"Failed to process message: {str(e)}"
            }
