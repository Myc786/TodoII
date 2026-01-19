"""
Task Identifier for Todo Chatbot Extension

This module identifies specific tasks from natural language input,
particularly for commands that reference existing tasks.
"""

import re
from typing import List, Dict, Optional, Tuple, Any
from sqlmodel import select
from datetime import datetime

from ..database.session import get_session
from ..models.task import Task
from ..models.user import User


class TaskIdentifier:
    """
    Identifies specific tasks from natural language input.
    """

    def __init__(self):
        # Patterns for identifying tasks by various attributes
        self.patterns = {
            "by_number": re.compile(r'(?:task|number|#)\s*(\d+)', re.IGNORECASE),
            "by_title": re.compile(r'"([^"]+)"|\'([^\']+)\'|([^.!?]+?)(?:\s+(?:task|please|now|today|tomorrow))', re.IGNORECASE),
            "by_keyword": re.compile(r'(?:task|about|regarding|for)\s+([^.!?]+?)(?:\.|!|\?|$)', re.IGNORECASE),
        }

    async def identify_task_from_text(self, user_input: str, user_id: str) -> Optional[Task]:
        """
        Identify a specific task from natural language input.

        Args:
            user_input: The user's input that may reference a task
            user_id: The ID of the user whose tasks to search

        Returns:
            The identified Task object or None if no task is identified
        """
        # First, try to identify by task number
        task = await self._identify_by_number(user_input, user_id)
        if task:
            return task

        # Next, try to identify by title or keywords
        task = await self._identify_by_title_or_keywords(user_input, user_id)
        if task:
            return task

        # If no specific task identified, return None
        return None

    async def _identify_by_number(self, user_input: str, user_id: str) -> Optional[Task]:
        """
        Identify a task by number reference (e.g., "task 3", "#5").

        Args:
            user_input: The user's input
            user_id: The ID of the user whose tasks to search

        Returns:
            The identified Task object or None
        """
        match = self.patterns["by_number"].search(user_input)
        if match:
            try:
                task_number = int(match.group(1))
                return await self._get_task_by_number(task_number, user_id)
            except ValueError:
                pass  # Not a valid number

        return None

    async def _identify_by_title_or_keywords(self, user_input: str, user_id: str) -> Optional[Task]:
        """
        Identify a task by title or keywords in the input.

        Args:
            user_input: The user's input
            user_id: The ID of the user whose tasks to search

        Returns:
            The identified Task object or None
        """
        # Try to extract potential task titles from quotes
        quote_match = re.search(r'"([^"]+)"|\'([^\']+)\'', user_input)
        if quote_match:
            title = quote_match.group(1) or quote_match.group(2)
            task = await self._find_task_by_title(title.strip(), user_id)
            if task:
                return task

        # Try to extract potential task identifiers from keywords
        keyword_match = self.patterns["by_keyword"].search(user_input)
        if keyword_match:
            keyword = keyword_match.group(1).strip()
            # First try as a direct title match
            task = await self._find_task_by_title(keyword, user_id)
            if task:
                return task

            # Then try as a partial match
            task = await self._find_task_by_partial_match(keyword, user_id)
            if task:
                return task

        return None

    async def _get_task_by_number(self, task_number: int, user_id: str) -> Optional[Task]:
        """
        Get a task by its sequential number among user's tasks.

        Args:
            task_number: The sequential number of the task (1-indexed)
            user_id: The ID of the user whose tasks to search

        Returns:
            The Task object or None
        """
        try:
            async with get_session() as session:
                # Get all tasks for the user ordered by creation date
                statement = select(Task).where(Task.owner_id == user_id).order_by(Task.created_at)
                result = await session.exec(statement)
                tasks = result.all()

                # Convert to 0-indexed and return the requested task
                if 1 <= task_number <= len(tasks):
                    return tasks[task_number - 1]

        except Exception as e:
            print(f"Error getting task by number: {e}")

        return None

    async def _find_task_by_title(self, title: str, user_id: str) -> Optional[Task]:
        """
        Find a task by its exact title.

        Args:
            title: The title to search for
            user_id: The ID of the user whose tasks to search

        Returns:
            The Task object or None
        """
        try:
            async with get_session() as session:
                # Find task with exact title match
                statement = select(Task).where(
                    Task.owner_id == user_id,
                    Task.title.ilike(f"%{title}%")  # Using ilike for case-insensitive partial match
                ).order_by(Task.created_at.desc())  # Most recent first

                result = await session.exec(statement)
                tasks = result.all()

                # Return the first match or None if no matches
                if tasks:
                    # For exact match, check if title matches exactly (ignoring case)
                    for task in tasks:
                        if task.title.lower() == title.lower():
                            return task
                    # If no exact match, return the first partial match
                    return tasks[0]

        except Exception as e:
            print(f"Error finding task by title: {e}")

        return None

    async def _find_task_by_partial_match(self, keyword: str, user_id: str) -> Optional[Task]:
        """
        Find a task by partial title match.

        Args:
            keyword: The keyword to search for in task titles
            user_id: The ID of the user whose tasks to search

        Returns:
            The Task object or None
        """
        try:
            async with get_session() as session:
                # Find tasks that contain the keyword
                statement = select(Task).where(
                    Task.owner_id == user_id,
                    Task.title.ilike(f"%{keyword}%")
                ).order_by(Task.created_at.desc())

                result = await session.exec(statement)
                tasks = result.all()

                # Return the most recent match
                if tasks:
                    return tasks[0]

        except Exception as e:
            print(f"Error finding task by partial match: {e}")

        return None

    async def identify_multiple_tasks(self, user_input: str, user_id: str) -> List[Task]:
        """
        Identify multiple tasks from natural language input.

        Args:
            user_input: The user's input
            user_id: The ID of the user whose tasks to search

        Returns:
            List of identified Task objects
        """
        tasks = []

        # Look for multiple task numbers
        number_matches = self.patterns["by_number"].findall(user_input)
        for num_str in number_matches:
            try:
                task_num = int(num_str)
                task = await self._get_task_by_number(task_num, user_id)
                if task and task not in tasks:  # Avoid duplicates
                    tasks.append(task)
            except ValueError:
                continue

        # If no numbered tasks found, try to identify by context
        if not number_matches:
            # For now, just return the most relevant single task
            single_task = await self.identify_task_from_text(user_input, user_id)
            if single_task:
                tasks = [single_task]

        return tasks

    async def get_task_suggestions(self, partial_input: str, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get task suggestions based on partial input.

        Args:
            partial_input: Partial text to match against task titles
            user_id: The ID of the user whose tasks to search
            limit: Maximum number of suggestions to return

        Returns:
            List of task suggestions with ID and title
        """
        suggestions = []

        try:
            async with get_session() as session:
                # Find tasks that contain the partial input
                statement = select(Task).where(
                    Task.owner_id == user_id,
                    Task.title.ilike(f"%{partial_input}%")
                ).order_by(Task.updated_at.desc()).limit(limit)

                result = await session.exec(statement)
                tasks = result.all()

                # Format the suggestions
                for task in tasks:
                    suggestions.append({
                        "id": str(task.id),
                        "title": task.title,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat()
                    })

        except Exception as e:
            print(f"Error getting task suggestions: {e}")

        return suggestions


# Global instance of the task identifier
task_identifier = TaskIdentifier()