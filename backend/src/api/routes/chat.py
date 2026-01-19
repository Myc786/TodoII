from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from ..deps import get_current_user
from ...models.user import User
import logging
from ...core import logging_config

# Import MCP tools
from ...mcp_tools.create_task import handle_create_task
from ...mcp_tools.list_tasks import handle_list_tasks
from ...mcp_tools.complete_task import handle_complete_task
from ...mcp_tools.delete_task import handle_delete_task

router = APIRouter()

# Pydantic models for chat requests and responses
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    intent: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    success: bool
    action: Optional[str] = None
    task_id: Optional[str] = None

@router.post("/chat", response_model=ChatResponse)
async def process_chat_command(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """
    Process natural language commands from the chatbot using MCP tools.

    Args:
        chat_request: The chat message and related data
        current_user: The authenticated user making the request

    Returns:
        ChatResponse: The response to the user's message
    """
    logger = logging_config.get_logger(__name__)
    logger.info(f"Processing chat command for user {current_user.email}: {chat_request.message}")

    try:
        # Process the natural language command
        message_lower = chat_request.message.lower()

        # Handle different types of commands using MCP tools
        if any(word in message_lower for word in ['create', 'add', 'make', 'new']):
            if any(word in message_lower for word in ['task', 'todo']):
                # Extract task description from message
                task_desc = message_lower.replace('create', '').replace('add', '').replace('make', '').replace('new', '').replace('task', '').replace('todo', '').strip()

                if not task_desc:
                    task_desc = "Task created via chatbot"

                # Use MCP tool to create the task
                params = {
                    "title": task_desc,
                    "description": f"Created via chatbot: {chat_request.message}"
                }

                # Execute the create_task MCP tool
                result = await handle_create_task(params, str(current_user.id))

                if result.get("success"):
                    task_data = result.get("data", {})
                    response_message = f"I've created a task for you: '{task_data.get('title', task_desc)}'."
                    action = "task_created"
                    task_id = task_data.get("id")
                else:
                    error_details = result.get("details", "Unknown error")
                    response_message = f"Sorry, I couldn't create the task. Error: {error_details}"
                    action = "task_creation_failed"
                    task_id = None

                return ChatResponse(
                    message=response_message,
                    success=result.get("success", False),
                    action=action,
                    task_id=task_id
                )

        elif any(word in message_lower for word in ['complete', 'done', 'finish', 'mark']):
            if any(word in message_lower for word in ['task', 'todo']):
                # For now, we'll use a simple approach to identify which task to complete
                # In a real implementation, we'd use more sophisticated NLP to identify the specific task
                # For demonstration, let's get all tasks and pick the most recent one
                params = {"filter": "all"}
                result = await handle_list_tasks(params, str(current_user.id))

                if result.get("success"):
                    tasks = result.get("data", [])
                    if tasks:
                        # Pick the most recent task for demo purposes
                        most_recent_task = max(tasks, key=lambda x: x.get("created_at", ""))
                        task_id = most_recent_task.get("id")

                        # Mark the task as complete
                        complete_params = {
                            "taskId": task_id,
                            "completed": True
                        }

                        complete_result = await handle_complete_task(complete_params, str(current_user.id))

                        if complete_result.get("success"):
                            response_message = f"I've marked the task '{most_recent_task.get('title')}' as completed."
                            action = "task_completed"
                            task_id = most_recent_task.get("id")
                        else:
                            error_details = complete_result.get("details", "Unknown error")
                            response_message = f"Sorry, I couldn't complete the task. Error: {error_details}"
                            action = "task_completion_failed"
                            task_id = None
                    else:
                        response_message = "You don't have any tasks to complete."
                        action = "no_tasks_found"
                        task_id = None
                else:
                    error_details = result.get("details", "Unknown error")
                    response_message = f"Sorry, I couldn't retrieve your tasks. Error: {error_details}"
                    action = "task_retrieval_failed"
                    task_id = None

                return ChatResponse(
                    message=response_message,
                    success=result.get("success", False) if 'result' in locals() else False,
                    action=action,
                    task_id=task_id
                )

        elif any(word in message_lower for word in ['delete', 'remove', 'cancel']):
            if any(word in message_lower for word in ['task', 'todo']):
                # Get all tasks to identify which one to delete
                params = {"filter": "all"}
                result = await handle_list_tasks(params, str(current_user.id))

                if result.get("success"):
                    tasks = result.get("data", [])
                    if tasks:
                        # Pick the most recent task for demo purposes
                        most_recent_task = max(tasks, key=lambda x: x.get("created_at", ""))
                        task_id = most_recent_task.get("id")

                        # Delete the task
                        delete_params = {
                            "taskId": task_id
                        }

                        delete_result = await handle_delete_task(delete_params, str(current_user.id))

                        if delete_result.get("success"):
                            response_message = f"I've deleted the task '{most_recent_task.get('title')}'."
                            action = "task_deleted"
                            task_id = most_recent_task.get("id")
                        else:
                            error_details = delete_result.get("details", "Unknown error")
                            response_message = f"Sorry, I couldn't delete the task. Error: {error_details}"
                            action = "task_deletion_failed"
                            task_id = None
                    else:
                        response_message = "You don't have any tasks to delete."
                        action = "no_tasks_found"
                        task_id = None
                else:
                    error_details = result.get("details", "Unknown error")
                    response_message = f"Sorry, I couldn't retrieve your tasks. Error: {error_details}"
                    action = "task_retrieval_failed"
                    task_id = None

                return ChatResponse(
                    message=response_message,
                    success=result.get("success", False) if 'result' in locals() else False,
                    action=action,
                    task_id=task_id
                )

        elif any(word in message_lower for word in ['list', 'show', 'display', 'view']):
            if any(word in message_lower for word in ['task', 'todo']):
                # Determine the filter based on the message
                filter_type = "all"
                if "completed" in message_lower:
                    filter_type = "completed"
                elif "active" in message_lower or "incomplete" in message_lower:
                    filter_type = "active"

                params = {"filter": filter_type}
                result = await handle_list_tasks(params, str(current_user.id))

                if result.get("success"):
                    tasks = result.get("data", [])
                    if tasks:
                        task_titles = [task.get("title") for task in tasks[:5]]  # Limit to first 5 tasks
                        tasks_str = ", ".join(task_titles)
                        response_message = f"Here are your {filter_type} tasks: {tasks_str}."
                        action = "task_listed"
                    else:
                        response_message = f"You don't have any {filter_type} tasks."
                        action = "no_tasks_found"
                else:
                    error_details = result.get("details", "Unknown error")
                    response_message = f"Sorry, I couldn't retrieve your tasks. Error: {error_details}"
                    action = "task_retrieval_failed"

                return ChatResponse(
                    message=response_message,
                    success=result.get("success", False),
                    action=action
                )

        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'greet']):
            response_message = "Hello! I'm your AI Todo Assistant. You can ask me to create, complete, or manage your tasks using natural language."
            action = "greeting"

            return ChatResponse(
                message=response_message,
                success=True,
                action=action
            )

        else:
            # Default response for unrecognized commands
            response_message = f"I received your message: '{chat_request.message}'. I can help you manage your tasks. Try commands like 'Create a task to buy groceries' or 'Show my tasks'."
            action = "unrecognized_command"

            return ChatResponse(
                message=response_message,
                success=True,
                action=action
            )

    except Exception as e:
        logger.error(f"Error processing chat command: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )