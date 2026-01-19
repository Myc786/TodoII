"""
List Tasks MCP Tool for Todo Chatbot Extension

This module implements the list_tasks MCP tool that allows the AI chatbot
to retrieve tasks for users.
"""

from typing import Dict, Any, List
from datetime import datetime

from .base import BaseMCPTask, MCPToolError
from .context_propagation import validate_user_authorization, get_current_user_id
from ..database.session import get_session
from ..services.task_service import TaskService
from ..models.task import Task


class ListTasksTool(BaseMCPTask):
    """
    MCP tool for listing tasks.
    """

    def __init__(self):
        super().__init__()

    async def validate_input(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input parameters for listing tasks.

        Args:
            params: Input parameters for task listing

        Returns:
            Validated parameters

        Raises:
            MCPToolError: If validation fails
        """
        if not isinstance(params, dict):
            raise MCPToolError("Parameters must be a dictionary")

        # Get the filter parameter (optional)
        filter_param = params.get("filter", "all")
        if filter_param not in ["all", "active", "completed"]:
            raise MCPToolError("Filter must be 'all', 'active', or 'completed'")

        # Get the limit parameter (optional)
        limit = params.get("limit")
        if limit is not None:
            try:
                limit = int(limit)
                if limit <= 0:
                    raise MCPToolError("Limit must be a positive integer")
            except (ValueError, TypeError):
                raise MCPToolError("Limit must be a valid integer")

        # Get the offset parameter (optional)
        offset = params.get("offset")
        if offset is not None:
            try:
                offset = int(offset)
                if offset < 0:
                    raise MCPToolError("Offset must be a non-negative integer")
            except (ValueError, TypeError):
                raise MCPToolError("Offset must be a valid integer")

        # Return validated parameters
        validated_params = {
            "filter": filter_param,
            "limit": limit,
            "offset": offset
        }

        # Remove None values
        validated_params = {k: v for k, v in validated_params.items() if v is not None}
        if "filter" not in validated_params:
            validated_params["filter"] = "all"

        return validated_params

    async def execute(self, params: Dict[str, Any], user_id: str) -> List[Dict[str, Any]]:
        """
        Execute the list tasks operation.

        Args:
            params: Validated parameters for task listing
            user_id: ID of the authenticated user

        Returns:
            List of task data
        """
        try:
            # Use the existing task service to get tasks
            async with get_session() as session:
                task_service = TaskService(session)

                # Determine which tasks to retrieve based on filter
                filter_type = params.get("filter", "all")

                if filter_type == "active":
                    tasks = await task_service.get_active_tasks(user_id)
                elif filter_type == "completed":
                    tasks = await task_service.get_completed_tasks(user_id)
                else:  # "all"
                    tasks = await task_service.get_user_tasks(user_id)

                # Apply limit and offset if specified
                limit = params.get("limit")
                offset = params.get("offset", 0)

                if limit is not None:
                    tasks = tasks[offset:offset + limit]
                else:
                    tasks = tasks[offset:]

            # Convert tasks to dictionaries
            tasks_data = []
            for task in tasks:
                tasks_data.append({
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description or "",
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                    "version": task.version
                })

            return tasks_data

        except Exception as e:
            self.logger.error(f"Error listing tasks: {str(e)}")
            raise MCPToolError(f"Failed to list tasks: {str(e)}")


# Global instance of the tool
list_tasks_tool = ListTasksTool()


async def handle_list_tasks(params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """
    Handler function for the list_tasks MCP tool.

    Args:
        params: Parameters for task listing
        user_id: ID of the authenticated user

    Returns:
        Result of the tool execution
    """
    return await list_tasks_tool.validate_and_execute(params, user_id)