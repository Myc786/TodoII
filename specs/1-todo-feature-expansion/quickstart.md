# Quickstart Guide: Todo App Feature Expansion

## Overview
This guide provides a quick overview of how to implement and use the intermediate and advanced features of the todo application.

## Prerequisites
- Python 3.12+ installed
- Node.js 18+ installed
- PostgreSQL database (Neon recommended)
- Better Auth configured
- Basic todo app features already implemented

## Environment Setup

### Backend Configuration
1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```env
DATABASE_URL="postgresql://username:password@localhost:5432/todoapp"
BETTER_AUTH_SECRET="your-secret-key"
BETTER_AUTH_URL="http://localhost:3000"
```

3. Run database migrations:
```bash
python -m src.main migrate
```

### Frontend Configuration
1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Set up environment variables in `.env.local`:
```env
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
```

## Running the Application

### Development Mode
1. Start the backend:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

2. Start the frontend:
```bash
cd frontend
npm run dev
```

## Key Features Implementation

### 1. Task Priority
Adding priority to tasks:

**Backend**: The `Task` model already includes a `priority` field (high/medium/low)
**Frontend**: Use the `PrioritySelector` component

Example usage:
```typescript
// Creating a task with priority
const taskData = {
  title: "Important task",
  priority: "high",  // Options: "high", "medium", "low"
  description: "This needs immediate attention"
};
```

### 2. Task Tags
Managing tags for tasks:

**Backend**: The `Tag` model and `TaskTag` association table are already implemented
**Frontend**: Use the `TagInput` and `TagManager` components

Example usage:
```typescript
// Creating a task with tags
const taskData = {
  title: "Project task",
  tag_ids: ["tag-uuid-1", "tag-uuid-2"]  // Array of tag IDs
};

// Managing tags
const tagData = {
  name: "Work",
  color: "#FF6B6B"  // Hex color
};
```

### 3. Due Dates
Setting due dates for tasks:

**Backend**: The `Task` model includes a `due_date` field
**Frontend**: Due dates are displayed in the `TaskCard` component

Example usage:
```typescript
// Creating a task with due date
const taskData = {
  title: "Meeting prep",
  due_date: "2023-12-25T10:00:00Z"  // ISO 8601 format
};
```

### 4. Search and Filtering
Using the enhanced search and filter capabilities:

**Backend**: New endpoints are available at `/api/tasks/search`
**Frontend**: Use the filter components in the UI

Example API call:
```bash
# Search tasks by keyword
GET /api/tasks/search?q=meeting&status=active&priority=high

# Filter by multiple criteria
GET /api/tasks/search?tag_ids=tag1,tag2&due_after=2023-12-01&sort_by=due_date&order=asc
```

### 5. Recurring Tasks
Creating tasks that repeat automatically:

**Backend**: The `Task` model includes a `recurrence_pattern` field
**Frontend**: Recurrence UI components need to be implemented

Example recurrence pattern:
```json
{
  "type": "weekly",
  "interval": 1,
  "days_of_week": [1, 3, 5],
  "end_date": "2024-12-31"
}
```

## API Endpoints

### Enhanced Task Endpoints
- `GET /api/tasks/search` - Search and filter tasks
- `POST /api/tasks/{task_id}/duplicate` - Duplicate a task
- `POST /api/tasks/recurrence` - Create recurring task
- `POST /api/reminders` - Create a reminder
- `DELETE /api/reminders/{reminder_id}` - Delete a reminder

### Tag Management Endpoints
- `GET /api/tags` - Get user's tags
- `POST /api/tags` - Create a new tag
- `PUT /api/tags/{tag_id}` - Update a tag
- `DELETE /api/tags/{tag_id}` - Delete a tag

## Frontend Components

### Task Components
- `TaskCard` - Displays individual tasks with priority, tags, and due dates
- `TaskForm` - Form for creating and updating tasks
- `TaskList` - List container for multiple tasks
- `TaskFilters` - Filtering controls
- `PrioritySelector` - Priority selection dropdown
- `TagInput` - Tag selection and creation input
- `TagManager` - Tag management interface

### Usage Example
```tsx
import { TaskForm, TaskList, TaskFilters } from '@/components/task';

function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [activeFilter, setActiveFilter] = useState<'all'|'active'|'completed'>('all');

  return (
    <div>
      <TaskFilters
        activeFilter={activeFilter}
        onFilterChange={setActiveFilter}
      />
      <TaskForm
        onTaskCreated={(newTask) => setTasks([newTask, ...tasks])}
      />
      <TaskList
        tasks={tasks}
        onToggle={handleToggle}
        onUpdate={handleUpdate}
        onDelete={handleDelete}
      />
    </div>
  );
}
```

## Database Schema

### Key Tables
- `task` - Main task table with priority, due_date, and recurrence fields
- `tag` - User-defined tags for organizing tasks
- `task_tag` - Junction table for many-to-many relationship between tasks and tags
- `reminder` - Scheduled reminders for tasks (to be implemented)

### Indexes
- `idx_task_user_id` - For user isolation
- `idx_task_priority` - For priority filtering
- `idx_task_due_date` - For due date queries
- `idx_task_completed` - For status filtering

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

### Common Issues
1. **Authentication errors**: Ensure JWT tokens are properly set in headers
2. **Database connection**: Verify DATABASE_URL is correct
3. **Frontend build errors**: Check that all dependencies are installed

### Debugging Tips
- Check the API documentation at `/docs` for endpoint details
- Look at the browser console for frontend errors
- Check the backend logs for server-side issues