"""Type definitions for MCP tools."""
from typing import Optional, Literal
from pydantic import BaseModel, Field


class TaskToolInput(BaseModel):
    """Input schema for task-related MCP tools."""
    user_id: str = Field(..., description="User ID from JWT authentication")
    title: Optional[str] = Field(None, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    task_id: Optional[int] = Field(None, description="Task ID for operations")
    status: Optional[Literal["all", "pending", "completed"]] = Field(
        "all",
        description="Status filter for list_tasks"
    )


class TaskToolOutput(BaseModel):
    """Output schema for MCP tool responses."""
    task_id: Optional[int] = Field(None, description="Task ID")
    status: str = Field(..., description="Operation status (created, completed, updated, deleted)")
    title: Optional[str] = Field(None, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    error: Optional[str] = Field(None, description="Error message if operation failed")
    message: Optional[str] = Field(None, description="User-friendly message")
