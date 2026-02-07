from fastapi import APIRouter
from . import tasks, auth, chat, reminders  # Import the route modules


# Main API router
router = APIRouter()

# Include all route modules
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(chat.router, tags=["chat"])  # chat.router already has /api prefix? Wait, check chat.py
router.include_router(reminders.router, prefix="/reminders", tags=["reminders"])


__all__ = ["router"]