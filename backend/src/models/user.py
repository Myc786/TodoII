from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .reminder import Reminder
    from .task import Task
    from .tag import Tag
    from .refresh_token import RefreshToken


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: str = Field(nullable=False, min_length=1, max_length=100)


class User(UserBase, table=True):
    """
    User model representing an authenticated user in the system.

    Attributes:
        id: Unique identifier for the user
        email: User's email address (used for authentication)
        name: User's display name
        password: Hashed password for authentication
        created_at: Timestamp when the user was created
        updated_at: Timestamp when the user was last updated
    """
    id: Optional[uuid.UUID] = Field(default=None, primary_key=True)
    password: Optional[str] = Field(default=None)  # Store hashed password
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    # Relationship to reminders
    reminders: List["Reminder"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    # Relationship to tags
    tags: List["Tag"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    # Relationship to refresh tokens
    refresh_tokens: List["RefreshToken"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class UserRead(UserBase):
    """Schema for reading user data."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_verified: bool


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str  # Adding password field for user creation


class UserUpdate(SQLModel):
    """Schema for updating user data."""
    email: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserPublic(UserBase):
    """Public-facing user schema without sensitive data."""
    id: uuid.UUID
    created_at: datetime