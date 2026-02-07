from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime, timedelta
from ..models.task import Task
from ..models.task_schemas import TaskCreate


class RecurringTaskService:
    """
    Service class for handling recurring task operations.
    """

    @staticmethod
    def create_recurring_task(session: Session, task_create: TaskCreate, user_id: UUID) -> Task:
        """
        Create a new recurring task template.

        Args:
            session: Database session
            task_create: Task creation data including recurrence pattern
            user_id: ID of the user creating the task

        Returns:
            The created recurring task template
        """
        # Create task object with the specified user_id
        task_data = task_create.dict(exclude_unset=True)
        task_data['user_id'] = user_id
        task_data['version'] = 1  # Initialize version for optimistic locking

        # Remove tag_ids from task_data as it's not part of the Task model
        tag_ids = task_data.pop('tag_ids', [])

        db_task = Task(**task_data)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Handle tag assignments if provided
        if tag_ids:
            from .task_service import TaskService
            TaskService._assign_tags_to_task(session, db_task.id, tag_ids)

        # Add tags to the refreshed task object
        if tag_ids:
            from ..models.tag import Tag
            from ..models.task_tag import TaskTag
            tag_objects = session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all()
            db_task.tags = tag_objects

        return db_task

    @staticmethod
    def generate_next_instance(session: Session, completed_task: Task) -> Optional[Task]:
        """
        Generate the next instance of a recurring task based on the recurrence pattern.

        Args:
            session: Database session
            completed_task: The completed task that should generate a new instance

        Returns:
            The new task instance if created, None otherwise
        """
        if not completed_task.recurrence_pattern:
            return None

        try:
            import json
            pattern = json.loads(completed_task.recurrence_pattern)

            # Determine the next occurrence based on the pattern
            next_due_date = RecurringTaskService._calculate_next_occurrence(
                completed_task.due_date, pattern
            )

            if next_due_date is None:
                return None

            # Create a new task with the same properties as the template
            new_task = Task(
                title=completed_task.title,
                description=completed_task.description,
                user_id=completed_task.user_id,
                priority=completed_task.priority,
                due_date=next_due_date,
                recurrence_pattern=completed_task.recurrence_pattern,
                original_task_id=completed_task.original_task_id or completed_task.id,
                version=1,
                completed=False
            )

            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            # Copy tags from the original task to the new instance
            if completed_task.tags:
                from .task_service import TaskService
                tag_ids = [tag.id for tag in completed_task.tags]
                TaskService._assign_tags_to_task(session, new_task.id, tag_ids)

            # Refresh the new task with its tags
            from ..models.tag import Tag
            from ..models.task_tag import TaskTag
            new_task_tags = session.exec(select(TaskTag).where(TaskTag.task_id == new_task.id)).all()
            tag_ids = [str(tt.tag_id) for tt in new_task_tags]
            if tag_ids:
                tags = session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all()
                new_task.tags = tags

            return new_task
        except Exception as e:
            print(f"Error generating next recurring task instance: {e}")
            return None

    @staticmethod
    def _calculate_next_occurrence(current_due_date: Optional[datetime], pattern: dict) -> Optional[datetime]:
        """
        Calculate the next occurrence date based on the recurrence pattern.

        Args:
            current_due_date: The current due date
            pattern: The recurrence pattern dictionary

        Returns:
            The next occurrence date, or None if no further occurrences
        """
        if not current_due_date:
            # If no due date is set, we can't calculate recurrence
            return None

        recurrence_type = pattern.get('type', 'daily')
        interval = pattern.get('interval', 1)

        if recurrence_type == 'daily':
            return current_due_date + timedelta(days=interval)
        elif recurrence_type == 'weekly':
            return current_due_date + timedelta(weeks=interval)
        elif recurrence_type == 'monthly':
            # For monthly recurrence, we need to handle day-of-month carefully
            # This is a simplified implementation - in production, you might want to handle edge cases
            try:
                import calendar
                year = current_due_date.year
                month = current_due_date.month + interval
                day = current_due_date.day

                # Handle year overflow
                while month > 12:
                    year += 1
                    month -= 12

                # Handle day overflow (e.g., Jan 31 + 1 month = Feb 31, which doesn't exist)
                max_day = calendar.monthrange(year, month)[1]
                if day > max_day:
                    day = max_day

                return current_due_date.replace(year=year, month=month, day=day)
            except ValueError:
                # If the calculated date is invalid, return None
                return None
        elif recurrence_type == 'custom':
            # Custom patterns can be more complex and might include end conditions
            end_date_str = pattern.get('end_date')
            if end_date_str:
                try:
                    from datetime import datetime
                    end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                    if current_due_date >= end_date:
                        return None  # No more occurrences after end date
                except ValueError:
                    pass  # Invalid end date, continue with calculation

            occurrences = pattern.get('occurrences')
            if occurrences is not None:
                # This would require tracking how many times the task has recurred
                # For now, we'll just return the next occurrence without checking limits
                pass

            # For custom patterns, use the interval to determine next occurrence
            # This is a simplified approach - a full implementation would handle more complex patterns
            return current_due_date + timedelta(days=interval)

        # Unknown recurrence type
        return None

    @staticmethod
    def handle_task_completion(session: Session, completed_task: Task) -> Optional[Task]:
        """
        Handle the completion of a task, creating a new instance if it's recurring.

        Args:
            session: Database session
            completed_task: The task that was completed

        Returns:
            The new recurring task instance if created, None otherwise
        """
        if completed_task.recurrence_pattern:
            return RecurringTaskService.generate_next_instance(session, completed_task)
        return None