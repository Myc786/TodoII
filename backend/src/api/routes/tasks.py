from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from uuid import UUID
from ...models.task import Task
from ...models.task_schemas import TaskCreate, TaskRead, TaskUpdate, TaskToggle
from ...api.deps import get_current_user, get_session
from ...models.user import User
from ...services.task_service import TaskService


router = APIRouter()


@router.get("/", response_model=List[TaskRead])
def get_user_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> List[Task]:
    """
    Retrieve all tasks for the currently authenticated user.

    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        List of tasks belonging to the authenticated user
    """
    tasks = TaskService.get_tasks_by_user_id(
        session=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return tasks


@router.post("/", response_model=TaskRead)
def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Task:
    """
    Create a new task for the currently authenticated user.

    Args:
        task_create: Task creation data
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        The created task
    """
    print(f"[DEBUG create_task] Called by user: {current_user.email if current_user else 'None'}")
    print(f"[DEBUG create_task] Task data: {task_create}")

    # Validate title length
    if not task_create.title or len(task_create.title.strip()) < 1 or len(task_create.title) > 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title must be between 1 and 200 characters"
        )

    try:
        task = TaskService.create_task(
            session=db,
            task_create=task_create,
            user_id=current_user.id
        )
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Task:
    """
    Retrieve a specific task by ID if it belongs to the authenticated user.

    Args:
        task_id: ID of the task to retrieve
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        The requested task

    Raises:
        HTTPException: If the task doesn't exist or doesn't belong to the user
    """
    task = TaskService.get_task_by_id(
        session=db,
        task_id=str(task_id),
        user_id=current_user.id
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Task:
    """
    Update a specific task by ID if it belongs to the authenticated user.

    Args:
        task_id: ID of the task to update
        task_update: Task update data
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        The updated task

    Raises:
        HTTPException: If the task doesn't exist or doesn't belong to the user
    """
    # Validate title if it's being updated
    if task_update.title is not None:
        if len(task_update.title.strip()) < 1 or len(task_update.title) > 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task title must be between 1 and 200 characters"
            )

    try:
        task = TaskService.update_task(
            session=db,
            task_id=str(task_id),
            task_update=task_update,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> dict:
    """
    Delete a specific task by ID if it belongs to the authenticated user.

    Args:
        task_id: ID of the task to delete
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        Confirmation message

    Raises:
        HTTPException: If the task doesn't exist or doesn't belong to the user
    """
    success = TaskService.delete_task(
        session=db,
        task_id=str(task_id),
        user_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/toggle", response_model=TaskRead)
def toggle_task_completion(
    task_id: UUID,
    toggle_data: TaskToggle,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Task:
    """
    Toggle the completion status of a specific task if it belongs to the authenticated user.

    Args:
        task_id: ID of the task to toggle
        toggle_data: Toggle data containing version for optimistic locking
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        The updated task with toggled completion status

    Raises:
        HTTPException: If the task doesn't exist, doesn't belong to the user, or version mismatch occurs
    """
    task = TaskService.toggle_task_completion(
        session=db,
        task_id=str(task_id),
        toggle_data=toggle_data,
        user_id=current_user.id
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )
    return task


@router.get("/search", response_model=List[TaskRead])
def search_and_filter_tasks(
    q: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tag_ids: Optional[str] = None,
    due_before: Optional[str] = None,
    due_after: Optional[str] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> List[Task]:
    """
    Search and filter tasks by various criteria including text, priority, tags, and due dates.

    Args:
        q: Keyword search term for title/description
        status: Filter by completion status ('active', 'completed', 'all')
        priority: Filter by priority level ('high', 'medium', 'low')
        tag_ids: Filter by tag IDs (comma-separated)
        due_before: Filter tasks due before specified date
        due_after: Filter tasks due after specified date
        sort_by: Sort by specified field ('due_date', 'priority', 'created_at', 'title')
        order: Sort order ('asc', 'desc')
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        List of tasks matching the search and filter criteria
    """
    # Parse tag_ids if provided
    parsed_tag_ids = None
    if tag_ids:
        parsed_tag_ids = [tid.strip() for tid in tag_ids.split(',') if tid.strip()]

    tasks = TaskService.search_and_filter_tasks(
        session=db,
        user_id=current_user.id,
        search_query=q,
        status=status,
        priority=priority,
        tag_ids=parsed_tag_ids,
        due_before=due_before,
        due_after=due_after,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit
    )
    return tasks