"""
Error Handler for Todo Chatbot Extension

This module handles errors for unrecognized commands and other error scenarios
in the AI chatbot.
"""

from typing import Dict, Any, Optional
from enum import Enum


class ErrorType(Enum):
    """Types of errors that can occur in the chatbot."""
    UNRECOGNIZED_COMMAND = "unrecognized_command"
    INVALID_INPUT = "invalid_input"
    AUTHENTICATION_FAILED = "authentication_failed"
    AUTHORIZATION_FAILED = "authorization_failed"
    RESOURCE_NOT_FOUND = "resource_not_found"
    VALIDATION_ERROR = "validation_error"
    SYSTEM_ERROR = "system_error"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    TIMEOUT_ERROR = "timeout_error"


class ErrorHandler:
    """
    Handles errors in the chatbot and provides appropriate responses.
    """

    def __init__(self):
        self.error_responses = {
            ErrorType.UNRECOGNIZED_COMMAND: [
                "I'm not sure how to help with that. Could you try rephrasing?",
                "I didn't understand that command. Try saying something like 'Add a task to buy groceries' or 'Show my tasks'.",
                "Could you please rephrase that? I can help with creating, listing, completing, or deleting tasks."
            ],
            ErrorType.INVALID_INPUT: [
                "The command seems incomplete. Please provide all required information.",
                "I need more details to complete that action. Could you provide the missing information?",
                "The task details seem incomplete. Please provide the necessary information."
            ],
            ErrorType.AUTHENTICATION_FAILED: [
                "I'm having trouble verifying your account. Please try logging in again.",
                "Authentication failed. Please make sure you're logged in to continue.",
                "I couldn't verify your identity. Please log in to use the todo features."
            ],
            ErrorType.AUTHORIZATION_FAILED: [
                "You don't have permission to perform this action.",
                "This action requires specific permissions that you don't have.",
                "I can't perform that action as you don't have the required permissions."
            ],
            ErrorType.RESOURCE_NOT_FOUND: [
                "I couldn't find the task you're looking for. Could you check the task name or ID?",
                "The requested task doesn't exist. Maybe it was already deleted?",
                "I can't find that task. Could you verify the task details?"
            ],
            ErrorType.VALIDATION_ERROR: [
                "The information you provided doesn't seem to be valid. Could you check it?",
                "There's an issue with the data you provided. Please verify and try again.",
                "I need you to provide valid information for this action."
            ],
            ErrorType.SYSTEM_ERROR: [
                "I'm experiencing some technical difficulties. Please try again in a moment.",
                "Something went wrong on my end. Could you try that again?",
                "I encountered an error processing your request. Please try again."
            ],
            ErrorType.RATE_LIMIT_EXCEEDED: [
                "You've reached the limit for requests. Please wait a moment before trying again.",
                "Too many requests at once. Please slow down and try again.",
                "I'm receiving too many requests from you. Please wait before sending another."
            ],
            ErrorType.TIMEOUT_ERROR: [
                "I'm taking too long to respond. Please try your request again.",
                "The request timed out. Please try again.",
                "I had trouble processing your request in time. Could you try again?"
            ]
        }

        # Common command suggestions
        self.command_suggestions = {
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

    async def handle_error(self, error_type: ErrorType, details: Optional[str] = None,
                          original_input: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle an error and return an appropriate response.

        Args:
            error_type: The type of error that occurred
            details: Additional error details
            original_input: The original user input that caused the error

        Returns:
            Dictionary with error response information
        """
        responses = self.error_responses.get(error_type,
                                           self.error_responses[ErrorType.SYSTEM_ERROR])

        # Select a response (in a full implementation, we might randomize this)
        response = responses[0]

        # Add contextual suggestions if applicable
        if original_input and error_type in [ErrorType.UNRECOGNIZED_COMMAND, ErrorType.INVALID_INPUT]:
            suggestion = await self._get_contextual_suggestion(original_input)
            if suggestion:
                response += f" {suggestion}"

        return {
            "success": False,
            "error_type": error_type.value,
            "message": response,
            "details": details or "No additional details",
            "original_input": original_input or ""
        }

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
        if any(keyword in user_lower for keyword in ["create", "add", "new", "make"]):
            return self.command_suggestions["create"][0]
        elif any(keyword in user_lower for keyword in ["show", "list", "view", "see", "my", "tasks", "todos"]):
            return self.command_suggestions["list"][0]
        elif any(keyword in user_lower for keyword in ["complete", "finish", "done", "mark"]):
            return self.command_suggestions["complete"][0]
        elif any(keyword in user_lower for keyword in ["delete", "remove", "kill"]):
            return self.command_suggestions["delete"][0]

        return None

    async def handle_unrecognized_command(self, original_input: str) -> Dict[str, Any]:
        """
        Handle cases where the command is not recognized.

        Args:
            original_input: The original user input that wasn't recognized

        Returns:
            Error response for unrecognized command
        """
        return await self.handle_error(ErrorType.UNRECOGNIZED_COMMAND,
                                     original_input=original_input)

    async def handle_invalid_input(self, details: Optional[str] = None,
                                 original_input: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle cases where the input is invalid.

        Args:
            details: Details about why the input is invalid
            original_input: The original user input that was invalid

        Returns:
            Error response for invalid input
        """
        return await self.handle_error(ErrorType.INVALID_INPUT,
                                     details=details,
                                     original_input=original_input)

    async def handle_authentication_failed(self, details: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle authentication failures.

        Args:
            details: Details about the authentication failure

        Returns:
            Error response for authentication failure
        """
        return await self.handle_error(ErrorType.AUTHENTICATION_FAILED,
                                     details=details)

    async def handle_authorization_failed(self, details: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle authorization failures.

        Args:
            details: Details about the authorization failure

        Returns:
            Error response for authorization failure
        """
        return await self.handle_error(ErrorType.AUTHORIZATION_FAILED,
                                     details=details)

    async def handle_resource_not_found(self, details: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle cases where a requested resource is not found.

        Args:
            details: Details about the missing resource

        Returns:
            Error response for resource not found
        """
        return await self.handle_error(ErrorType.RESOURCE_NOT_FOUND,
                                     details=details)

    async def handle_validation_error(self, details: Optional[str] = None,
                                   original_input: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle validation errors.

        Args:
            details: Details about the validation error
            original_input: The original user input that caused the validation error

        Returns:
            Error response for validation error
        """
        return await self.handle_error(ErrorType.VALIDATION_ERROR,
                                     details=details,
                                     original_input=original_input)

    async def handle_system_error(self, details: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle system errors.

        Args:
            details: Details about the system error

        Returns:
            Error response for system error
        """
        return await self.handle_error(ErrorType.SYSTEM_ERROR,
                                     details=details)

    async def handle_rate_limit_exceeded(self, details: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle rate limit exceeded errors.

        Args:
            details: Details about the rate limit issue

        Returns:
            Error response for rate limit exceeded
        """
        return await self.handle_error(ErrorType.RATE_LIMIT_EXCEEDED,
                                     details=details)

    async def handle_timeout_error(self, details: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle timeout errors.

        Args:
            details: Details about the timeout issue

        Returns:
            Error response for timeout error
        """
        return await self.handle_error(ErrorType.TIMEOUT_ERROR,
                                     details=details)

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


# Global instance of the error handler
error_handler = ErrorHandler()