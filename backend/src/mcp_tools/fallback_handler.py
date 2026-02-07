"""
Fallback Handler for Todo Chatbot Extension

This module implements fallback mechanisms for handling misunderstood commands
and other error scenarios in the AI chatbot.
"""

from typing import Dict, Any, Optional
from enum import Enum


class FallbackType(Enum):
    """Enumeration of fallback types."""
    UNKNOWN_COMMAND = "unknown_command"
    AMBIGUOUS_INTENT = "ambiguous_intent"
    INVALID_PARAMETERS = "invalid_parameters"
    AUTHENTICATION_ERROR = "authentication_error"
    AUTHORIZATION_ERROR = "authorization_error"
    SYSTEM_ERROR = "system_error"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"


class FallbackHandler:
    """
    Handler for providing fallback responses when the chatbot cannot process a request.
    """

    def __init__(self):
        self.fallback_responses = {
            FallbackType.UNKNOWN_COMMAND: [
                "I'm not sure how to help with that. Could you try rephrasing?",
                "I didn't understand that command. Try saying something like 'Add a task to buy groceries' or 'Show my tasks'.",
                "Could you please rephrase that? I can help with creating, listing, completing, or deleting tasks."
            ],
            FallbackType.AMBIGUOUS_INTENT: [
                "I'm not sure what you mean. Could you be more specific?",
                "That's a bit unclear. Could you specify if you want to create, list, update, or delete a task?",
                "I need more information. Are you trying to create a new task or modify an existing one?"
            ],
            FallbackType.INVALID_PARAMETERS: [
                "The command seems incomplete. Please provide all required information.",
                "I need more details to complete that action. Could you provide the missing information?",
                "The task details seem incomplete. Please provide the necessary information."
            ],
            FallbackType.AUTHENTICATION_ERROR: [
                "I'm having trouble verifying your account. Please try logging in again.",
                "Authentication failed. Please make sure you're logged in to continue.",
                "I couldn't verify your identity. Please log in to use the todo features."
            ],
            FallbackType.AUTHORIZATION_ERROR: [
                "You don't have permission to perform this action.",
                "This action requires specific permissions that you don't have.",
                "I can't perform that action as you don't have the required permissions."
            ],
            FallbackType.SYSTEM_ERROR: [
                "I'm experiencing some technical difficulties. Please try again in a moment.",
                "Something went wrong on my end. Could you try that again?",
                "I encountered an error processing your request. Please try again."
            ],
            FallbackType.RATE_LIMIT_EXCEEDED: [
                "You've reached the limit for requests. Please wait a moment before trying again.",
                "Too many requests at once. Please slow down and try again.",
                "I'm receiving too many requests from you. Please wait before sending another."
            ]
        }

        # Suggestions for common misunderstandings
        self.suggestions = {
            "create": [
                "To create a task, try: 'Add a task to buy groceries'",
                "To create a task, try: 'Create a task called finish report'"
            ],
            "list": [
                "To see your tasks, try: 'Show my tasks'",
                "To see your tasks, try: 'What are my pending tasks?'"
            ],
            "complete": [
                "To complete a task, try: 'Mark task 3 as complete'",
                "To complete a task, try: 'Finish the grocery task'"
            ],
            "delete": [
                "To delete a task, try: 'Delete the meeting task'",
                "To delete a task, try: 'Remove task 1'"
            ]
        }

    async def get_fallback_response(self, fallback_type: FallbackType, original_input: Optional[str] = None) -> str:
        """
        Get an appropriate fallback response for the given error type.

        Args:
            fallback_type: The type of fallback needed
            original_input: The original user input that caused the fallback

        Returns:
            A fallback response string
        """
        responses = self.fallback_responses.get(fallback_type, self.fallback_responses[FallbackType.UNKNOWN_COMMAND])

        # Return the first response (in a more complete implementation,
        # we might randomize or rotate these)
        response = responses[0]

        # Add contextual suggestions if applicable
        if original_input and fallback_type in [FallbackType.UNKNOWN_COMMAND, FallbackType.AMBIGUOUS_INTENT]:
            suggestion = await self._get_contextual_suggestion(original_input)
            if suggestion:
                response += f" {suggestion}"

        return response

    async def _get_contextual_suggestion(self, user_input: str) -> Optional[str]:
        """
        Get a contextual suggestion based on the user's input.

        Args:
            user_input: The user's original input

        Returns:
            A suggestion string or None if no good suggestion found
        """
        user_lower = user_input.lower()

        # Check for keywords that might suggest an intent
        if any(keyword in user_lower for keyword in ["create", "add", "new"]):
            return self.suggestions["create"][0]
        elif any(keyword in user_lower for keyword in ["show", "list", "view", "see"]):
            return self.suggestions["list"][0]
        elif any(keyword in user_lower for keyword in ["complete", "finish", "done"]):
            return self.suggestions["complete"][0]
        elif any(keyword in user_lower for keyword in ["delete", "remove"]):
            return self.suggestions["delete"][0]

        return None

    async def handle_unknown_command(self, user_input: str) -> str:
        """
        Handle cases where the command is completely unknown.

        Args:
            user_input: The user's input that wasn't understood

        Returns:
            A helpful response for unknown commands
        """
        return await self.get_fallback_response(FallbackType.UNKNOWN_COMMAND, user_input)

    async def handle_ambiguous_intent(self, user_input: str) -> str:
        """
        Handle cases where the intent is ambiguous.

        Args:
            user_input: The user's input that had ambiguous intent

        Returns:
            A response asking for clarification
        """
        return await self.get_fallback_response(FallbackType.AMBIGUOUS_INTENT, user_input)

    async def handle_invalid_parameters(self, user_input: str, error_details: Optional[str] = None) -> str:
        """
        Handle cases where parameters are invalid.

        Args:
            user_input: The user's input that had invalid parameters
            error_details: Additional error details

        Returns:
            A response indicating invalid parameters
        """
        return await self.get_fallback_response(FallbackType.INVALID_PARAMETERS, user_input)

    async def handle_authentication_error(self) -> str:
        """
        Handle authentication errors.

        Returns:
            A response indicating authentication issues
        """
        return await self.get_fallback_response(FallbackType.AUTHENTICATION_ERROR)

    async def handle_authorization_error(self) -> str:
        """
        Handle authorization errors.

        Returns:
            A response indicating authorization issues
        """
        return await self.get_fallback_response(FallbackType.AUTHORIZATION_ERROR)

    async def handle_system_error(self, error_details: Optional[str] = None) -> str:
        """
        Handle system errors.

        Args:
            error_details: Additional error details

        Returns:
            A response indicating system errors
        """
        return await self.get_fallback_response(FallbackType.SYSTEM_ERROR)

    async def handle_rate_limit(self) -> str:
        """
        Handle rate limit exceeded errors.

        Returns:
            A response indicating rate limit issues
        """
        return await self.get_fallback_response(FallbackType.RATE_LIMIT_EXCEEDED)

    async def generate_help_response(self) -> str:
        """
        Generate a help response with examples of what the bot can do.

        Returns:
            A help response with examples
        """
        help_text = (
            "I'm your AI Todo Assistant! Here's what I can help you with:\n\n"
            "• Create tasks: 'Add a task to buy groceries'\n"
            "• List tasks: 'Show my tasks' or 'What are my pending tasks?'\n"
            "• Complete tasks: 'Mark task 3 as complete' or 'Finish the grocery task'\n"
            "• Delete tasks: 'Delete the assignment task' or 'Remove task 1'\n"
            "• Check status: 'What tasks are completed?'\n\n"
            "Just tell me what you'd like to do with your tasks!"
        )
        return help_text


# Global instance of the fallback handler
fallback_handler = FallbackHandler()