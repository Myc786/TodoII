"""
Complete Task MCP Tool for Todo Chatbot Extension

This module implements the complete_task MCP tool that allows the AI chatbot
to mark tasks as complete or incomplete for users.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from .base import BaseMCPTask, MCPToolError
from .context_propagation import validate_user_authorization, get_current_user_id
from ..database.session import get_session
from ..services.task_service import TaskService
from ..models.task import Task


class CompleteTaskTool(BaseMCPTask):
    """
    MCP tool for marking tasks as complete/incomplete.
    """

    def __init__(self):
        super().__init__()

    async def validate_input(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input parameters for completing a task.

        Args:
            params: Input parameters for task completion

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

        completed = params.get("completed", True)
        if not isinstance(completed, bool):
            try:
                completed = bool(completed)
            except (ValueError, TypeError):
                raise MCPToolError("Completed must be a boolean value")

        # Version parameter is optional for optimistic locking
        version = params.get("version")
        if version is not None:
            try:
                version = int(version)
                if version < 0:
                    raise MCPToolError("Version must be a non-negative integer")
            except (ValueError, TypeError):
                raise MCPToolError("Version must be a valid integer")

        # Return validated parameters
        validated_params = {
            "taskId": task_id.strip(),
            "completed": completed
        }

        if version is not None:
            validated_params["version"] = version

        return validated_params

    async def execute(self, params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Execute the complete task operation.

        Args:
            params: Validated parameters for task completion
            user_id: ID of the authenticated user

        Returns:
            Updated task data
        """
        task_id = params["taskId"]
        completed = params["completed"]
        version = params.get("version")

        try:
            # Use the existing task service to update the task completion status
            async with get_session() as session:
                task_service = TaskService(session)

                # Update the task completion status
                task = await task_service.update_task_completion(
                    task_id=task_id,
                    user_id=user_id,
                    completed=completed,
                    version=version
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
            self.logger.error(f"Error completing task: {str(e)}")
            raise MCPToolError(f"Failed to complete task: {str(e)}")


# Global instance of the tool
complete_task_tool = CompleteTaskTool()


async def handle_complete_task(params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """
    Handler function for the complete_task MCP tool.

    Args:
        params: Parameters for task completion
        user_id: ID of the authenticated user

    Returns:
        Result of the tool execution
    """
    return await complete_task_tool.validate_and_execute(params, user_id)