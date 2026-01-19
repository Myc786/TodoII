"""
Intent Recognition Engine for Todo Chatbot Extension

This module implements the intent recognition engine that identifies
user intentions from natural language input.
"""

import re
from typing import Dict, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

from .agent_prompt import get_intent_examples


class IntentType(Enum):
    """Enumeration of possible user intents."""
    CREATE_TASK = "create_task"
    LIST_TASKS = "list_tasks"
    UPDATE_TASK = "update_task"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    QUERY_STATUS = "query_status"
    UNKNOWN = "unknown"


@dataclass
class IntentRecognitionResult:
    """Result of intent recognition."""
    intent: IntentType
    confidence: float  # Between 0 and 1
    parameters: Dict[str, Any]
    original_text: str


class IntentRecognizer:
    """
    Intent recognition engine that identifies user intentions from natural language input.
    """

    def __init__(self):
        # Compile regex patterns for different intents
        self.patterns = {
            IntentType.CREATE_TASK: [
                r"(?:add|create|make|new)\s+(?:a\s+)?(?:task|todo)\s+(?:to\s+|for\s+)?(.+)",
                r"(?:add|create|make|new)\s+(.+)\s+(?:as\s+)?(?:a\s+)?(?:task|todo)",
                r"(?:task|todo)\s+(?:to\s+)?(.+)",
                r"(.+)\s+(?:please|pls)?",
            ],
            IntentType.LIST_TASKS: [
                r"(?:show|display|list|view)\s+(?:my\s+)?(?:tasks?|todos?)",
                r"(?:what|show)\s+(?:are\s+)?(?:my\s+)?(?:tasks?|todos?)",
                r"(?:do\s+i\s+have|what\s+do\s+i\s+have)\s+(?:any\s+)?(?:tasks?|todos?)",
                r"my\s+(?:tasks?|todos?)",
            ],
            IntentType.COMPLETE_TASK: [
                r"(?:mark|complete|finish|done)\s+(?:task|todo)\s+(\d+|\w+)\s+(?:as\s+)?(?:complete|done|finished)",
                r"(?:mark|complete|finish|done)\s+(?:task|todo)\s+(\d+|\w+)",
                r"(?:complete|finish|done)\s+(?:the\s+)?(.+?)\s+(?:task|todo)",
            ],
            IntentType.DELETE_TASK: [
                r"(?:delete|remove|kill|erase)\s+(?:task|todo)\s+(\d+|\w+)",
                r"(?:delete|remove|kill|erase)\s+(?:the\s+)?(.+?)\s+(?:task|todo)",
                r"(?:remove|delete)\s+(?:task|todo)\s+(?:named\s+|called\s+)?(.+)",
            ],
            IntentType.UPDATE_TASK: [
                r"(?:update|modify|change|edit)\s+(?:task|todo)\s+(?:id\s+)?(\d+|\w+)",
                r"(?:update|modify|change|edit)\s+(?:the\s+)?(.+?)\s+(?:task|todo)",
            ],
            IntentType.QUERY_STATUS: [
                r"(?:what|show)\s+(?:tasks?|todos?)\s+(?:are\s+)?(?:completed|done|finished)",
                r"(?:what|show)\s+(?:tasks?|todos?)\s+(?:are\s+)?(?:pending|not\s+done|incomplete)",
                r"(?:do\s+i\s+have|how\s+many)\s+(?:completed|done|finished)\s+(?:tasks?|todos?)",
                r"(?:completed|done|finished)\s+(?:tasks?|todos?)",
            ]
        }

    async def recognize_intent(self, user_input: str) -> IntentRecognitionResult:
        """
        Recognize the intent from user input.

        Args:
            user_input: The raw input from the user

        Returns:
            IntentRecognitionResult with the identified intent and parameters
        """
        user_input = user_input.strip().lower()

        # First, try pattern matching
        for intent_type, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, user_input)
                if match:
                    # Extract parameters based on intent
                    params = await self._extract_parameters(intent_type, user_input, match)
                    return IntentRecognitionResult(
                        intent=intent_type,
                        confidence=0.9,  # High confidence for pattern matches
                        parameters=params,
                        original_text=user_input
                    )

        # If no pattern matches, use a more general approach
        intent_type, confidence = await self._classify_general_intent(user_input)
        return IntentRecognitionResult(
            intent=intent_type,
            confidence=confidence,
            parameters={},
            original_text=user_input
        )

    async def _extract_parameters(self, intent_type: IntentType, user_input: str, match: re.Match) -> Dict[str, Any]:
        """
        Extract parameters for the recognized intent.

        Args:
            intent_type: The recognized intent type
            user_input: The original user input
            match: The regex match object

        Returns:
            Dictionary of extracted parameters
        """
        params = {}

        if intent_type == IntentType.CREATE_TASK:
            # Extract task title from the matched groups
            for group in match.groups():
                if group:
                    params['title'] = group.strip()
                    break

        elif intent_type == IntentType.COMPLETE_TASK:
            # Extract task ID or name
            for group in match.groups():
                if group:
                    if group.isdigit():
                        params['taskId'] = group
                    else:
                        params['taskName'] = group.strip()
                    break
            params['completed'] = True

        elif intent_type == IntentType.DELETE_TASK:
            # Extract task ID or name
            for group in match.groups():
                if group:
                    if group.isdigit():
                        params['taskId'] = group
                    else:
                        params['taskName'] = group.strip()
                    break

        elif intent_type == IntentType.LIST_TASKS:
            # Determine filter type based on the input
            if "completed" in user_input or "done" in user_input or "finished" in user_input:
                params['filter'] = 'completed'
            elif "pending" in user_input or "not done" in user_input or "incomplete" in user_input:
                params['filter'] = 'active'
            else:
                params['filter'] = 'all'

        elif intent_type == IntentType.QUERY_STATUS:
            # Determine the status query type
            if "completed" in user_input or "done" in user_input or "finished" in user_input:
                params['filter'] = 'completed'
            elif "pending" in user_input or "not done" in user_input or "incomplete" in user_input:
                params['filter'] = 'active'
            else:
                params['filter'] = 'all'

        return params

    async def _classify_general_intent(self, user_input: str) -> Tuple[IntentType, float]:
        """
        Classify intent using general keywords if pattern matching fails.

        Args:
            user_input: The user input to classify

        Returns:
            Tuple of (intent type, confidence level)
        """
        # Keywords for each intent type
        keywords = {
            IntentType.CREATE_TASK: ['add', 'create', 'new', 'make', 'task', 'todo'],
            IntentType.LIST_TASKS: ['show', 'list', 'view', 'see', 'my', 'tasks', 'todos'],
            IntentType.COMPLETE_TASK: ['complete', 'finish', 'done', 'mark', 'as done'],
            IntentType.DELETE_TASK: ['delete', 'remove', 'kill', 'erase'],
            IntentType.UPDATE_TASK: ['update', 'modify', 'change', 'edit'],
            IntentType.QUERY_STATUS: ['completed', 'done', 'finished', 'pending', 'incomplete']
        }

        scores = {}
        user_words = set(user_input.split())

        for intent_type, intent_keywords in keywords.items():
            score = sum(1 for keyword in intent_keywords if keyword in user_words)
            scores[intent_type] = score

        # Find the intent with the highest score
        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]

        if max_score == 0:
            return IntentType.UNKNOWN, 0.1
        else:
            # Normalize confidence based on the highest possible score
            confidence = min(max_score / 5.0, 1.0)  # Assuming max 5 keywords could match
            return best_intent, confidence

    async def get_suggested_corrections(self, user_input: str) -> Optional[str]:
        """
        Provide suggested corrections for misunderstood input.

        Args:
            user_input: The user input that was misunderstood

        Returns:
            Suggested correction or None if no good suggestion found
        """
        # Simple suggestions based on common patterns
        user_lower = user_input.lower()

        if "add" in user_lower and "task" not in user_lower and "todo" not in user_lower:
            return f'Did you mean: "Add a task to {user_input.replace("add", "").strip()}"?'

        if "show" in user_lower and any(word in user_lower for word in ["my", "tasks", "todos"]):
            return 'I can show your tasks. Try saying "Show my tasks"'

        if any(word in user_lower for word in ["complete", "finish", "done"]) and any(word in user_lower for word in ["task", "todo"]):
            return 'To complete a task, say something like "Mark task 3 as complete"'

        return None


# Global instance of the intent recognizer
intent_recognizer = IntentRecognizer()