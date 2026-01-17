"""
Test script to verify database connectivity and basic CRUD operations.
"""
import asyncio
from sqlmodel import Session
from src.database.session import get_session
from src.models.user import User, UserCreate
from src.models.task import Task, TaskCreate
from src.database.init_db import create_db_and_tables
from src.core.security import get_password_hash


def test_database_connectivity():
    """
    Test database connectivity by creating sample data.
    """
    print("Creating database tables...")
    create_db_and_tables()

    print("Testing database connectivity and basic operations...")

    # Create a session
    with get_session() as session:
        # Create a test user
        user_data = UserCreate(
            email="test@example.com",
            name="Test User",
            password="testpassword"
        )

        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create user object
        db_user = User(
            email=user_data.email,
            name=user_data.name,
        )

        # Add user to session and commit
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        print(f"Created user: {db_user.name} ({db_user.email})")

        # Create a test task for the user
        task_data = TaskCreate(
            title="Test Task",
            description="This is a test task",
            completed=False,
            user_id=db_user.id
        )

        # Create task object
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            user_id=task_data.user_id
        )

        # Add task to session and commit
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        print(f"Created task: {db_task.title} for user {db_user.name}")

        # Retrieve the task to verify it was stored correctly
        retrieved_task = session.get(Task, db_task.id)
        if retrieved_task:
            print(f"Retrieved task: {retrieved_task.title}")
        else:
            print("Failed to retrieve task")

        # Retrieve all tasks for the user
        user_tasks = session.query(Task).filter(Task.user_id == db_user.id).all()
        print(f"Found {len(user_tasks)} tasks for user {db_user.name}")

        # Clean up - delete test data
        session.delete(retrieved_task)
        session.delete(db_user)
        session.commit()

        print("Test completed successfully!")


if __name__ == "__main__":
    test_database_connectivity()