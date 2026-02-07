# Quickstart Guide: Frontend UI & API Integration

## Prerequisites
- Node.js 18+ (LTS recommended)
- npm or yarn package manager
- Access to the FastAPI backend running on http://localhost:8000/api
- Environment variables configured (NEXT_PUBLIC_API_URL)

## Setup Instructions

### 1. Clone and Initialize
```bash
# Navigate to frontend directory
cd frontend
```

### 2. Install Dependencies
```bash
# Using npm
npm install

# Or using yarn
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Todo App
```

### 4. Run the Application
```bash
# Development mode
npm run dev

# Or using yarn
yarn dev
```

The application will start on `http://localhost:3000`

## Key Components

### API Client
Located at `src/lib/api.ts`, this centralized client handles all communication with the backend:
- `getTasks()` - Fetch all tasks for the authenticated user
- `createTask(data)` - Create a new task
- `updateTask(id, data)` - Update an existing task
- `deleteTask(id)` - Delete a task
- `toggleTaskCompletion(id, version)` - Toggle task completion status

### UI Components
Reusable components located in `src/components/`:
- `TaskCard` - Displays individual task with title, description, and completion status
- `TaskList` - Container for multiple TaskCards with loading states
- `TaskForm` - Form for creating new tasks with validation
- `StatusBadge` - Visual indicator for task completion status

### Hooks
Custom React hooks in `src/hooks/`:
- `useToast` - Manages toast notifications for user feedback

## Testing the Application

### Connectivity Check
1. Start the FastAPI backend server
2. Start the Next.js frontend server
3. Navigate to the dashboard
4. Check the browser's Network tab for successful 200 OK responses from the backend

### Feature Testing
- **Add Task**: Use the form to add a new task and verify it appears in the list
- **Toggle Completion**: Click the toggle button on a task and verify the status changes
- **Responsive Design**: Test the layout on different screen sizes
- **Empty State**: Clear the database to verify the "No tasks found" message displays correctly

## Key Features
- Responsive Todo Dashboard built with Next.js 15+ App Router and Tailwind CSS
- Optimistic UI updates for immediate feedback when toggling tasks
- Centralized API client for communication with FastAPI backend
- Reusable UI components for consistent design
- Loading states and empty-list illustrations
- Toast notifications for error handling