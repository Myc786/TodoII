"""
Test script to verify all CRUD endpoints for tasks.
"""
import asyncio
import sys
from sqlmodel import Session, select

from src.database.session import get_session, get_session_context
from src.models.user import User
from src.models.task import Task
from src.services.task_service import TaskService
from src.database.init_db import create_db_and_tables
from src.core.security import get_password_hash


def test_crud_operations():
    """
    Test all CRUD operations for tasks.
    """
    print("Setting up database for testing...")
    create_db_and_tables()

    # Create a session
    with get_session_context() as session:
        # Check for existing test user and delete if exists
        existing_user = session.exec(select(User).where(User.email == "crud-test@example.com")).first()
        if existing_user:
            print("Found existing test user, cleaning up...")
            # Delete tasks first to avoid FK constraint issues if cascade isn't set
            tasks = TaskService.get_tasks_by_user_id(session, existing_user.id)
            for t in tasks:
                TaskService.delete_task(session, str(t.id), existing_user.id)
            session.delete(existing_user)
            session.commit()

        # Create a test user
        user_data = User(
            email="crud-test@example.com",
            name="CRUD Test User"
        )
        session.add(user_data)
        session.commit()
        session.refresh(user_data)

        print(f"Created test user: {user_data.name}")

        # Test CREATE operation
        from src.models.task_schemas import TaskCreate
        task_create_data = TaskCreate(
            title="Test CRUD Task",
            description="This is a test task for CRUD operations",
            completed=False
        )

        created_task = TaskService.create_task(
            session=session,
            task_create=task_create_data,
            user_id=user_data.id
        )
        print(f"Created task: {created_task.title}")

        # Test READ (single) operation
        retrieved_task = TaskService.get_task_by_id(
            session=session,
            task_id=created_task.id,
            user_id=user_data.id
        )
        if retrieved_task:
            print(f"Retrieved task: {retrieved_task.title}")
        else:
            print("Failed to retrieve task")

        # Test READ (multiple) operation
        user_tasks = TaskService.get_tasks_by_user_id(
            session=session,
            user_id=user_data.id
        )
        print(f"Found {len(user_tasks)} tasks for user")

        # Test UPDATE operation
        from src.models.task_schemas import TaskUpdate
        task_update_data = TaskUpdate(
            title="Updated CRUD Task",
            description="This task has been updated",
            completed=True,
            version=created_task.version
        )

        updated_task = TaskService.update_task(
            session=session,
            task_id=created_task.id,
            task_update=task_update_data,
            user_id=user_data.id
        )
        if updated_task:
            print(f"Updated task: {updated_task.title}, completed: {updated_task.completed}")
        else:
            print("Failed to update task")

        # Test TOGGLE operation
        from src.models.task_schemas import TaskToggle
        toggle_data = TaskToggle(version=updated_task.version)

        toggled_task = TaskService.toggle_task_completion(
            session=session,
            task_id=updated_task.id,
            toggle_data=toggle_data,
            user_id=user_data.id
        )
        if toggled_task:
            print(f"Toggled task: {toggled_task.title}, now completed: {toggled_task.completed}")
        else:
            print("Failed to toggle task")

        # Test DELETE operation
        delete_success = TaskService.delete_task(
            session=session,
            task_id=created_task.id,
            user_id=user_data.id
        )
        if delete_success:
            print("Successfully deleted task")
        else:
            print("Failed to delete task")

        # Verify deletion by trying to retrieve again
        deleted_task = TaskService.get_task_by_id(
            session=session,
            task_id=created_task.id,
            user_id=user_data.id
        )
        if not deleted_task:
            print("Verified task was deleted")

        # --- REPRODUCTION ATTEMPT: Invalid Tag ID ---
        print("\n--- Testing Invalid Tag ID ---")
        try:
             # Create a task with invalid tag ID
            invalid_tag_task_data = TaskCreate(
                title="Task with Invalid Tag",
                description="Should fail gracefully",
                tag_ids=["not-a-uuid"]
            )
            TaskService.create_task(
                session=session,
                task_create=invalid_tag_task_data,
                user_id=user_data.id
            )
            print("ERROR: Task created with invalid tag ID (Expected failure)")
        except ValueError as e:
            print(f"Caught expected ValueError: {e}")
        except Exception as e:
             print(f"Caught unexpected exception: {type(e).__name__}: {e}")

        # Clean up: delete the test user
        session.delete(user_data)
        session.commit()

        print("CRUD operations test completed successfully!")


if __name__ == "__main__":
    test_crud_operations()