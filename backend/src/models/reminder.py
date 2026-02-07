from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum


class ReminderType(str, Enum):
    """Enumeration for reminder types."""
    EMAIL = "email"
    BROWSER_NOTIFICATION = "browser_notification"
    BOTH = "both"


class ReminderBase(SQLModel):
    """
    Base class for Reminder model with common fields.
    """
    task_id: uuid.UUID = Field(foreign_key="task.id", index=True)
    reminder_time: datetime = Field(sa_column_kwargs={"index": True})  # Add index for efficient querying
    reminder_type: ReminderType = Field(default=ReminderType.BROWSER_NOTIFICATION)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)


class Reminder(ReminderBase, table=True):
    """
    Reminder model representing scheduled notifications for tasks.

    Attributes:
        id: Unique identifier for the reminder
        task_id: Foreign key linking to the task being reminded about
        reminder_time: Time when the reminder should be sent
        reminder_type: Type of reminder (email, browser notification, or both)
        user_id: Foreign key linking to the user who owns this reminder
        created_at: Timestamp when the reminder was created
        sent_at: Timestamp when the reminder was sent (null if not sent yet)
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, index=True)  # Add index for chronological queries
    sent_at: Optional[datetime] = Field(default=None)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="reminders")

    # Relationship to task
    task: Optional["Task"] = Relationship(back_populates="reminders")


class ReminderRead(ReminderBase):
    """Schema for reading reminder data."""
    id: uuid.UUID
    created_at: datetime
    sent_at: Optional[datetime]


class ReminderCreate(ReminderBase):
    """Schema for creating a new reminder."""
    task_id: uuid.UUID  # Required field
    reminder_time: datetime  # Required field
    reminder_type: ReminderType = ReminderType.BROWSER_NOTIFICATION  # Default value


class ReminderUpdate(SQLModel):
    """Schema for updating reminder data."""
    reminder_time: Optional[datetime] = None
    reminder_type: Optional[ReminderType] = None
    sent_at: Optional[datetime] = None