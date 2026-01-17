from fastapi import APIRouter
from . import tasks, auth  # Import the route modules


# Main API router
router = APIRouter()

# Include all route modules
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])


__all__ = ["router"]