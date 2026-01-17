from fastapi import HTTPException, status


class TaskNotFoundException(HTTPException):
    """Exception raised when a task is not found."""
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )


class TaskConflictException(HTTPException):
    """Exception raised when there's a conflict during task update (optimistic locking)."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task was updated by another request. Please refresh and try again."
        )


class ValidationErrorException(HTTPException):
    """Exception raised when there's a validation error."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


# Predefined exceptions for common scenarios
def get_task_not_found_exception(task_id: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {task_id} not found"
    )


def get_validation_error_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )


def get_conflict_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Resource conflict. Please refresh and try again."
    )