from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime
from ..models.reminder import Reminder, ReminderCreate, ReminderUpdate
from ..models.task import Task
from ..models.user import User


class ReminderService:
    """
    Service class for handling reminder-related operations with user isolation.
    """

    @staticmethod
    def create_reminder(session: Session, reminder_create: ReminderCreate, user_id: UUID) -> Reminder:
        """
        Create a new reminder for a task belonging to the user.

        Args:
            session: Database session
            reminder_create: Reminder creation data
            user_id: ID of the user creating the reminder

        Returns:
            The created reminder
        """
        # Verify that the task belongs to the user
        task_statement = select(Task).where(Task.id == reminder_create.task_id, Task.user_id == user_id)
        task = session.exec(task_statement).first()
        if not task:
            raise ValueError("Task not found or does not belong to user")

        # Create reminder object
        reminder_data = reminder_create.dict(exclude_unset=True)
        reminder_data['user_id'] = user_id
        reminder_data['id'] = uuid.uuid4()

        db_reminder = Reminder(**reminder_data)
        session.add(db_reminder)
        session.commit()
        session.refresh(db_reminder)

        return db_reminder

    @staticmethod
    def get_reminder_by_id(session: Session, reminder_id: str, user_id: UUID) -> Optional[Reminder]:
        """
        Retrieve a specific reminder by ID if it belongs to the specified user.

        Args:
            session: Database session
            reminder_id: ID of the reminder to retrieve
            user_id: ID of the user who should own the reminder

        Returns:
            The reminder if found and owned by the user, None otherwise
        """
        statement = select(Reminder).where(Reminder.id == UUID(reminder_id), Reminder.user_id == user_id)
        reminder = session.exec(statement).first()
        return reminder

    @staticmethod
    def get_reminders_by_user_id(session: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Reminder]:
        """
        Retrieve all reminders for a specific user with pagination.

        Args:
            session: Database session
            user_id: ID of the user whose reminders to retrieve
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return (for pagination)

        Returns:
            List of reminders belonging to the user
        """
        statement = select(Reminder).where(Reminder.user_id == user_id).offset(skip).limit(limit)
        reminders = session.exec(statement).all()
        return reminders

    @staticmethod
    def get_upcoming_reminders(session: Session, user_id: UUID, current_time: datetime) -> List[Reminder]:
        """
        Retrieve all upcoming reminders for a user that haven't been sent yet.

        Args:
            session: Database session
            user_id: ID of the user whose reminders to retrieve
            current_time: Current time to compare against reminder times

        Returns:
            List of upcoming reminders that haven't been sent yet
        """
        statement = select(Reminder).where(
            Reminder.user_id == user_id,
            Reminder.reminder_time <= current_time,
            Reminder.sent_at.is_(None)
        )
        reminders = session.exec(statement).all()
        return reminders

    @staticmethod
    def update_reminder(session: Session, reminder_id: str, reminder_update: ReminderUpdate, user_id: UUID) -> Optional[Reminder]:
        """
        Update a specific reminder if it belongs to the specified user.

        Args:
            session: Database session
            reminder_id: ID of the reminder to update
            reminder_update: Reminder update data
            user_id: ID of the user who owns the reminder

        Returns:
            The updated reminder if successful, None if reminder not found or doesn't belong to user
        """
        db_reminder = ReminderService.get_reminder_by_id(session, reminder_id, user_id)
        if not db_reminder:
            return None

        # Update fields that are provided
        update_data = reminder_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reminder, field, value)

        session.add(db_reminder)
        session.commit()
        session.refresh(db_reminder)

        return db_reminder

    @staticmethod
    def delete_reminder(session: Session, reminder_id: str, user_id: UUID) -> bool:
        """
        Delete a specific reminder if it belongs to the specified user.

        Args:
            session: Database session
            reminder_id: ID of the reminder to delete
            user_id: ID of the user who owns the reminder

        Returns:
            True if the reminder was deleted, False if reminder not found or doesn't belong to user
        """
        db_reminder = ReminderService.get_reminder_by_id(session, reminder_id, user_id)
        if not db_reminder:
            return False

        session.delete(db_reminder)
        session.commit()
        return True

    @staticmethod
    def mark_reminder_as_sent(session: Session, reminder_id: str, user_id: UUID) -> bool:
        """
        Mark a reminder as sent by updating its sent_at timestamp.

        Args:
            session: Database session
            reminder_id: ID of the reminder to mark as sent
            user_id: ID of the user who owns the reminder

        Returns:
            True if successfully marked as sent, False otherwise
        """
        db_reminder = ReminderService.get_reminder_by_id(session, reminder_id, user_id)
        if not db_reminder:
            return False

        db_reminder.sent_at = datetime.utcnow()
        session.add(db_reminder)
        session.commit()
        session.refresh(db_reminder)

        return True