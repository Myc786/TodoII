"""
Data Isolation Enforcer for Todo Chatbot Extension

This module enforces strict per-user data isolation to ensure that users
can only access their own data through the AI chatbot.
"""

from typing import Dict, Any, Optional
import logging
from enum import Enum

from ..database.session import get_session
from ..models.user import User
from ..models.task import Task
from .security_validator import security_validator


class DataAccessResult(Enum):
    """Enumeration of data access results."""
    ALLOWED = "allowed"
    DENIED = "denied"
    NOT_FOUND = "not_found"


class DataIsolationEnforcer:
    """
    Enforces data isolation between users to prevent unauthorized access.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    async def validate_user_data_access(self, requesting_user_id: str, target_user_id: str) -> bool:
        """
        Validate that a user can access another user's data.

        Args:
            requesting_user_id: ID of the user requesting access
            target_user_id: ID of the user whose data is being accessed

        Returns:
            True if access is allowed, False otherwise
        """
        # For now, implement a strict rule: users can only access their own data
        # In a more complex system, you might have roles/permissions
        is_allowed = requesting_user_id == target_user_id

        if not is_allowed:
            self.logger.warning(
                f"User {requesting_user_id} attempted to access data for user {target_user_id}"
            )

        return is_allowed

    async def validate_task_access(self, user_id: str, task_id: str) -> DataAccessResult:
        """
        Validate that a user has access to a specific task.

        Args:
            user_id: ID of the user requesting access
            task_id: ID of the task to access

        Returns:
            DataAccessResult indicating whether access is allowed, denied, or not found
        """
        try:
            async with get_session() as session:
                # Retrieve the task
                task = await session.get(Task, task_id)

                if not task:
                    self.logger.warning(f"Task {task_id} not found")
                    return DataAccessResult.NOT_FOUND

                # Check if the task belongs to the requesting user
                if str(task.owner_id) != user_id:
                    self.logger.warning(
                        f"User {user_id} attempted to access task {task_id} owned by {task.owner_id}"
                    )
                    return DataAccessResult.DENIED

                return DataAccessResult.ALLOWED

        except Exception as e:
            self.logger.error(f"Error validating task access: {str(e)}")
            return DataAccessResult.DENIED

    async def validate_user_exists(self, user_id: str) -> bool:
        """
        Validate that a user exists in the system.

        Args:
            user_id: ID of the user to validate

        Returns:
            True if user exists, False otherwise
        """
        try:
            async with get_session() as session:
                user = await session.get(User, user_id)
                return user is not None
        except Exception as e:
            self.logger.error(f"Error validating user existence: {str(e)}")
            return False

    async def filter_user_tasks(self, user_id: str, tasks: list) -> list:
        """
        Filter a list of tasks to only include tasks belonging to the specified user.

        Args:
            user_id: ID of the user whose tasks to return
            tasks: List of tasks to filter

        Returns:
            Filtered list of tasks belonging to the user
        """
        filtered_tasks = []
        for task in tasks:
            # Assuming task objects have an owner_id attribute
            if hasattr(task, 'owner_id') and str(task.owner_id) == user_id:
                filtered_tasks.append(task)
            elif hasattr(task, 'dict') and 'owner_id' in task.dict():
                if str(task.dict()['owner_id']) == user_id:
                    filtered_tasks.append(task)
            elif isinstance(task, dict) and 'owner_id' in task:
                if str(task['owner_id']) == user_id:
                    filtered_tasks.append(task)

        return filtered_tasks

    async def validate_bulk_operation_access(self, user_id: str, resource_ids: list, resource_type: str) -> Dict[str, Any]:
        """
        Validate access for bulk operations on multiple resources.

        Args:
            user_id: ID of the user performing the operation
            resource_ids: List of resource IDs to access
            resource_type: Type of resource ('task', 'user', etc.)

        Returns:
            Dictionary with allowed and denied resource IDs
        """
        allowed_ids = []
        denied_ids = []
        not_found_ids = []

        for resource_id in resource_ids:
            if resource_type == 'task':
                access_result = await self.validate_task_access(user_id, resource_id)
                if access_result == DataAccessResult.ALLOWED:
                    allowed_ids.append(resource_id)
                elif access_result == DataAccessResult.DENIED:
                    denied_ids.append(resource_id)
                else:  # NOT_FOUND
                    not_found_ids.append(resource_id)
            # Add other resource types as needed

        return {
            "allowed": allowed_ids,
            "denied": denied_ids,
            "not_found": not_found_ids
        }

    async def enforce_isolation_on_query(self, user_id: str, query_filter: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforce data isolation by adding user-specific filters to a query.

        Args:
            user_id: ID of the user making the request
            query_filter: Original query filter

        Returns:
            Query filter with user isolation enforced
        """
        # Add user-specific filter to ensure only user's data is accessed
        enforced_filter = query_filter.copy()
        enforced_filter['owner_id'] = user_id

        return enforced_filter

    async def validate_cross_user_operation(self, requesting_user_id: str, target_user_id: str, operation: str) -> bool:
        """
        Validate if a cross-user operation is allowed.

        Args:
            requesting_user_id: ID of the user requesting the operation
            target_user_id: ID of the target user
            operation: Type of operation being performed

        Returns:
            True if operation is allowed, False otherwise
        """
        # For now, deny all cross-user operations
        # In a more complex system, you might allow certain operations
        # based on roles, relationships, or permissions
        if requesting_user_id != target_user_id:
            self.logger.warning(
                f"Cross-user operation denied: {operation} by {requesting_user_id} on {target_user_id}"
            )
            return False

        return True

    async def sanitize_returned_data(self, user_id: str, data: Dict[str, Any], resource_type: str) -> Dict[str, Any]:
        """
        Sanitize data to be returned to a user, ensuring no sensitive information is leaked.

        Args:
            user_id: ID of the user requesting the data
            data: Raw data to sanitize
            resource_type: Type of resource being returned

        Returns:
            Sanitized data with sensitive information removed
        """
        sanitized_data = data.copy()

        # Remove sensitive fields that shouldn't be exposed
        sensitive_fields = {
            'user': ['password', 'hashed_password', 'salt', 'verification_token'],
            'task': []  # Tasks generally don't have sensitive fields in our model
        }

        fields_to_remove = sensitive_fields.get(resource_type, [])
        for field in fields_to_remove:
            sanitized_data.pop(field, None)

        # If this is a user resource, ensure it's only the requesting user's data
        if resource_type == 'user' and 'id' in sanitized_data:
            if sanitized_data['id'] != user_id:
                # This should not happen if isolation is properly enforced earlier
                # but as a safety measure, clear the data
                self.logger.error(f"Attempt to return another user's data to user {user_id}")
                return {}

        return sanitized_data


# Global instance of the data isolation enforcer
data_isolation_enforcer = DataIsolationEnforcer()