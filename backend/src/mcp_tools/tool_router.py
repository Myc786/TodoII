"""
MCP Tool Router for Todo Chatbot Extension

This module provides a unified interface to all MCP tools and handles
routing requests to the appropriate tool.
"""

from typing import Dict, Any, Optional
from enum import Enum
import logging

from .create_task import handle_create_task
from .list_tasks import handle_list_tasks
from .update_task import handle_update_task
from .complete_task import handle_complete_task
from .delete_task import handle_delete_task
from .context_propagation import set_user_context, get_current_user_id


class ToolType(Enum):
    """Enumeration of available MCP tools."""
    CREATE_TASK = "create_task"
    LIST_TASKS = "list_tasks"
    UPDATE_TASK = "update_task"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"


class MCPTaskRouter:
    """
    Router that directs MCP tool requests to the appropriate handler.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.handlers = {
            ToolType.CREATE_TASK.value: handle_create_task,
            ToolType.LIST_TASKS.value: handle_list_tasks,
            ToolType.UPDATE_TASK.value: handle_update_task,
            ToolType.COMPLETE_TASK.value: handle_complete_task,
            ToolType.DELETE_TASK.value: handle_delete_task
        }

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any], token: str) -> Dict[str, Any]:
        """
        Execute an MCP tool with the given parameters and authentication token.

        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool
            token: JWT authentication token

        Returns:
            Result of the tool execution
        """
        # Validate the tool name
        if tool_name not in self.handlers:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(self.handlers.keys())
            }

        # Set user context based on the token
        user_authenticated = await set_user_context(token)
        if not user_authenticated:
            return {
                "success": False,
                "error": "Authentication failed",
                "message": "Invalid or expired token"
            }

        # Get the user ID from context
        user_id = get_current_user_id()
        if not user_id:
            return {
                "success": False,
                "error": "User context not found",
                "message": "Unable to determine authenticated user"
            }

        try:
            # Get the handler function
            handler = self.handlers[tool_name]

            # Execute the tool with user context
            result = await handler(parameters, user_id)

            # Format the response
            return {
                "success": True,
                "data": result
            }

        except Exception as e:
            self.logger.error(f"Error executing tool '{tool_name}': {str(e)}")
            return {
                "success": False,
                "error": f"Tool execution failed: {str(e)}"
            }

    def get_available_tools(self) -> Dict[str, str]:
        """
        Get a list of available tools and their descriptions.

        Returns:
            Dictionary of available tools with descriptions
        """
        return {
            ToolType.CREATE_TASK.value: "Create a new task",
            ToolType.LIST_TASKS.value: "List existing tasks",
            ToolType.UPDATE_TASK.value: "Update an existing task",
            ToolType.COMPLETE_TASK.value: "Mark a task as complete/incomplete",
            ToolType.DELETE_TASK.value: "Delete an existing task"
        }

    async def validate_tool_parameters(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate parameters for a specific tool without executing it.

        Args:
            tool_name: Name of the tool to validate parameters for
            parameters: Parameters to validate

        Returns:
            Validation result
        """
        # This would normally call the specific tool's validate_input method
        # For now, we'll return a generic response
        try:
            # Import the specific tool class to call its validation
            if tool_name == ToolType.CREATE_TASK.value:
                from .create_task import create_task_tool
                validated_params = await create_task_tool.validate_input(parameters)
            elif tool_name == ToolType.LIST_TASKS.value:
                from .list_tasks import list_tasks_tool
                validated_params = await list_tasks_tool.validate_input(parameters)
            elif tool_name == ToolType.UPDATE_TASK.value:
                from .update_task import update_task_tool
                validated_params = await update_task_tool.validate_input(parameters)
            elif tool_name == ToolType.COMPLETE_TASK.value:
                from .complete_task import complete_task_tool
                validated_params = await complete_task_tool.validate_input(parameters)
            elif tool_name == ToolType.DELETE_TASK.value:
                from .delete_task import delete_task_tool
                validated_params = await delete_task_tool.validate_input(parameters)
            else:
                return {
                    "valid": False,
                    "error": f"Tool '{tool_name}' not found"
                }

            return {
                "valid": True,
                "parameters": validated_params,
                "message": "Parameters are valid"
            }

        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "message": "Parameter validation failed"
            }


# Global instance of the router
tool_router = MCPTaskRouter()


async def call_mcp_tool(tool_name: str, parameters: Dict[str, Any], token: str) -> Dict[str, Any]:
    """
    Unified function to call any MCP tool.

    Args:
        tool_name: Name of the tool to call
        parameters: Parameters for the tool
        token: Authentication token

    Returns:
        Result of the tool call
    """
    return await tool_router.execute_tool(tool_name, parameters, token)