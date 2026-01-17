# Todo Frontend Application

A responsive todo application built with Next.js 15+ App Router, TypeScript, and Tailwind CSS.

## Features

- Responsive dashboard with mobile-friendly design
- Task management (create, read, update, delete)
- Toggle task completion status with optimistic UI updates
- Loading states and empty state illustrations
- Error handling with toast notifications
- Integration with FastAPI backend

## Tech Stack

- Next.js 15+ (App Router)
- React 18+
- TypeScript 5.x
- Tailwind CSS 3.x
- Lucide React (icons)
- Radix UI (accessible components)
- shadcn/ui (component patterns)

## Setup

1. Clone the repository
2. Install dependencies:

```bash
npm install
```

3. Create a `.env.local` file based on `.env.example`:

```bash
cp .env.example .env.local
```

4. Update the `NEXT_PUBLIC_API_URL` in `.env.local` to point to your backend API

5. Run the development server:

```bash
npm run dev
```

The application will start on `http://localhost:3000`

## Environment Variables

- `NEXT_PUBLIC_API_URL`: URL of the backend API (e.g., http://localhost:8000/api)

## Scripts

- `npm run dev`: Start development server
- `npm run build`: Build the application for production
- `npm run start`: Start production server
- `npm run lint`: Run linter

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── app/               # Next.js App Router pages
│   ├── components/        # Reusable UI components
│   │   ├── ui/           # Base UI components (buttons, cards, etc.)
│   │   ├── task/         # Task-specific components
│   │   └── layout/       # Layout components
│   ├── lib/              # Utilities and API client
│   ├── hooks/            # Custom React hooks
│   └── styles/           # Global styles
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── .env.example
```

## API Integration

The application communicates with the backend API through the centralized API client in `src/lib/api.ts`. All API calls include proper error handling and authentication headers.

## Components

- `TaskCard`: Displays individual tasks with title, description, and completion status
- `TaskForm`: Form for creating new tasks with validation
- `TaskList`: Container for multiple TaskCards with loading and empty states
- `StatusBadge`: Visual indicator for task completion status
- Base UI components from shadcn/ui (Button, Card, Input, etc.)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Specify license here]