from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
import uuid
from ..models.task import Task
from ..models.task_schemas import TaskCreate, TaskUpdate, TaskToggle


class TaskService:
    """
    Service class for handling task-related operations with user isolation.
    """

    @staticmethod
    def get_tasks_by_user_id(session: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Retrieve all tasks for a specific user with pagination.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return (for pagination)

        Returns:
            List of tasks belonging to the user
        """
        statement = select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
        tasks = session.exec(statement).all()
        return tasks

    @staticmethod
    def get_task_by_id(session: Session, task_id: str, user_id: UUID) -> Optional[Task]:
        """
        Retrieve a specific task by ID if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user who should own the task

        Returns:
            The task if found and owned by the user, None otherwise
        """
        # Convert string ID to UUID for comparison
        statement = select(Task).where(Task.id == UUID(task_id), Task.user_id == user_id)
        task = session.exec(statement).first()
        return task

    @staticmethod
    def create_task(session: Session, task_create: TaskCreate, user_id: UUID) -> Task:
        """
        Create a new task for a specific user.

        Args:
            session: Database session
            task_create: Task creation data
            user_id: ID of the user creating the task

        Returns:
            The created task
        """
        # Create task object with the specified user_id
        task_data = task_create.dict()
        task_data['user_id'] = user_id
        task_data['version'] = 1  # Initialize version for optimistic locking

        db_task = Task(**task_data)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def update_task(session: Session, task_id: str, task_update: TaskUpdate, user_id: UUID) -> Optional[Task]:
        """
        Update a specific task if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to update
            task_update: Task update data
            user_id: ID of the user who owns the task

        Returns:
            The updated task if successful, None if task not found or doesn't belong to user
        """
        # Get the existing task
        db_task = TaskService.get_task_by_id(session, task_id, user_id)
        if not db_task:
            return None

        # Handle optimistic locking
        if task_update.version is not None and task_update.version != db_task.version:
            raise ValueError("Task was updated by another request. Please refresh and try again.")

        # Update fields that are provided
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field != "version":  # Don't update the version field directly
                setattr(db_task, field, value)

        # Increment the version for optimistic locking
        db_task.version += 1

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(session: Session, task_id: str, user_id: UUID) -> bool:
        """
        Delete a specific task if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user who owns the task

        Returns:
            True if the task was deleted, False if task not found or doesn't belong to user
        """
        db_task = TaskService.get_task_by_id(session, task_id, user_id)
        if not db_task:
            return False

        session.delete(db_task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: str, toggle_data: TaskToggle, user_id: UUID) -> Optional[Task]:
        """
        Toggle the completion status of a specific task if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to toggle
            toggle_data: Toggle data containing version for optimistic locking
            user_id: ID of the user who owns the task

        Returns:
            The updated task if successful, None if task not found or doesn't belong to user
        """
        # Get the existing task
        db_task = TaskService.get_task_by_id(session, task_id, user_id)
        if not db_task:
            return None

        # Handle optimistic locking
        if toggle_data.version != db_task.version:
            raise ValueError("Task was updated by another request. Please refresh and try again.")

        # Toggle the completion status
        db_task.completed = not db_task.completed
        # Increment the version for optimistic locking
        db_task.version += 1

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task