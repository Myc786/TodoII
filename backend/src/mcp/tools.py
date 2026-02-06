"""MCP tools for task operations.

All tools enforce user_id validation to ensure users can only
operate on their own tasks (security requirement).
"""
import json
from typing import Dict, Any, List
from uuid import UUID
from sqlmodel import Session
from ..services.task_service import TaskService
from ..models.task_schemas import TaskCreate, TaskUpdate, TaskToggle
from ..core.config import get_session


def add_task(user_id: str, title: str, description: str = "") -> Dict[str, Any]:
    """
    Create a new task for the user.

    MCP Tool: add_task
    Security: Validates user_id ownership

    Args:
        user_id: User ID from JWT authentication
        title: Task title extracted from user message
        description: Optional task description

    Returns:
        Dict with task_id, status="created", title, description
    """
    try:
        session = next(get_session())
        user_uuid = UUID(user_id)

        # Create task using existing TaskService
        task_create = TaskCreate(
            title=title,
            description=description if description else None,
            is_completed=False
        )
        task = TaskService.create_task(session, task_create, user_uuid)

        return {
            "task_id": str(task.id),
            "status": "created",
            "title": task.title,
            "description": task.description
        }
    except Exception as e:
        return {
            "error": "CREATION_FAILED",
            "message": f"Failed to create task: {str(e)}"
        }
    finally:
        session.close()


def list_tasks(user_id: str, status: str = "all") -> List[Dict[str, Any]]:
    """
    List user's tasks with optional status filter.

    MCP Tool: list_tasks
    Security: Filters by user_id

    Args:
        user_id: User ID from JWT authentication
        status: Status filter ("all", "pending", "completed")

    Returns:
        List of task dicts with task_id, title, description, status, created_at
    """
    try:
        session = next(get_session())
        user_uuid = UUID(user_id)

        # Get all tasks for user
        tasks = TaskService.get_tasks_by_user_id(session, user_uuid, skip=0, limit=100)

        # Filter by status if requested
        if status == "pending":
            tasks = [t for t in tasks if not t.is_completed]
        elif status == "completed":
            tasks = [t for t in tasks if t.is_completed]

        # Format for agent
        result = []
        for task in tasks:
            result.append({
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "status": "completed" if task.is_completed else "pending",
                "created_at": task.created_at.isoformat() if task.created_at else None
            })

        return result
    except Exception as e:
        return [{
            "error": "LIST_FAILED",
            "message": f"Failed to list tasks: {str(e)}"
        }]
    finally:
        session.close()


def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Mark a task as completed.

    MCP Tool: complete_task
    Security: Validates user_id ownership

    Args:
        user_id: User ID from JWT authentication
        task_id: Task ID to complete

    Returns:
        Dict with task_id, status="completed", title
    """
    try:
        session = next(get_session())
        user_uuid = UUID(user_id)

        # Get task with ownership check
        task = TaskService.get_task_by_id(session, str(task_id), user_uuid)
        if not task:
            return {
                "error": "NOT_FOUND",
                "message": f"Task #{task_id} not found or access denied",
                "task_id": task_id
            }

        # Toggle task to completed
        task_toggle = TaskToggle(is_completed=True)
        updated_task = TaskService.toggle_task_completion(session, str(task.id), user_uuid, task_toggle)

        return {
            "task_id": str(updated_task.id),
            "status": "completed",
            "title": updated_task.title
        }
    except Exception as e:
        return {
            "error": "COMPLETION_FAILED",
            "message": f"Failed to complete task: {str(e)}",
            "task_id": task_id
        }
    finally:
        session.close()


def update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
    """
    Update task title or description.

    MCP Tool: update_task
    Security: Validates user_id ownership

    Args:
        user_id: User ID from JWT authentication
        task_id: Task ID to update
        title: New task title (optional)
        description: New task description (optional)

    Returns:
        Dict with task_id, status="updated", title, description
    """
    try:
        if not title and not description:
            return {
                "error": "VALIDATION",
                "message": "No fields provided for update",
                "task_id": task_id
            }

        session = next(get_session())
        user_uuid = UUID(user_id)

        # Get task with ownership check
        task = TaskService.get_task_by_id(session, str(task_id), user_uuid)
        if not task:
            return {
                "error": "NOT_FOUND",
                "message": f"Task #{task_id} not found or access denied",
                "task_id": task_id
            }

        # Update task
        task_update = TaskUpdate(
            title=title if title else task.title,
            description=description if description is not None else task.description
        )
        updated_task = TaskService.update_task(session, str(task.id), user_uuid, task_update)

        return {
            "task_id": str(updated_task.id),
            "status": "updated",
            "title": updated_task.title,
            "description": updated_task.description
        }
    except Exception as e:
        return {
            "error": "UPDATE_FAILED",
            "message": f"Failed to update task: {str(e)}",
            "task_id": task_id
        }
    finally:
        session.close()


def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Permanently delete a task.

    MCP Tool: delete_task
    Security: Validates user_id ownership

    Args:
        user_id: User ID from JWT authentication
        task_id: Task ID to delete

    Returns:
        Dict with task_id, status="deleted", title
    """
    try:
        session = next(get_session())
        user_uuid = UUID(user_id)

        # Get task with ownership check
        task = TaskService.get_task_by_id(session, str(task_id), user_uuid)
        if not task:
            return {
                "error": "NOT_FOUND",
                "message": f"Task #{task_id} not found or access denied",
                "task_id": task_id
            }

        # Store title before deletion
        task_title = task.title

        # Delete task
        TaskService.delete_task(session, str(task.id), user_uuid)

        return {
            "task_id": str(task_id),
            "status": "deleted",
            "title": task_title
        }
    except Exception as e:
        return {
            "error": "DELETE_FAILED",
            "message": f"Failed to delete task: {str(e)}",
            "task_id": task_id
        }
    finally:
        session.close()
