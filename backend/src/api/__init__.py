from fastapi import APIRouter
from . import routes


# Main API router
router = routes.router


__all__ = ["router"]