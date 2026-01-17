import os
from typing import Optional
from sqlmodel import create_engine
from sqlalchemy import event
from sqlalchemy.pool import Pool, StaticPool


# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Engine configuration
engine_kwargs = {}

if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL-specific configuration
    engine_kwargs.update({
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "pool_recycle": 300,
    })
elif DATABASE_URL.startswith("sqlite"):
    # SQLite-specific configuration
    engine_kwargs.update({
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    })

# Create the database engine
engine = create_engine(DATABASE_URL, **engine_kwargs)


def get_engine():
    """Return the database engine instance."""
    return engine