# Data Model: Secure Auth & JWT Integration

## User Entity
Based on the authentication requirements and Better Auth integration:

```typescript
// Frontend User Type (from Better Auth)
interface FrontendUser {
  id: string;           // Unique identifier from Better Auth
  email: string;        // User's email address
  name?: string;        // User's display name (optional)
  createdAt: string;    // Account creation timestamp
  updatedAt: string;    // Last update timestamp
  emailVerified: boolean; // Whether the email has been verified
}

// Backend User Model (for database operations)
interface BackendUser {
  id: string;           // Unique identifier (matching Better Auth format)
  email: string;        // User's email address
  email_verified: boolean; // Whether the email has been verified
  created_at: string;   // Account creation timestamp
  updated_at: string;   // Last update timestamp
}
```

### Validation Rules
- Email must be a valid email format
- Email must be unique across all users
- User ID format must match Better Auth's ID format (UUID or custom)

## JWT Token Structure
Standard JWT with custom claims for user authentication:

```typescript
interface JwtPayload {
  sub: string;          // Subject (user ID)
  aud: string;          // Audience (application identifier)
  exp: number;          // Expiration time (as Unix timestamp)
  iat: number;          // Issued at time (as Unix timestamp)
  nbf: number;          // Not before time (as Unix timestamp)
  name?: string;        // User's display name (optional)
  email: string;        // User's email address
  // Additional custom claims as needed
}
```

### Token Validation Rules
- Token must be properly signed with the shared BETTER_AUTH_SECRET
- Token must not be expired (exp claim must be in the future)
- Token must be valid for the current time (iat and nbf claims)
- Signature must be verified using HS256 algorithm

## Auth Session Interface
Managing authentication state on the frontend:

```typescript
interface AuthSession {
  user: FrontendUser;   // Authenticated user information
  accessToken: string;  // Current JWT access token
  refreshToken?: string; // Refresh token (if implemented)
  expiresAt: number;    // Token expiration time (Unix timestamp)
  isAuthenticated: boolean; // Whether the user is currently authenticated
}
```

## API Request/Response Types
Standardized types for authenticated API communication:

```typescript
interface AuthenticatedRequest {
  headers: {
    Authorization: `Bearer ${string}`; // JWT token in Authorization header
    [key: string]: string;             // Other headers as needed
  };
  body?: any;                          // Request body (optional)
}

interface AuthenticatedApiResponse<T> {
  data?: T;
  error?: string;
  success: boolean;
  user_id?: string;                   // Associated user ID (when applicable)
}
```

## Authentication Flow Types
Types for managing the authentication flow:

```typescript
interface LoginCredentials {
  email: string;
  password: string;
}

interface SignupDetails {
  email: string;
  password: string;
  name?: string;
}

interface LoginResponse {
  user: FrontendUser;
  accessToken: string;
  refreshToken?: string;
  success: boolean;
  error?: string;
}
```

## Task Entity with User Association
Updated task model with proper user association for data isolation:

```typescript
interface TaskWithUser {
  id: string;           // Unique task identifier
  title: string;        // Task title (1-200 characters)
  description?: string; // Optional task description
  completed: boolean;   // Whether the task is completed
  user_id: string;      // Associated user ID for data isolation
  version: number;      // Version number for optimistic locking
  created_at: string;   // Task creation timestamp
  updated_at: string;   // Last update timestamp
}
```

### Data Isolation Rules
- All task queries must be filtered by the authenticated user's ID
- Users cannot access tasks belonging to other users
- Database queries must enforce user_id filtering at the application level