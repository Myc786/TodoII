"""
Delete Task MCP Tool for Todo Chatbot Extension

This module implements the delete_task MCP tool that allows the AI chatbot
to delete tasks for users.
"""

from typing import Dict, Any
from datetime import datetime

from .base import BaseMCPTask, MCPToolError
from .context_propagation import validate_user_authorization, get_current_user_id
from ..database.session import get_session
from ..services.task_service import TaskService
from ..models.task import Task


class DeleteTaskTool(BaseMCPTask):
    """
    MCP tool for deleting tasks.
    """

    def __init__(self):
        super().__init__()

    async def validate_input(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input parameters for deleting a task.

        Args:
            params: Input parameters for task deletion

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

        # Return validated parameters
        return {
            "taskId": task_id.strip()
        }

    async def execute(self, params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Execute the delete task operation.

        Args:
            params: Validated parameters for task deletion
            user_id: ID of the authenticated user

        Returns:
            Result of the deletion operation
        """
        task_id = params["taskId"]

        try:
            # Use the existing task service to delete the task
            async with get_session() as session:
                task_service = TaskService(session)

                # Delete the task
                await task_service.delete_task(task_id=task_id, user_id=user_id)

            # Return success result
            return {
                "success": True,
                "message": "Task deleted successfully",
                "taskId": task_id
            }

        except Exception as e:
            self.logger.error(f"Error deleting task: {str(e)}")
            raise MCPToolError(f"Failed to delete task: {str(e)}")


# Global instance of the tool
delete_task_tool = DeleteTaskTool()


async def handle_delete_task(params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """
    Handler function for the delete_task MCP tool.

    Args:
        params: Parameters for task deletion
        user_id: ID of the authenticated user

    Returns:
        Result of the tool execution
    """
    return await delete_task_tool.validate_and_execute(params, user_id)