from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid


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
        created_at: Timestamp when the user was created
        updated_at: Timestamp when the user was last updated
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


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