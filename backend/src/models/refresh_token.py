from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .user import User


class RefreshToken(SQLModel, table=True):
    """
    RefreshToken model for storing user refresh tokens.

    Attributes:
        id: Unique identifier for the refresh token
        token: The actual refresh token string (unique, indexed)
        user_id: Foreign key reference to the user
        expires_at: Expiration timestamp for the token
        created_at: Timestamp when the token was created
        revoked: Boolean indicating if token has been revoked
        revoked_at: Timestamp when token was revoked (if applicable)
        device_info: Optional device/client information for tracking
    """
    __tablename__ = "refresh_tokens"

    id: Optional[uuid.UUID] = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True, nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    expires_at: datetime = Field(nullable=False, index=True)
    created_at: Optional[datetime] = Field(default=None, nullable=False)
    revoked: bool = Field(default=False, nullable=False, index=True)
    revoked_at: Optional[datetime] = Field(default=None)
    device_info: Optional[str] = Field(default=None, max_length=500)

    # Relationship to user
    user: "User" = Relationship(back_populates="refresh_tokens")

    def is_valid(self) -> bool:
        """Check if the refresh token is still valid."""
        return not self.revoked and self.expires_at > datetime.utcnow()

    def revoke(self) -> None:
        """Revoke this refresh token."""
        self.revoked = True
        self.revoked_at = datetime.utcnow()
