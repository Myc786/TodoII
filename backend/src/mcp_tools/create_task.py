"""
Create Task MCP Tool for Todo Chatbot Extension

This module implements the create_task MCP tool that allows the AI chatbot
to create new tasks for users.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from .base import BaseMCPTask, MCPToolError
from .context_propagation import validate_user_authorization, get_current_user_id
from ..database.session import get_session
from ..services.task_service import TaskService
from ..models.task import Task


class CreateTaskTool(BaseMCPTask):
    """
    MCP tool for creating new tasks.
    """

    def __init__(self):
        super().__init__()

    async def validate_input(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input parameters for creating a task.

        Args:
            params: Input parameters for task creation

        Returns:
            Validated parameters

        Raises:
            MCPToolError: If validation fails
        """
        if not isinstance(params, dict):
            raise MCPToolError("Parameters must be a dictionary")

        title = params.get("title")
        if not title or not isinstance(title, str) or len(title.strip()) == 0:
            raise MCPToolError("Title is required and must be a non-empty string")

        if len(title.strip()) > 255:
            raise MCPToolError("Title must be 255 characters or less")

        description = params.get("description", "")
        if not isinstance(description, str):
            raise MCPToolError("Description must be a string")

        if len(description) > 1000:
            raise MCPToolError("Description must be 1000 characters or less")

        # Return validated parameters with cleaned values
        return {
            "title": title.strip(),
            "description": description.strip()
        }

    async def execute(self, params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Execute the create task operation.

        Args:
            params: Validated parameters for task creation
            user_id: ID of the authenticated user

        Returns:
            Created task data
        """
        title = params["title"]
        description = params["description"]

        try:
            # Use the existing task service to create the task
            async with get_session() as session:
                task_service = TaskService(session)

                # Create the task
                task = await task_service.create_task(
                    user_id=user_id,
                    title=title,
                    description=description if description else None
                )

            # Return the created task data
            return {
                "id": str(task.id),
                "title": task.title,
                "description": task.description or "",
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "version": task.version
            }

        except Exception as e:
            self.logger.error(f"Error creating task: {str(e)}")
            raise MCPToolError(f"Failed to create task: {str(e)}")


# Global instance of the tool
create_task_tool = CreateTaskTool()


async def handle_create_task(params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """
    Handler function for the create_task MCP tool.

    Args:
        params: Parameters for task creation
        user_id: ID of the authenticated user

    Returns:
        Result of the tool execution
    """
    return await create_task_tool.validate_and_execute(params, user_id)