"""
Update Task MCP Tool for Todo Chatbot Extension

This module implements the update_task MCP tool that allows the AI chatbot
to update existing tasks for users.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from .base import BaseMCPTask, MCPToolError
from .context_propagation import validate_user_authorization, get_current_user_id
from ..database.session import get_session
from ..services.task_service import TaskService
from ..models.task import Task


class UpdateTaskTool(BaseMCPTask):
    """
    MCP tool for updating tasks.
    """

    def __init__(self):
        super().__init__()

    async def validate_input(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input parameters for updating a task.

        Args:
            params: Input parameters for task update

        Returns:
            Validated parameters

        Raises:
            MCPToolError: If validation fails
        """
        if not isinstance(params, dict):
            raise MCPToolError("Parameters must be a dictionary")

        task_id = params.get("taskId")
        if not task_id or not isinstance(task_id, str) or len(task_id.strip()) == 0:
            raise MCPToolError("Task ID is required and must be a non-empty string")

        # At least one field to update must be provided
        title = params.get("title")
        description = params.get("description")

        if title is None and description is None:
            raise MCPToolError("At least one field (title or description) must be provided for update")

        if title is not None:
            if not isinstance(title, str):
                raise MCPToolError("Title must be a string")
            if len(title.strip()) == 0:
                raise MCPToolError("Title cannot be empty")
            if len(title.strip()) > 255:
                raise MCPToolError("Title must be 255 characters or less")

        if description is not None:
            if not isinstance(description, str):
                raise MCPToolError("Description must be a string")
            if len(description) > 1000:
                raise MCPToolError("Description must be 1000 characters or less")

        # Return validated parameters with cleaned values
        validated_params = {
            "taskId": task_id.strip()
        }

        if title is not None:
            validated_params["title"] = title.strip()
        if description is not None:
            validated_params["description"] = description

        return validated_params

    async def execute(self, params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Execute the update task operation.

        Args:
            params: Validated parameters for task update
            user_id: ID of the authenticated user

        Returns:
            Updated task data
        """
        task_id = params["taskId"]
        title = params.get("title")
        description = params.get("description")

        try:
            # Use the existing task service to update the task
            async with get_session() as session:
                task_service = TaskService(session)

                # Update the task
                task = await task_service.update_task(
                    task_id=task_id,
                    user_id=user_id,
                    title=title,
                    description=description
                )

            # Return the updated task data
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
            self.logger.error(f"Error updating task: {str(e)}")
            raise MCPToolError(f"Failed to update task: {str(e)}")


# Global instance of the tool
update_task_tool = UpdateTaskTool()


async def handle_update_task(params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """
    Handler function for the update_task MCP tool.

    Args:
        params: Parameters for task update
        user_id: ID of the authenticated user

    Returns:
        Result of the tool execution
    """
    return await update_task_tool.validate_and_execute(params, user_id)