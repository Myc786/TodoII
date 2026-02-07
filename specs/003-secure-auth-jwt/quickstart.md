# Quickstart Guide: Secure Auth & JWT Integration

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Access to both frontend and backend environments
- BETTER_AUTH_SECRET environment variable set identically in both environments

## Setup Instructions

### 1. Environment Configuration
Ensure the same BETTER_AUTH_SECRET is configured in both environments:

**Frontend (.env.local):**
```env
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-shared-secret-key
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
```

**Backend (.env):**
```env
BETTER_AUTH_SECRET=your-shared-secret-key
```

### 2. Frontend Authentication Setup
1. Install Better Auth dependencies:
```bash
npm install better-auth @better-auth/react
```

2. Configure Better Auth client in `frontend/src/lib/auth.ts`:
```typescript
import { createAuthClient } from "better-auth/client";
import { reactHooks } from "@better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000/api/auth",
  plugins: [reactHooks()],
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

### 3. Backend Authentication Setup
1. Install JWT verification dependencies:
```bash
pip install python-jose[cryptography]
```

2. Create JWT verification utilities in `backend/src/auth_utils.py`:
```python
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from typing import Optional
import os

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token and return the payload if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Get the current user from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    return {"id": user_id}
```

### 4. Update API Client for JWT Headers
Modify the existing API client in `frontend/src/lib/api.ts` to include JWT tokens:

```typescript
const getAuthHeaders = (): HeadersInit => {
  const token = localStorage.getItem('better-auth-token'); // Or however token is stored
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
};
```

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

### Protected Task Endpoints
All task endpoints now require valid JWT authentication:
- `GET /api/tasks` - Get current user's tasks
- `POST /api/tasks` - Create new task for current user
- `GET /api/tasks/{id}` - Get specific task (if owned by user)
- `PUT /api/tasks/{id}` - Update task (if owned by user)
- `DELETE /api/tasks/{id}` - Delete task (if owned by user)
- `PATCH /api/tasks/{id}/toggle` - Toggle task completion (if owned by user)

## Testing the Integration

### 1. Authentication Flow Test
1. Register a new user account
2. Verify successful login and JWT token reception
3. Access protected endpoints with the token

### 2. Data Isolation Test
1. Create two user accounts (User A and User B)
2. Log in as User A and create some tasks
3. Log in as User B and verify they cannot see User A's tasks
4. Attempt to access User A's specific task using User B's token (should fail)

### 3. Unauthorized Access Test
1. Try accessing protected endpoints without a token (should return 401)
2. Try accessing protected endpoints with an invalid token (should return 401)
3. Try accessing protected endpoints with an expired token (should return 401)

## Key Features
- Secure JWT-based authentication with Better Auth
- Automatic JWT token attachment to API requests
- FastAPI middleware for token verification
- User data isolation with user_id filtering
- Proper 401 Unauthorized responses for invalid requests
- Stateless authentication (no server-side session storage)