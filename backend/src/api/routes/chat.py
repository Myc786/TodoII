"""Chat API routes for AI chatbot."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated
from ...core.config import get_session
from ...core.security import get_current_user_id
from ...models.chat_schemas import ChatRequest, ChatResponse
from ...services.chat_service import ChatService

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: int,
    request: ChatRequest,
    session: Annotated[Session, Depends(get_session)],
    authenticated_user_id: Annotated[int, Depends(get_current_user_id)]
):
    """
    Process chat message with AI agent.

    Stateless endpoint that:
    1. Authenticates user via JWT
    2. Validates user_id matches authenticated user
    3. Loads conversation history (or creates new)
    4. Processes message with AI agent
    5. Persists conversation
    6. Returns response

    Args:
        user_id: User ID from path (must match JWT)
        request: Chat request with message and optional conversation_id
        session: Database session
        authenticated_user_id: User ID from JWT token

    Returns:
        ChatResponse with conversation_id, response, and tool_calls

    Raises:
        HTTPException: 400, 401, 403, 500 errors
    """
    # Validate user_id matches authenticated user (security check)
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID mismatch: cannot access other user's conversations"
        )

    # Validate request
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )

    try:
        # Process message with ChatService
        chat_service = ChatService(session)
        result = chat_service.process_message(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id
        )

        # Check for errors
        if "error" in result:
            if result["error"] == "CONVERSATION_NOT_FOUND":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=result.get("message", "Conversation not found")
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=result.get("message", "Failed to process message")
                )

        return ChatResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI service temporarily unavailable. Please try again or use the traditional task interface."
        )
