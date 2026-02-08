from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime
from ..models.task import Task
from ..models.tag import Tag
from ..models.task_tag import TaskTag
from ..models.task_schemas import TaskCreate, TaskUpdate, TaskToggle, TaskTagAssignment


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

        # Add tags to each task by extending the task object with tags
        for task in tasks:
            task_tags = session.exec(select(TaskTag).where(TaskTag.task_id == task.id)).all()
            tag_ids = [str(tt.tag_id) for tt in task_tags]
            if tag_ids:
                tags = session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all()
                # Explicitly assign tags to the task object
                task.tags = tags
            else:
                task.tags = []

        return tasks

    @staticmethod
    def get_task_by_id(session: Session, task_id: str | UUID, user_id: UUID) -> Optional[Task]:
        """
        Retrieve a specific task by ID if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user who should own the task

        Returns:
            The task if found and owned by the user, None otherwise
        """
        # Convert string ID to UUID for comparison if needed
        task_uuid = UUID(str(task_id)) if not isinstance(task_id, UUID) else task_id
        statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_id)
        task = session.exec(statement).first()

        if task:
            # Add tags to the task
            task_tags = session.exec(select(TaskTag).where(TaskTag.task_id == task.id)).all()
            tag_ids = [str(tt.tag_id) for tt in task_tags]
            if tag_ids:
                tags = session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all()
                 # Explicitly assign tags to the task object
                task.tags = tags
            else:
                task.tags = []

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
        task_data = task_create.dict(exclude_unset=True)
        task_data['user_id'] = user_id
        task_data['version'] = 1  # Initialize version for optimistic locking

        # Set default values for fields that need them
        task_data['id'] = uuid.uuid4()
        task_data['created_at'] = datetime.utcnow()
        task_data['updated_at'] = datetime.utcnow()

        # Remove tag_ids and tags from task_data as they're not part of the Task model directly
        tag_ids = task_data.pop('tag_ids', [])
        task_data.pop('tags', None)  # Remove any tags field that might exist

        db_task = Task(**task_data)
        session.add(db_task)
        session.commit()

        # Handle tag assignments if provided
        if tag_ids:
            TaskService._assign_tags_to_task(session, db_task.id, tag_ids)
            
            # Commit tag assignments
            session.commit()

        # Get the newly created task with a fresh query to avoid refresh issues
        from sqlmodel import select
        # Query without loading the tags relationship to avoid the validation error
        fresh_task = session.exec(select(Task).where(Task.id == db_task.id)).first()
        
        # Manually load tags for the response to ensure they are present for validation
        if tag_ids:
             tag_objects = session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all()
             fresh_task.tags = tag_objects
        else:
             fresh_task.tags = []

        # Return the fresh task
        return fresh_task

    @staticmethod
    def update_task(session: Session, task_id: str | UUID, task_update: TaskUpdate, user_id: UUID) -> Optional[Task]:
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
        tag_ids = update_data.pop('tag_ids', None)  # Remove tag_ids from update
        for field, value in update_data.items():
            if field != "version":  # Don't update the version field directly
                setattr(db_task, field, value)

        # Increment the version for optimistic locking
        db_task.version += 1

        # Handle tag assignments if provided
        if tag_ids is not None:
            TaskService._remove_all_tags_from_task(session, db_task.id)
            if tag_ids:
                TaskService._assign_tags_to_task(session, db_task.id, tag_ids)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Add tags to the refreshed task object
        if tag_ids is not None:
            if tag_ids:
                tag_objects = session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all()
                # Explicitly assign tags to the task object
                db_task.tags = tag_objects
            else:
                db_task.tags = []
        else:
             # If tag_ids is None (not updated), we still need to ensure tags are loaded for response
             task_tags = session.exec(select(TaskTag).where(TaskTag.task_id == db_task.id)).all()
             tag_ids_list = [str(tt.tag_id) for tt in task_tags]
             if tag_ids_list:
                 tag_objects = session.exec(select(Tag).where(Tag.id.in_(tag_ids_list))).all()
                 db_task.tags = tag_objects
             else:
                 db_task.tags = []
        return db_task

    @staticmethod
    def delete_task(session: Session, task_id: str | UUID, user_id: UUID) -> bool:
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

        # Remove all tag associations before deleting the task
        TaskService._remove_all_tags_from_task(session, db_task.id)

        session.delete(db_task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: str | UUID, toggle_data: TaskToggle, user_id: UUID) -> Optional[Task]:
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
        was_completed = db_task.completed
        db_task.completed = not db_task.completed
        # Increment the version for optimistic locking
        db_task.version += 1

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # If the task was marked as completed and has a recurrence pattern, create a new instance
        if db_task.completed and not was_completed and db_task.recurrence_pattern:
            try:
                from .recurring_task_service import RecurringTaskService
                RecurringTaskService.handle_task_completion(session, db_task)
            except Exception as e:
                print(f"Error creating recurring task instance: {e}")
                # Continue with the original task update even if recurring task creation fails

        # Add tags to the refreshed task object
        task_tags = session.exec(select(TaskTag).where(TaskTag.task_id == db_task.id)).all()
        tag_ids = [str(tt.tag_id) for tt in task_tags]
        if tag_ids:
            tags = session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all()
            # Temporarily add tags for serialization without triggering validation
            if hasattr(db_task, '__dict__'):
                db_task.__dict__['tags'] = tags
            else:
                object.__setattr__(db_task, 'tags', tags)
        else:
            # Temporarily add empty tags for serialization
            if hasattr(db_task, '__dict__'):
                db_task.__dict__['tags'] = []
            else:
                object.__setattr__(db_task, 'tags', [])

        return db_task

    @staticmethod
    def _assign_tags_to_task(session: Session, task_id: UUID, tag_ids: List[str]) -> None:
        """
        Assign tags to a task.

        Args:
            session: Database session
            task_id: ID of the task to assign tags to
            tag_ids: List of tag IDs to assign
        """
        for tag_id in tag_ids:
            task_tag = TaskTag(task_id=task_id, tag_id=UUID(tag_id))
            session.add(task_tag)
        session.commit()

    @staticmethod
    def _remove_all_tags_from_task(session: Session, task_id: UUID) -> None:
        """
        Remove all tags from a task.

        Args:
            session: Database session
            task_id: ID of the task to remove tags from
        """
        task_tags = session.exec(select(TaskTag).where(TaskTag.task_id == task_id)).all()
        for task_tag in task_tags:
            session.delete(task_tag)
        session.commit()

    @staticmethod
    def update_task_tags(session: Session, task_id: str, tag_assignment: TaskTagAssignment, user_id: UUID) -> Optional[Task]:
        """
        Update tags for a specific task.

        Args:
            session: Database session
            task_id: ID of the task to update tags for
            tag_assignment: Tag assignment data
            user_id: ID of the user who owns the task

        Returns:
            The updated task if successful, None if task not found or doesn't belong to user
        """
        # Get the existing task
        db_task = TaskService.get_task_by_id(session, task_id, user_id)
        if not db_task:
            return None

        # Remove all existing tags
        TaskService._remove_all_tags_from_task(session, UUID(task_id))

        # Add new tags if provided
        if tag_assignment.tag_ids:
            TaskService._assign_tags_to_task(session, UUID(task_id), tag_assignment.tag_ids)

        # Refresh the task to get updated tags
        session.refresh(db_task)

        # Add tags to the refreshed task object
        task_tags = session.exec(select(TaskTag).where(TaskTag.task_id == db_task.id)).all()
        tag_ids = [str(tt.tag_id) for tt in task_tags]
        if tag_ids:
            tags = session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all()
            # Temporarily add tags for serialization without triggering validation
            if hasattr(db_task, '__dict__'):
                db_task.__dict__['tags'] = tags
            else:
                object.__setattr__(db_task, 'tags', tags)
        else:
            # Temporarily add empty tags for serialization
            if hasattr(db_task, '__dict__'):
                db_task.__dict__['tags'] = []
            else:
                object.__setattr__(db_task, 'tags', [])

        return db_task

    @staticmethod
    def search_and_filter_tasks(
        session: Session,
        user_id: UUID,
        search_query: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tag_ids: Optional[List[str]] = None,
        due_before: Optional[str] = None,
        due_after: Optional[str] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        Search and filter tasks by various criteria.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to search/filter
            search_query: Keyword to search in title/description
            status: Filter by completion status ('active', 'completed', 'all')
            priority: Filter by priority level ('high', 'medium', 'low')
            tag_ids: List of tag IDs to filter by
            due_before: Filter tasks due before this date
            due_after: Filter tasks due after this date
            sort_by: Sort by field ('due_date', 'priority', 'created_at', 'title')
            order: Sort order ('asc', 'desc')
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return (for pagination)

        Returns:
            List of tasks matching the search and filter criteria
        """
        # Start with base query for user's tasks
        query = select(Task).where(Task.user_id == user_id)

        # Apply search filter
        if search_query:
            search_term = f"%{search_query}%"
            query = query.where(
                Task.title.ilike(search_term) |
                (Task.description.is_not(None) & Task.description.ilike(search_term))
            )

        # Apply status filter
        if status and status.lower() != 'all':
            if status.lower() == 'active':
                query = query.where(Task.completed == False)
            elif status.lower() == 'completed':
                query = query.where(Task.completed == True)

        # Apply priority filter
        if priority:
            query = query.where(Task.priority == priority.lower())

        # Apply due date filters
        if due_before:
            try:
                # Handle ISO format with timezone
                if due_before.endswith('Z'):
                    due_before_dt = datetime.fromisoformat(due_before.replace('Z', '+00:00'))
                elif '+' in due_before or due_before.count('-') > 2:  # Has timezone info
                    due_before_dt = datetime.fromisoformat(due_before)
                else:
                    # Assume it's a date string, convert to datetime
                    due_before_dt = datetime.fromisoformat(due_before)

                query = query.where(Task.due_date <= due_before_dt)
            except ValueError:
                # Invalid date format, ignore filter
                pass

        if due_after:
            try:
                # Handle ISO format with timezone
                if due_after.endswith('Z'):
                    due_after_dt = datetime.fromisoformat(due_after.replace('Z', '+00:00'))
                elif '+' in due_after or due_after.count('-') > 2:  # Has timezone info
                    due_after_dt = datetime.fromisoformat(due_after)
                else:
                    # Assume it's a date string, convert to datetime
                    due_after_dt = datetime.fromisoformat(due_after)

                query = query.where(Task.due_date >= due_after_dt)
            except ValueError:
                # Invalid date format, ignore filter
                pass

        # Apply tag filter
        if tag_ids:
            # First get all task IDs that have any of the specified tags
            tag_query = select(TaskTag.task_id).where(TaskTag.tag_id.in_([UUID(tid) for tid in tag_ids]))
            task_ids_with_tags = [row.task_id for row in session.exec(tag_query).all()]

            if task_ids_with_tags:
                query = query.where(Task.id.in_(task_ids_with_tags))
            else:
                # If no tasks have the specified tags, return empty list
                return []

        # Apply sorting
        if sort_by:
            sort_field = None
            if sort_by == 'due_date':
                sort_field = Task.due_date
            elif sort_by == 'priority':
                sort_field = Task.priority
            elif sort_by == 'created_at':
                sort_field = Task.created_at
            elif sort_by == 'title':
                sort_field = Task.title

            if sort_field:
                if order and order.lower() == 'desc':
                    query = query.order_by(sort_field.desc())
                else:
                    query = query.order_by(sort_field.asc())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        tasks = session.exec(query).all()

        # Add tags to each task by extending the task object with tags
        for task in tasks:
            task_tags = session.exec(select(TaskTag).where(TaskTag.task_id == task.id)).all()
            tag_ids = [str(tt.tag_id) for tt in task_tags]
            if tag_ids:
                tags = session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all()
                # Explicitly assign tags to the task object
                task.tags = tags
            else:
                task.tags = []

        return tasks