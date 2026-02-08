from sqlmodel import SQLModel
from sqlalchemy import text
from ..core.config import get_engine
from ..models.user import User
from ..models.task import Task
from ..models.tag import Tag
from ..models.task_tag import TaskTag
from ..models.reminder import Reminder
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.refresh_token import RefreshToken


def create_db_and_tables():
    """
    Create the database and all tables based on the SQLModel models.

    This function should be called when starting the application to ensure
    all necessary tables exist in the database.
    """
    try:
        engine = get_engine()
        
        # Check if we're using PostgreSQL
        from sqlalchemy import inspect
        inspector = inspect(engine)
        db_dialect = engine.dialect.name
        
        if db_dialect == 'postgresql':
            # For PostgreSQL, we might need to handle existing schema issues
            # Drop all existing tables to ensure clean schema
            from sqlalchemy import MetaData
            meta = MetaData()
            
            with engine.connect() as conn:
                trans = conn.begin()  # Start transaction
                try:
                    # Reflect existing tables
                    meta.reflect(bind=engine)
                    
                    # Drop all tables
                    for table in reversed(meta.sorted_tables):
                        conn.execute(text(f'DROP TABLE IF EXISTS "{table.name}" CASCADE'))
                        print(f"Dropped {table.name} table if it existed")
                    
                    trans.commit()
                    print("All existing tables dropped successfully")
                except Exception as e:
                    print(f"Error during table dropping: {e}")
                    # Continue anyway, as this might be the first run
                    trans.rollback()
        
        # Ensure all models are properly registered before creating tables
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        # Re-raise the exception to prevent the app from starting with a broken DB
        raise


if __name__ == "__main__":
    create_db_and_tables()