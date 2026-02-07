from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from ...models.tag import Tag, TagCreate, TagRead, TagUpdate
from ...models.task_schemas import TaskTagAssignment
from ...api.deps import get_current_user, get_session
from ...models.user import User
from ...services.task_service import TaskService

router = APIRouter()


@router.get("/", response_model=List[TagRead])
def get_user_tags(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> List[Tag]:
    """
    Retrieve all tags for the currently authenticated user.

    Args:
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        List of tags belonging to the authenticated user
    """
    from sqlmodel import select
    statement = select(Tag).where(Tag.user_id == current_user.id)
    tags = db.exec(statement).all()
    return tags


@router.post("/", response_model=TagRead)
def create_tag(
    tag_create: TagCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Tag:
    """
    Create a new tag for the currently authenticated user.

    Args:
        tag_create: Tag creation data
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        The created tag
    """
    # Validate tag name length
    if not tag_create.name or len(tag_create.name.strip()) < 1 or len(tag_create.name) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag name must be between 1 and 50 characters"
        )

    # Check if tag name already exists for this user
    from sqlmodel import select
    existing_statement = select(Tag).where(
        Tag.name == tag_create.name,
        Tag.user_id == current_user.id
    )
    existing_tag = db.exec(existing_statement).first()
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this name already exists for this user"
        )

    tag_data = tag_create.dict(exclude_unset=True)
    tag_data['user_id'] = current_user.id

    db_tag = Tag(**tag_data)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@router.get("/{tag_id}", response_model=TagRead)
def get_tag(
    tag_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Tag:
    """
    Retrieve a specific tag by ID if it belongs to the authenticated user.

    Args:
        tag_id: ID of the tag to retrieve
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        The requested tag

    Raises:
        HTTPException: If the tag doesn't exist or doesn't belong to the user
    """
    from sqlmodel import select
    statement = select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id)
    tag = db.exec(statement).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found or does not belong to user"
        )
    return tag


@router.put("/{tag_id}", response_model=TagRead)
def update_tag(
    tag_id: UUID,
    tag_update: TagUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Tag:
    """
    Update a specific tag by ID if it belongs to the authenticated user.

    Args:
        tag_id: ID of the tag to update
        tag_update: Tag update data
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        The updated tag

    Raises:
        HTTPException: If the tag doesn't exist or doesn't belong to the user
    """
    from sqlmodel import select
    statement = select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id)
    db_tag = db.exec(statement).first()
    if not db_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found or does not belong to user"
        )

    # Validate tag name if it's being updated
    if tag_update.name is not None:
        if len(tag_update.name.strip()) < 1 or len(tag_update.name) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag name must be between 1 and 50 characters"
            )

        # Check if the new name already exists for this user
        existing_statement = select(Tag).where(
            Tag.name == tag_update.name,
            Tag.user_id == current_user.id,
            Tag.id != tag_id  # Exclude the current tag from check
        )
        existing_tag = db.exec(existing_statement).first()
        if existing_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this name already exists for this user"
            )

    # Update fields that are provided
    update_data = tag_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tag, field, value)

    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@router.delete("/{tag_id}")
def delete_tag(
    tag_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> dict:
    """
    Delete a specific tag by ID if it belongs to the authenticated user.

    Args:
        tag_id: ID of the tag to delete
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        Confirmation message

    Raises:
        HTTPException: If the tag doesn't exist or doesn't belong to the user
    """
    from sqlmodel import select
    statement = select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id)
    db_tag = db.exec(statement).first()
    if not db_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found or does not belong to user"
        )

    db.delete(db_tag)
    db.commit()
    return {"message": "Tag deleted successfully"}


@router.put("/{tag_id}/tasks/{task_id}")
def assign_tag_to_task(
    tag_id: UUID,
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> dict:
    """
    Assign a tag to a task if both belong to the authenticated user.

    Args:
        tag_id: ID of the tag to assign
        task_id: ID of the task to assign the tag to
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        Confirmation message

    Raises:
        HTTPException: If the tag or task doesn't exist or don't belong to the user
    """
    # Verify that both tag and task belong to the user
    from sqlmodel import select
    tag_statement = select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id)
    tag = db.exec(tag_statement).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found or does not belong to user"
        )

    task = TaskService.get_task_by_id(db, str(task_id), current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    # Check if the tag is already assigned to the task
    from ...models.task_tag import TaskTag
    assignment_statement = select(TaskTag).where(
        TaskTag.task_id == task_id,
        TaskTag.tag_id == tag_id
    )
    existing_assignment = db.exec(assignment_statement).first()
    if existing_assignment:
        return {"message": "Tag already assigned to task"}

    # Create the assignment
    task_tag = TaskTag(task_id=task_id, tag_id=tag_id)
    db.add(task_tag)
    db.commit()
    return {"message": "Tag assigned to task successfully"}


@router.delete("/{tag_id}/tasks/{task_id}")
def remove_tag_from_task(
    tag_id: UUID,
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> dict:
    """
    Remove a tag from a task if both belong to the authenticated user.

    Args:
        tag_id: ID of the tag to remove
        task_id: ID of the task to remove the tag from
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        Confirmation message

    Raises:
        HTTPException: If the tag or task doesn't exist or don't belong to the user
    """
    # Verify that both tag and task belong to the user
    from sqlmodel import select
    tag_statement = select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id)
    tag = db.exec(tag_statement).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found or does not belong to user"
        )

    task = TaskService.get_task_by_id(db, str(task_id), current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    # Find and remove the assignment
    assignment_statement = select(TaskTag).where(
        TaskTag.task_id == task_id,
        TaskTag.tag_id == tag_id
    )
    task_tag = db.exec(assignment_statement).first()
    if not task_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag is not assigned to this task"
        )

    db.delete(task_tag)
    db.commit()
    return {"message": "Tag removed from task successfully"}