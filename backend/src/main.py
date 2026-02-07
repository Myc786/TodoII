from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import config FIRST to load .env before any other modules
from .core.config import ENVIRONMENT, settings
from .core import logging_config

# Now import routes (which may depend on env vars)
from .api.routes import router as api_router
from .api.routes.chat import router as chat_router
from .services.reminder_scheduler import initialize_reminder_scheduler
from .database.init_db import create_db_and_tables


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

    # Add a custom middleware to log incoming origins for debugging
    @app.middleware("http")
    async def log_origin(request: Request, call_next):
        origin = request.headers.get("origin")
        if origin:
            print(f"[DEBUG] Incoming request from origin: {origin} to {request.url.path}")
        return await call_next(request)

    # Add CORS middleware to allow frontend requests
    # Since we use JWT and not cookies, we can be more permissive to fix CORS issues
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes - all routes are consolidated in the main api_router
    # This includes /tasks, /auth, /chat, and /reminders under the /api prefix
    app.include_router(api_router, prefix="/api")

    @app.get("/health")
    def health_check():
        """Health check endpoint to verify the API is running."""
        logger = logging_config.get_logger(__name__)
        logger.info("Health check accessed")
        return {"status": "healthy", "environment": ENVIRONMENT}

    # Initialize the reminder scheduler
    initialize_reminder_scheduler()

    # Initialize database tables on startup
    @app.on_event("startup")
    async def on_startup():
        """Initialize database tables on application startup."""
        logger = logging_config.get_logger(__name__)
        logger.info("Initializing database tables...")
        try:
            create_db_and_tables()
            logger.info("Database tables initialized successfully!")
        except Exception as e:
            logger.error(f"Error initializing database tables: {e}")

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