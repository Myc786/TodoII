#!/usr/bin/env python3
"""
Script to fix the Task model for proper SQLModel usage
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Index
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum
from src.models.user import User


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
    id: Optional[uuid.UUID] = Field(default=None, primary_key=True)
    version: int = Field(default=1)  # For optimistic locking
    created_at: Optional[datetime] = Field(default=None, index=True)  # Add index to created_at
    updated_at: Optional[datetime] = Field(default=None)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")

    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None:
            self.id = uuid.uuid4()
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


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


if __name__ == "__main__":
    print("Fixed Task model defined successfully!")