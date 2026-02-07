"""Pydantic schemas for chat API requests and responses."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    conversation_id: Optional[int] = Field(None, description="Conversation ID for resuming chat (optional for new conversation)")
    message: str = Field(..., min_length=1, max_length=1000, description="User message text")


class ToolCallInfo(BaseModel):
    """Information about a tool call executed by the agent."""
    tool: str = Field(..., description="Tool name")
    arguments: Dict[str, Any] = Field(..., description="Tool arguments")
    result: Dict[str, Any] = Field(..., description="Tool execution result")


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    conversation_id: int = Field(..., description="Conversation ID")
    response: str = Field(..., description="Assistant response message")
    tool_calls: List[ToolCallInfo] = Field(default_factory=list, description="List of tools executed")
