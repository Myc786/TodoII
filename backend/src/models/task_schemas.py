from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(SQLModel):
    """
    Base class for Task model with common fields.
    """
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    title: str  # Required field, validated for length in routes


class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: uuid.UUID
    version: int
    created_at: datetime
    updated_at: datetime
    user_id: uuid.UUID


class TaskUpdate(SQLModel):
    """Schema for updating task data."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    version: Optional[int] = None  # Required for optimistic locking


class TaskToggle(SQLModel):
    """Schema for toggling task completion status."""
    version: int  # Required for optimistic locking