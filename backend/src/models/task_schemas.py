from sqlmodel import SQLModel
from typing import Optional, List
from datetime import datetime
import uuid
from ..models.reminder import ReminderType
from typing import TYPE_CHECKING
from ..models.tag import TagRead



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
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    recurrence_pattern: Optional[str] = None
    tag_ids: Optional[List[str]] = []


class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: uuid.UUID
    version: int
    created_at: datetime
    updated_at: datetime
    user_id: uuid.UUID
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    recurrence_pattern: Optional[str] = None
    tags: Optional[List["TagRead"]] = []  # Changed to strictly typed list


class TaskUpdate(SQLModel):
    """Schema for updating task data."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence_pattern: Optional[str] = None
    tag_ids: Optional[List[str]] = None
    version: Optional[int] = None  # Required for optimistic locking


class TaskToggle(SQLModel):
    """Schema for toggling task completion status."""
    version: int  # Required for optimistic locking


class TagBase(SQLModel):
    """
    Base class for Tag model with common fields.
    """
    name: str
    color: Optional[str] = None  # Hex color code
    user_id: uuid.UUID


class TagCreate(TagBase):
    """Schema for creating a new tag."""
    name: str  # Required field





class TagUpdate(SQLModel):
    """Schema for updating tag data."""
    name: Optional[str] = None
    color: Optional[str] = None


class TaskTagAssignment(SQLModel):
    """Schema for assigning tags to a task."""
    tag_ids: List[str]


class CreateReminderRequest(SQLModel):
    """Schema for creating a new reminder."""
    task_id: str  # UUID as string
    reminder_time: datetime
    reminder_type: Optional[ReminderType] = ReminderType.BROWSER_NOTIFICATION


class UpdateReminderRequest(SQLModel):
    """Schema for updating an existing reminder."""
    reminder_time: Optional[datetime] = None
    reminder_type: Optional[ReminderType] = None