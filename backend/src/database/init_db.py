from sqlmodel import SQLModel
from .session import get_engine
from ..models.user import User
from ..models.task import Task


def create_db_and_tables():
    """
    Create the database and all tables based on the SQLModel models.

    This function should be called when starting the application to ensure
    all necessary tables exist in the database.
    """
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_db_and_tables()