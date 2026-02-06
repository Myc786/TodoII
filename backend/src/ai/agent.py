"""AI agent for natural language task management using OpenAI SDK with Cohere."""
import json
from typing import List, Dict, Any
from ..mcp import tools as mcp_tools
from .config import get_openai_client, get_model_name
from .instructions import get_agent_instructions


class ChatAgent:
    """
    AI agent for processing natural language task management commands.

    Uses OpenAI SDK configured with Cohere models via compatibility API.
    Integrates with MCP tools for task operations.
    """

    def __init__(self):
        self.client = get_openai_client()
        self.model = get_model_name()
        self.instructions = get_agent_instructions()

        # Define available tools in OpenAI function calling format
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "User ID from JWT authentication"
                            },
                            "title": {
                                "type": "string",
                                "description": "Task title"
                            },
                            "description": {
                                "type": "string",
                                "description": "Task description (optional)"
                            }
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List user's tasks with optional status filter",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "User ID from JWT authentication"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["all", "pending", "completed"],
                                "description": "Status filter (default: all)"
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "User ID from JWT authentication"
                            },
                            "task_id": {
                                "type": "integer",
                                "description": "Task ID to complete"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update task title or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "User ID from JWT authentication"
                            },
                            "task_id": {
                                "type": "integer",
                                "description": "Task ID to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New task title (optional)"
                            },
                            "description": {
                                "type": "string",
                                "description": "New task description (optional)"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Permanently delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "User ID from JWT authentication"
                            },
                            "task_id": {
                                "type": "integer",
                                "description": "Task ID to delete"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

    def format_message_history(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Convert database messages to OpenAI message format.

        Args:
            messages: List of dicts with role and content

        Returns:
            Formatted messages for OpenAI API
        """
        formatted = [{"role": "system", "content": self.instructions}]

        for msg in messages:
            formatted.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        return formatted

    def execute_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute an MCP tool based on agent's function call.

        Args:
            tool_name: Name of tool to execute
            arguments: Tool arguments from agent

        Returns:
            Tool execution result
        """
        tool_function = getattr(mcp_tools, tool_name, None)
        if not tool_function:
            return {"error": "TOOL_NOT_FOUND", "message": f"Tool {tool_name} not found"}

        try:
            result = tool_function(**arguments)
            return result
        except Exception as e:
            return {"error": "TOOL_EXECUTION_FAILED", "message": str(e)}

    def process_message(self, user_id: str, message: str, history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Process user message with agent and execute tools.

        Implements stateless agent pattern:
        1. Load message history from database
        2. Add new user message
        3. Call agent with tools
        4. Execute tool calls if requested
        5. Get final response from agent
        6. Return response with tool call info

        Args:
            user_id: User ID from JWT
            message: New user message
            history: Previous conversation messages

        Returns:
            Dict with response and tool_calls
        """
        try:
            # Format message history with system instructions
            messages = self.format_message_history(history)

            # Add new user message
            messages.append({"role": "user", "content": message})

            # Call agent with tools
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message
            tool_calls_info = []

            # Check if agent wants to use tools
            if assistant_message.tool_calls:
                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)

                    # Inject user_id into tool arguments
                    arguments["user_id"] = user_id

                    # Execute tool
                    tool_result = self.execute_tool_call(tool_name, arguments)

                    # Store tool call info
                    tool_calls_info.append({
                        "tool": tool_name,
                        "arguments": arguments,
                        "result": tool_result
                    })

                    # Add tool result to conversation
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [{
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "arguments": tool_call.function.arguments
                            }
                        }]
                    })
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    })

                # Get final response after tool execution
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                final_content = final_response.choices[0].message.content

                return {
                    "response": final_content,
                    "tool_calls": tool_calls_info
                }
            else:
                # No tool calls, return direct response
                return {
                    "response": assistant_message.content,
                    "tool_calls": []
                }

        except Exception as e:
            return {
                "response": f"I'm sorry, I encountered an error processing your request. Please try again.",
                "tool_calls": [],
                "error": str(e)
            }
