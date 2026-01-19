import os
from typing import Optional
from sqlmodel import create_engine
from sqlalchemy import event
from sqlalchemy.pool import Pool, StaticPool


class Settings:
    """Application settings configuration."""

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Engine configuration
    @property
    def engine_kwargs(self):
        kwargs = {}

        if self.DATABASE_URL.startswith("postgresql"):
            # PostgreSQL-specific configuration
            kwargs.update({
                "pool_size": 5,
                "max_overflow": 10,
                "pool_pre_ping": True,
                "pool_recycle": 300,
            })
        elif self.DATABASE_URL.startswith("sqlite"):
            # SQLite-specific configuration
            kwargs.update({
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            })

        return kwargs

    @property
    def engine(self):
        """Return the database engine instance."""
        return create_engine(self.DATABASE_URL, **self.engine_kwargs)


# Create settings instance
settings = Settings()

# For backward compatibility, also define the old constants
DATABASE_URL = settings.DATABASE_URL
ENVIRONMENT = settings.ENVIRONMENT
engine = settings.engine


def get_engine():
    """Return the database engine instance."""
    return engine