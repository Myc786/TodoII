from sqlmodel import SQLModel
from ..core.config import get_engine
from ..models.user import User
from ..models.task import Task
from ..models.tag import Tag
from ..models.task_tag import TaskTag
from ..models.reminder import Reminder
from ..models.conversation import Conversation
from ..models.message import Message


def create_db_and_tables():
    """
    Create the database and all tables based on the SQLModel models.

    This function should be called when starting the application to ensure
    all necessary tables exist in the database.
    """
    engine = get_engine()
    # Ensure all models are properly registered before creating tables
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_db_and_tables()