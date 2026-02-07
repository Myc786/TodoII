from sqlmodel import Session, create_engine
from contextlib import contextmanager
from ..core.config import get_engine


def get_session() -> Session:
    """
    Get a database session using the configured engine.

    Yields:
        Session: A SQLModel session connected to the database
    """
    engine = get_engine()
    with Session(engine) as session:
        yield session


@contextmanager
def get_session_context():
    """
    Context manager for database sessions.

    Ensures proper session cleanup after use.
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


def get_session_sync():
    """
    Synchronous generator for getting a database session.

    This function is compatible with FastAPI's dependency injection system.
    """
    engine = get_engine()
    with Session(engine) as session:
        yield session