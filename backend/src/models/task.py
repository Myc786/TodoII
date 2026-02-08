from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Index
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid
from enum import Enum

if TYPE_CHECKING:
    from .tag import Tag
    from .reminder import Reminder
    from .user import User
from .task_tag import TaskTag




class TaskStatus(str, Enum):
    """Enumeration for task statuses."""
    ACTIVE = "active"
    COMPLETED = "completed"


class PriorityLevel(str, Enum):
    """Enumeration for task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskBase(SQLModel):
    """
    Base class for Task model with common fields.
    """
    title: str = Field(nullable=False, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)  # Add index to user_id


from pydantic import ConfigDict

class Task(TaskBase, table=True):
    """
    Task model representing a todo item belonging to a specific user.

    Attributes:
        id: Unique identifier for the task
        title: Title of the task (1-200 characters)
        description: Optional description of the task
        completed: Boolean indicating if the task is completed
        user_id: Foreign key linking to the user who owns this task
        version: Integer for optimistic locking (default: 1)
        created_at: Timestamp when the task was created
        updated_at: Timestamp when the task was last updated
        priority: Priority level of the task (high, medium, low)
        due_date: Date when the task is due
        recurrence_pattern: JSON defining recurrence rules if task repeats
        original_task_id: Links to template for recurring instances
    """
    model_config = ConfigDict(from_attributes=True)
    id: Optional[uuid.UUID] = Field(default=None, primary_key=True)
    version: int = Field(default=1)  # For optimistic locking
    created_at: Optional[datetime] = Field(default=None, index=True)  # Add index to created_at
    updated_at: Optional[datetime] = Field(default=None)

    # New fields for feature expansion
    priority: Optional[str] = Field(default=PriorityLevel.MEDIUM.value, max_length=10)  # Priority level
    due_date: Optional[datetime] = Field(default=None)  # Due date for the task
    recurrence_pattern: Optional[str] = Field(default=None)  # JSON for recurrence rules
    original_task_id: Optional[uuid.UUID] = Field(default=None, foreign_key="task.id")  # For recurring tasks

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")

    # Relationship for reminders - using string references to avoid circular import
    reminders: list["Reminder"] = Relationship(back_populates="task")

    # Relationship to tags
    tags: list["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)