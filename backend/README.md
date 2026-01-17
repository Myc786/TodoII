# Todo Backend API

Backend API for the Todo application built with FastAPI and SQLModel.

## Features

- JWT-based authentication
- Full CRUD operations for tasks
- User isolation (users only see their own tasks)
- Optimistic locking for concurrent task modifications
- Input validation
- Error handling

## Tech Stack

- Python 3.11
- FastAPI
- SQLModel
- PostgreSQL (Neon Serverless)
- JWT for authentication

## Setup

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or using Poetry:

```bash
poetry install
```

3. Create a `.env` file with the required environment variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your_jwt_secret_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
```

4. Run the application:

```bash
python -m src.main
```

Or using uvicorn:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

API documentation is automatically available at:
- `/docs` - Interactive Swagger UI
- `/redoc` - ReDoc documentation
- `/openapi.json` - OpenAPI specification

## Endpoints

- `GET /api/tasks` - List all tasks for authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a specific task
- `PATCH /api/tasks/{task_id}/toggle` - Toggle task completion status
- `DELETE /api/tasks/{task_id}` - Delete a specific task
- `GET /health` - Health check endpoint

## Environment Variables

- `DATABASE_URL`: Database connection string
- `BETTER_AUTH_SECRET`: JWT secret key for token signing/verification
- `ENVIRONMENT`: Environment mode (development, production)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Running Tests

Unit and integration tests can be run using pytest:

```bash
pytest
```

## Database Initialization

The database tables are created automatically when the application starts through the init_db.py script.