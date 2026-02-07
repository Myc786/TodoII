"""
Ambiguity Resolver for Todo Chatbot Extension

This module handles ambiguous user input by asking clarification questions
to determine the user's intent.
"""

from typing import Dict, Any, List, Optional
from enum import Enum
import re


class AmbiguityType(Enum):
    """Types of ambiguities that may occur in user input."""
    MULTIPLE_TASKS_MATCHED = "multiple_tasks_matched"
    UNCLEAR_ACTION = "unclear_action"
    MISSING_INFORMATION = "missing_information"
    TASK_REFERENCE_AMBIGUOUS = "task_reference_ambiguous"


class AmbiguityResolver:
    """
    Resolves ambiguities in user input by asking clarifying questions.
    """

    def __init__(self):
        self.ambiguity_patterns = {
            AmbiguityType.MULTIPLE_TASKS_MATCHED: [
                r"(\w+)\s+(?:task|one|it)",  # "buy groceries task", "grocery one", "it"
            ],
            AmbiguityType.UNCLEAR_ACTION: [
                r"(?:do|make|need|want)\s+.+",  # "do something", "make this", etc.
            ],
            AmbiguityType.MISSING_INFORMATION: [
                r"update\s+.+",  # "update the task" without details
            ],
            AmbiguityType.TASK_REFERENCE_AMBIGUOUS: [
                r"that\s+(?:task|one|it)",  # "update that task", "complete that one", "finish it"
            ]
        }

    async def detect_ambiguity(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> List[AmbiguityType]:
        """
        Detect potential ambiguities in user input.

        Args:
            user_input: The user's input
            context: Additional context that may help resolve ambiguity

        Returns:
            List of detected ambiguity types
        """
        detected_ambiguities = []

        user_lower = user_input.lower().strip()

        # Check for multiple possible task matches
        if context and 'possible_tasks' in context and len(context['possible_tasks']) > 1:
            detected_ambiguities.append(AmbiguityType.MULTIPLE_TASKS_MATCHED)

        # Check for unclear action
        if any(re.search(pattern, user_lower) for pattern in self.ambiguity_patterns[AmbiguityType.UNCLEAR_ACTION]):
            detected_ambiguities.append(AmbiguityType.UNCLEAR_ACTION)

        # Check for missing information
        if any(re.search(pattern, user_lower) for pattern in self.ambiguity_patterns[AmbiguityType.MISSING_INFORMATION]):
            detected_ambiguities.append(AmbiguityType.MISSING_INFORMATION)

        # Check for ambiguous task reference
        if any(re.search(pattern, user_lower) for pattern in self.ambiguity_patterns[AmbiguityType.TASK_REFERENCE_AMBIGUOUS]):
            detected_ambiguities.append(AmbiguityType.TASK_REFERENCE_AMBIGUOUS)

        return detected_ambiguities

    async def generate_clarification_question(self, ambiguity_type: AmbiguityType,
                                           user_input: str,
                                           context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate an appropriate clarification question for the detected ambiguity.

        Args:
            ambiguity_type: The type of ambiguity detected
            user_input: The original user input
            context: Additional context that may help form the question

        Returns:
            A clarification question for the user
        """
        if ambiguity_type == AmbiguityType.MULTIPLE_TASKS_MATCHED:
            if context and 'possible_tasks' in context:
                task_titles = [task.get('title', f'Task #{task.get("id", "unknown")}')
                              for task in context['possible_tasks'][:5]]  # Limit to 5 tasks
                if len(task_titles) > 1:
                    task_list = ", ".join(task_titles[:-1]) + f" and {task_titles[-1]}"
                    return f"I found multiple tasks that might match: {task_list}. Which one did you mean?"

        elif ambiguity_type == AmbiguityType.UNCLEAR_ACTION:
            return f"I'm not sure what you'd like me to do with '{user_input}'. Could you clarify if you want to create, update, complete, or delete a task?"

        elif ambiguity_type == AmbiguityType.MISSING_INFORMATION:
            return f"To perform this action, I need more information. Could you provide the specific details for the task?"

        elif ambiguity_type == AmbiguityType.TASK_REFERENCE_AMBIGUOUS:
            if context and 'recent_tasks' in context:
                recent_task_titles = [task.get('title', f'Task #{task.get("id", "unknown")}')
                                    for task in context['recent_tasks'][:3]]  # Limit to 3 recent tasks
                if recent_task_titles:
                    task_list = ", ".join(recent_task_titles[:-1]) + f" and {recent_task_titles[-1]}"
                    return f"When you say 'that', do you mean {task_list}? Or could you specify which task you're referring to?"

        # Default clarification question
        return "I'm not sure I understand what you mean. Could you please rephrase or provide more details?"

    async def resolve_ambiguity(self, user_input: str,
                               ambiguity_types: List[AmbiguityType],
                               context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Attempt to resolve detected ambiguities in user input.

        Args:
            user_input: The user's input
            ambiguity_types: List of detected ambiguity types
            context: Additional context that may help resolve ambiguity

        Returns:
            Resolution result with either clarified parameters or clarification request
        """
        if not ambiguity_types:
            # No ambiguities detected, return original input for processing
            return {
                "resolved": True,
                "parameters": {"original_input": user_input},
                "needs_clarification": False
            }

        # If there are ambiguities, generate clarification questions
        clarification_questions = []
        for ambiguity_type in ambiguity_types:
            question = await self.generate_clarification_question(ambiguity_type, user_input, context)
            clarification_questions.append(question)

        return {
            "resolved": False,
            "parameters": {},
            "needs_clarification": True,
            "clarification_questions": clarification_questions
        }

    async def handle_ambiguous_input(self, user_input: str,
                                   context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle ambiguous input by detecting ambiguities and returning appropriate response.

        Args:
            user_input: The user's input
            context: Additional context that may help resolve ambiguity

        Returns:
            Response indicating if input is ambiguous and what to do next
        """
        ambiguity_types = await self.detect_ambiguity(user_input, context)

        if ambiguity_types:
            return await self.resolve_ambiguity(user_input, ambiguity_types, context)
        else:
            # No ambiguities detected
            return {
                "resolved": True,
                "parameters": {"original_input": user_input},
                "needs_clarification": False
            }

    async def build_context_from_conversation(self, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Build context from conversation history to help resolve ambiguities.

        Args:
            conversation_history: List of previous conversation exchanges

        Returns:
            Context dictionary with relevant information
        """
        context = {
            "recent_tasks": [],
            "possible_tasks": [],
            "previous_actions": [],
            "entities_mentioned": []
        }

        # Extract recent tasks from conversation history
        for message in reversed(conversation_history[-10:]):  # Look at last 10 messages
            if message.get('sender') == 'ai' and 'data' in message:
                # This is an AI response that might contain task information
                data = message['data']
                if isinstance(data, dict):
                    if 'id' in data and 'title' in data:  # Likely a task
                        context['recent_tasks'].append(data)
                        if len(context['recent_tasks']) >= 5:  # Limit to 5 recent tasks
                            break

        return context


# Global instance of the ambiguity resolver
ambiguity_resolver = AmbiguityResolver()