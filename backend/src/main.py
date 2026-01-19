from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.routes import router as api_router
from src.core.config import ENVIRONMENT
from src.core import logging_config
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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
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