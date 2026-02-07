from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from ...models.reminder import Reminder, ReminderCreate, ReminderUpdate, ReminderRead
from ...models.user import User
from ...api.deps import get_current_user, get_session
from ...services.reminder_service import ReminderService


router = APIRouter()


@router.get("/", response_model=List[ReminderRead])
def get_user_reminders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> List[Reminder]:
    """
    Retrieve all reminders for the currently authenticated user.

    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        List of reminders belonging to the authenticated user
    """
    reminders = ReminderService.get_reminders_by_user_id(
        session=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return reminders


@router.post("/", response_model=ReminderRead)
def create_reminder(
    reminder_create: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Reminder:
    """
    Create a new reminder for the currently authenticated user.

    Args:
        reminder_create: Reminder creation data
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        The created reminder
    """
    try:
        reminder = ReminderService.create_reminder(
            session=db,
            reminder_create=reminder_create,
            user_id=current_user.id
        )
        return reminder
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the reminder"
        )


@router.get("/{reminder_id}", response_model=ReminderRead)
def get_reminder(
    reminder_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Reminder:
    """
    Retrieve a specific reminder by ID if it belongs to the authenticated user.

    Args:
        reminder_id: ID of the reminder to retrieve
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        The requested reminder

    Raises:
        HTTPException: If the reminder doesn't exist or doesn't belong to the user
    """
    reminder = ReminderService.get_reminder_by_id(
        session=db,
        reminder_id=str(reminder_id),
        user_id=current_user.id
    )
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found or does not belong to user"
        )
    return reminder


@router.put("/{reminder_id}", response_model=ReminderRead)
def update_reminder(
    reminder_id: UUID,
    reminder_update: ReminderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Reminder:
    """
    Update a specific reminder by ID if it belongs to the authenticated user.

    Args:
        reminder_id: ID of the reminder to update
        reminder_update: Reminder update data
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        The updated reminder

    Raises:
        HTTPException: If the reminder doesn't exist or doesn't belong to the user
    """
    reminder = ReminderService.update_reminder(
        session=db,
        reminder_id=str(reminder_id),
        reminder_update=reminder_update,
        user_id=current_user.id
    )
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found or does not belong to user"
        )
    return reminder


@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> dict:
    """
    Delete a specific reminder by ID if it belongs to the authenticated user.

    Args:
        reminder_id: ID of the reminder to delete
        current_user: The authenticated user making the request
        db: Database session

    Returns:
        Confirmation message

    Raises:
        HTTPException: If the reminder doesn't exist or doesn't belong to the user
    """
    success = ReminderService.delete_reminder(
        session=db,
        reminder_id=str(reminder_id),
        user_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found or does not belong to user"
        )
    return {"message": "Reminder deleted successfully"}