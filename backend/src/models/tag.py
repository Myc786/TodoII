from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .task import Task
    from .user import User
from .task_tag import TaskTag



class TagBase(SQLModel):
    """
    Base class for Tag model with common fields.
    """
    name: str = Field(nullable=False, min_length=1, max_length=50)
    color: Optional[str] = Field(default=None, max_length=7)  # Hex color code
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)


class Tag(TagBase, table=True):
    """
    Tag model representing a category or label that can be applied to tasks.

    Attributes:
        id: Unique identifier for the tag
        name: Name of the tag (1-50 characters)
        color: Optional hex color code for visual representation
        user_id: Foreign key linking to the user who owns this tag
        created_at: Timestamp when the tag was created
    """
    id: Optional[uuid.UUID] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default=None, index=True)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tags")

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="tags", link_model=TaskTag)

    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None:
            self.id = uuid.uuid4()
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class TagRead(TagBase):
    """Schema for reading tag data."""
    id: uuid.UUID
    created_at: datetime


class TagCreate(TagBase):
    """Schema for creating a new tag."""
    name: str = Field(min_length=1, max_length=50)  # Required field


class TagUpdate(SQLModel):
    """Schema for updating tag data."""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = None