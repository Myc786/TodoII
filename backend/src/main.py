from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.routes import router as api_router
from src.core.config import ENVIRONMENT
from src.core import logging_config
from src.services.reminder_scheduler import initialize_reminder_scheduler
import logging


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="Todo API",
        description="API for managing todo tasks with user authentication",
        version="1.0.0",
        debug=(ENVIRONMENT == "development")
    )

    # Add CORS middleware to allow frontend requests
    if ENVIRONMENT == "development":
        # Allow all origins in development
        allowed_origins = ["*"]
    else:
        # Production: Restrict to specific frontend domains
        allowed_origins = [
            "https://frontend-mocha-beta-73.vercel.app",
            "https://frontend-qmwqrks1n-myc786s-projects.vercel.app",
            "http://localhost:3000",
            "http://localhost:3001"
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router, prefix="/api", tags=["tasks"])

    @app.get("/health")
    def health_check():
        """Health check endpoint to verify the API is running."""
        logger = logging_config.get_logger(__name__)
        logger.info("Health check accessed")
        return {"status": "healthy", "environment": ENVIRONMENT}

    # Initialize the reminder scheduler
    initialize_reminder_scheduler()

    return app


# Create the main application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=(ENVIRONMENT == "development")
    )