from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Index
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum


class TaskStatus(str, Enum):
    """Enumeration for task statuses."""
    ACTIVE = "active"
    COMPLETED = "completed"


class TaskBase(SQLModel):
    """
    Base class for Task model with common fields.
    """
    title: str = Field(nullable=False, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)  # Add index to user_id


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
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    version: int = Field(default=1)  # For optimistic locking
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, index=True)  # Add index to created_at
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")


class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: uuid.UUID
    version: int
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    title: str = Field(min_length=1, max_length=200)  # Required field


class TaskUpdate(SQLModel):
    """Schema for updating task data."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None
    version: Optional[int] = None  # Required for optimistic locking


class TaskToggle(SQLModel):
    """Schema for toggling task completion status."""
    version: int  # Required for optimistic locking