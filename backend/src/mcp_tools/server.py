"""
MCP Tools Server Configuration for Todo Chatbot Extension

This module sets up the Model Context Protocol (MCP) server that exposes
various tools for the AI-powered chatbot to interact with the todo system.
"""

import asyncio
import json
from typing import Dict, Any, List
from pydantic import BaseModel

# Import existing services from the todo application
from ..services.task_service import TaskService
from ..database.session import get_session
from ..models.user import User
from ..models.task import Task


class MCPServer:
    """
    Model Context Protocol Server for Todo Chatbot
    """

    def __init__(self):
        self.tools = {}
        self.register_default_tools()

    def register_tool(self, name: str, handler):
        """Register an MCP tool with its handler function."""
        self.tools[name] = handler

    def register_default_tools(self):
        """Register all default todo management tools."""
        self.register_tool("create_task", self.handle_create_task)
        self.register_tool("list_tasks", self.handle_list_tasks)
        self.register_tool("update_task", self.handle_update_task)
        self.register_tool("complete_task", self.handle_complete_task)
        self.register_tool("delete_task", self.handle_delete_task)

    async def call_tool(self, tool_name: str, parameters: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Call an MCP tool with the given parameters and user context.

        Args:
            tool_name: Name of the tool to call
            parameters: Parameters to pass to the tool
            user_id: ID of the authenticated user

        Returns:
            Result of the tool execution
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }

        try:
            # Call the tool handler with user context
            result = await self.tools[tool_name](parameters, user_id)
            return {
                "success": True,
                "data": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def handle_create_task(self, params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Handle task creation requests."""
        title = params.get("title")
        description = params.get("description", "")

        if not title:
            raise ValueError("Title is required for task creation")

        # Use existing task service to create the task
        async with get_session() as session:
            task_service = TaskService(session)
            task = await task_service.create_task(user_id=user_id, title=title, description=description)

        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }

    async def handle_list_tasks(self, params: Dict[str, Any], user_id: str) -> List[Dict[str, Any]]:
        """Handle task listing requests."""
        filter_type = params.get("filter", "all")  # all, active, completed

        async with get_session() as session:
            task_service = TaskService(session)

            if filter_type == "active":
                tasks = await task_service.get_active_tasks(user_id)
            elif filter_type == "completed":
                tasks = await task_service.get_completed_tasks(user_id)
            else:
                tasks = await task_service.get_user_tasks(user_id)

        return [
            {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]

    async def handle_update_task(self, params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Handle task update requests."""
        task_id = params.get("taskId")
        title = params.get("title")
        description = params.get("description")

        if not task_id:
            raise ValueError("Task ID is required for update")

        async with get_session() as session:
            task_service = TaskService(session)
            task = await task_service.update_task(
                task_id=task_id,
                user_id=user_id,
                title=title,
                description=description
            )

        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }

    async def handle_complete_task(self, params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Handle task completion requests."""
        task_id = params.get("taskId")
        completed = params.get("completed", True)
        version = params.get("version")

        if not task_id:
            raise ValueError("Task ID is required for completion")

        async with get_session() as session:
            task_service = TaskService(session)
            task = await task_service.update_task_completion(
                task_id=task_id,
                user_id=user_id,
                completed=completed,
                version=version
            )

        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }

    async def handle_delete_task(self, params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Handle task deletion requests."""
        task_id = params.get("taskId")

        if not task_id:
            raise ValueError("Task ID is required for deletion")

        async with get_session() as session:
            task_service = TaskService(session)
            await task_service.delete_task(task_id=task_id, user_id=user_id)

        return {"message": "Task deleted successfully"}


# Global server instance
mcp_server = MCPServer()


async def run_mcp_server():
    """Run the MCP server (placeholder for actual server implementation)."""
    print("MCP Server initialized with tools:", list(mcp_server.tools.keys()))
    # Actual server implementation would go here
    pass


if __name__ == "__main__":
    asyncio.run(run_mcp_server())