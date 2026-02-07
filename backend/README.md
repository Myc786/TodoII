---
title: Todo API Backend
emoji: 📝
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# Todo API Backend

A FastAPI-based backend for managing todo tasks with user authentication.

## Features

- User authentication with JWT tokens
- Task management (CRUD operations)
- Tags and reminders support
- Chat integration with AI
- RESTful API design

## Deployment

### Hugging Face Spaces

This backend is deployed on Hugging Face Spaces using Docker.

**Space URL:** https://huggingface.co/spaces/myc786/Part2

**API Base URL:** https://myc786-part2.hf.space

### Environment Variables

Set these in your Hugging Face Space settings:

- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT secret key for authentication
- `ENVIRONMENT`: Set to `production`
- `OPENAI_API_KEY`: (Optional) For AI chat features

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn src.main:app --reload --port 8000
```

## API Endpoints

- `GET /health` - Health check
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/tasks` - List tasks
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `GET /api/tags` - List tags
- `POST /api/chat` - Chat with AI assistant

## License

MIT
