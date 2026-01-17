# Quickstart Guide: Backend & Database Foundation

## Prerequisites
- Python 3.11+
- Poetry or pip for dependency management
- PostgreSQL (or Neon Serverless instance)
- Environment variables configured (DATABASE_URL, BETTER_AUTH_SECRET)

## Setup Instructions

### 1. Clone and Initialize
```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Navigate to backend directory
cd backend
```

### 2. Install Dependencies
```bash
# Using poetry
poetry install

# Or using pip
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-jwt-secret-key-here
```

### 4. Database Setup
```bash
# Run database migrations
python -m alembic upgrade head

# Or initialize the database directly
python -c "from backend.src.database.session import engine; from backend.src.models import Base; Base.metadata.create_all(engine)"
```

### 5. Run the Application
```bash
# Using uvicorn
uvicorn backend.src.main:app --reload --port 8000

# Or using the run script if available
python -m backend.src.main
```

## API Endpoints

### Task Management
- `GET /api/tasks` - List all tasks for authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a specific task
- `PATCH /api/tasks/{task_id}/toggle` - Toggle task completion status
- `DELETE /api/tasks/{task_id}` - Delete a specific task

### Authentication
- `POST /api/auth/login` - User login (handled by Better Auth)
- `POST /api/auth/logout` - User logout (handled by Better Auth)

## Testing the API

### Using FastAPI Documentation
1. Start the server
2. Navigate to `http://localhost:8000/docs`
3. Use the interactive API documentation to test endpoints

### Using curl
```bash
# Get all tasks (requires JWT token)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/tasks

# Create a new task (requires JWT token)
curl -X POST -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Sample task", "description": "Task description"}' \
  http://localhost:8000/api/tasks
```

## Key Features
- JWT-based authentication with shared secret
- User data isolation (each user only sees their own tasks)
- Optimistic locking for concurrent task updates
- Input validation (title length 1-200 characters)
- Proper error handling (404 for not found, 400 for bad requests)