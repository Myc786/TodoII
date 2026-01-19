"""
Command Mapper for Todo Chatbot Extension

This module maps natural language commands to appropriate MCP tools
based on intent recognition.
"""

from typing import Dict, Any, Optional
from enum import Enum

from .intent_recognizer import IntentRecognizer, IntentRecognitionResult, IntentType
from .tool_router import call_mcp_tool
from .fallback_handler import fallback_handler, FallbackType


class CommandMapper:
    """
    Maps natural language commands to appropriate MCP tools based on intent recognition.
    """

    def __init__(self):
        self.intent_recognizer = IntentRecognizer()

    async def process_command(self, user_input: str, token: str) -> Dict[str, Any]:
        """
        Process a natural language command and execute the appropriate MCP tool.

        Args:
            user_input: Natural language command from the user
            token: Authentication token for the user

        Returns:
            Result of the command processing
        """
        # Recognize the intent from user input
        intent_result = await self.intent_recognizer.recognize_intent(user_input)

        # Map the recognized intent to the appropriate MCP tool
        tool_name = self._map_intent_to_tool(intent_result.intent)

        if tool_name is None:
            # Handle unknown intents with fallback response
            fallback_response = await fallback_handler.get_fallback_response(
                FallbackType.UNKNOWN_COMMAND,
                user_input
            )
            return {
                "success": False,
                "error": "Unknown command",
                "message": fallback_response,
                "original_input": user_input
            }

        # Transform the recognized parameters to match MCP tool expectations
        tool_params = await self._transform_parameters(intent_result.intent, intent_result.parameters)

        # Execute the appropriate MCP tool
        result = await call_mcp_tool(tool_name, tool_params, token)

        # Enhance the result with additional context
        result["intent"] = intent_result.intent.value
        result["confidence"] = intent_result.confidence
        result["original_input"] = user_input

        return result

    def _map_intent_to_tool(self, intent_type: IntentType) -> Optional[str]:
        """
        Map an intent type to the corresponding MCP tool name.

        Args:
            intent_type: The recognized intent type

        Returns:
            Corresponding MCP tool name or None if no mapping exists
        """
        intent_to_tool_map = {
            IntentType.CREATE_TASK: "create_task",
            IntentType.LIST_TASKS: "list_tasks",
            IntentType.UPDATE_TASK: "update_task",
            IntentType.COMPLETE_TASK: "complete_task",
            IntentType.DELETE_TASK: "delete_task",
            IntentType.QUERY_STATUS: "list_tasks",  # Query status maps to list_tasks with filters
            IntentType.UNKNOWN: None
        }

        return intent_to_tool_map.get(intent_type)

    async def _transform_parameters(self, intent_type: IntentType, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform recognized parameters to match MCP tool expectations.

        Args:
            intent_type: The recognized intent type
            parameters: Recognized parameters from the intent

        Returns:
            Transformed parameters for the MCP tool
        """
        if intent_type == IntentType.CREATE_TASK:
            # Transform parameters for create_task tool
            transformed = {}
            if "title" in parameters:
                transformed["title"] = parameters["title"]
            if "description" in parameters:
                transformed["description"] = parameters["description"]
            return transformed

        elif intent_type == IntentType.LIST_TASKS:
            # Transform parameters for list_tasks tool
            transformed = {}
            if "filter" in parameters:
                transformed["filter"] = parameters["filter"]
            if "limit" in parameters:
                transformed["limit"] = parameters["limit"]
            if "offset" in parameters:
                transformed["offset"] = parameters["offset"]
            return transformed

        elif intent_type == IntentType.COMPLETE_TASK:
            # Transform parameters for complete_task tool
            transformed = {}
            if "taskId" in parameters:
                transformed["taskId"] = parameters["taskId"]
            elif "taskName" in parameters:
                # Need to resolve task name to ID - this would require a lookup
                # For now, we'll return a placeholder that the tool will need to handle
                transformed["taskName"] = parameters["taskName"]

            # Default to marking as completed unless specified otherwise
            transformed["completed"] = parameters.get("completed", True)

            if "version" in parameters:
                transformed["version"] = parameters["version"]
            return transformed

        elif intent_type == IntentType.DELETE_TASK:
            # Transform parameters for delete_task tool
            transformed = {}
            if "taskId" in parameters:
                transformed["taskId"] = parameters["taskId"]
            elif "taskName" in parameters:
                # Need to resolve task name to ID
                transformed["taskName"] = parameters["taskName"]
            return transformed

        elif intent_type == IntentType.UPDATE_TASK:
            # Transform parameters for update_task tool
            transformed = {}
            if "taskId" in parameters:
                transformed["taskId"] = parameters["taskId"]
            if "title" in parameters:
                transformed["title"] = parameters["title"]
            if "description" in parameters:
                transformed["description"] = parameters["description"]
            return transformed

        elif intent_type == IntentType.QUERY_STATUS:
            # Transform parameters for list_tasks tool with status filters
            transformed = {"filter": parameters.get("filter", "all")}
            if "limit" in parameters:
                transformed["limit"] = parameters["limit"]
            return transformed

        # For unknown intents, return original parameters
        return parameters

    async def suggest_corrections(self, user_input: str) -> Optional[str]:
        """
        Suggest corrections for misunderstood commands.

        Args:
            user_input: The original user input that was misunderstood

        Returns:
            Suggested correction or None if no good suggestion found
        """
        return await self.intent_recognizer.get_suggested_corrections(user_input)


# Global instance of the command mapper
command_mapper = CommandMapper()


async def process_natural_language_command(user_input: str, token: str) -> Dict[str, Any]:
    """
    Process a natural language command and execute the appropriate action.

    Args:
        user_input: Natural language command from the user
        token: Authentication token for the user

    Returns:
        Result of the command processing
    """
    return await command_mapper.process_command(user_input, token)