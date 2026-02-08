# Token Refresh Implementation

## Overview

This document describes the token refresh mechanism implemented in the authentication system. The implementation provides secure, automatic token renewal using refresh tokens with rotation to prevent token theft and replay attacks.

## Architecture

### Backend Components

#### 1. Database Model (`backend/src/models/refresh_token.py`)

The `RefreshToken` model stores refresh tokens in the database with the following fields:

```python
- id: UUID (primary key)
- token: str (unique, indexed) - The actual refresh token
- user_id: UUID (foreign key to users table, indexed)
- expires_at: datetime (indexed) - Token expiration timestamp
- created_at: datetime - When token was created
- revoked: bool (indexed) - Whether token has been revoked
- revoked_at: datetime - When token was revoked (nullable)
- device_info: str - Optional device/client information (max 500 chars)
```

**Key Features:**
- Tokens are indexed for fast lookups
- Built-in `is_valid()` method checks expiration and revocation
- Built-in `revoke()` method for token revocation
- Cascade delete when user is deleted

#### 2. Security Module (`backend/src/core/security.py`)

Added refresh token functions:

**`generate_refresh_token()`**
- Generates cryptographically secure 64-character token using `secrets.token_urlsafe(48)`

**`create_refresh_token(user_id, db, device_info=None)`**
- Creates new refresh token in database
- Default expiration: 7 days (configurable via `REFRESH_TOKEN_EXPIRE_DAYS`)
- Returns token string

**`verify_refresh_token(token, db)`**
- Validates token exists, not revoked, and not expired
- Returns associated User object or None

**`rotate_refresh_token(old_token, db, device_info=None)`**
- Validates old token
- Revokes old token
- Creates new token
- Returns tuple: (new_token, user) or None

**`revoke_refresh_token(token, db)`**
- Revokes a specific token
- Returns True if successful

**`revoke_all_user_refresh_tokens(user_id, db)`**
- Revokes all active tokens for a user
- Returns count of revoked tokens

#### 3. API Endpoints (`backend/src/api/routes/auth.py`)

**POST /api/auth/login**
- Modified to return both `access_token` and `refresh_token`
- Stores refresh token in database
- Response format:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "abc123...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

**POST /api/auth/refresh** (NEW)
- Accepts refresh token
- Validates token
- Implements token rotation (revokes old, creates new)
- Returns new access token + new refresh token
- Request format:
```json
{
  "refresh_token": "abc123...",
  "device_info": "optional device info"
}
```

**POST /api/auth/logout**
- Modified to accept refresh token
- Supports two modes:
  1. Revoke specific token: `{"refresh_token": "abc123..."}`
  2. Revoke all user tokens: `{"revoke_all": true}`
- Requires authentication (access token in header)

#### 4. Configuration (`backend/src/core/config.py`)

Added new setting:
```python
REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # Default 7 days
```

Environment variable: `REFRESH_TOKEN_EXPIRE_DAYS`

### Frontend Components

#### 1. Auth Provider (`frontend/src/components/auth/provider.tsx`)

Enhanced with refresh token support:

**Storage:**
- Stores `access_token`, `refresh_token`, and `user` in localStorage
- New helper: `clearAuthStorage()` clears all auth data

**Session Validation:**
- On mount, validates access token
- If 401, attempts refresh using refresh token
- Clears storage if refresh fails

**`refreshAccessToken(refreshToken)` (internal)**
- Calls `/api/auth/refresh`
- Updates stored tokens
- Returns boolean success status

**`refreshToken()` (public API)**
- Public method for manual token refresh
- Uses stored refresh token
- Updates session state

**Login:**
- Stores both access and refresh tokens
- Returns tokens to caller

**Logout:**
- Sends refresh token to backend for revocation
- Supports `revoke_all` flag
- Clears local storage
- Updates session state

**Event Listener:**
- Listens for `auth:logout` custom events
- Automatically clears auth data when event fired
- Used by API client when refresh fails

#### 2. API Client (`frontend/src/lib/api-client.ts`) (NEW)

Provides authenticated fetch wrapper with automatic token refresh:

**`authenticatedFetch(url, options)`**
- Automatically adds Authorization header
- Intercepts 401 responses
- Attempts token refresh
- Retries request with new token
- Emits `auth:logout` event if refresh fails

**Convenience Methods:**
- `authenticatedGet(url, options)`
- `authenticatedPost(url, body, options)`
- `authenticatedPut(url, body, options)`
- `authenticatedDelete(url, options)`

**Options:**
- `skipAuth`: Don't add Authorization header
- `skipRefresh`: Don't attempt refresh on 401

#### 3. Chatbot API (`frontend/src/lib/chatbot-api.ts`)

Updated to use `authenticatedPost()` from API client:
- Automatic token refresh on expiration
- No manual token handling needed

## Token Flow

### Initial Authentication

1. User submits credentials to `/api/auth/login`
2. Backend validates credentials
3. Backend generates:
   - Access token (JWT, 30 min expiration)
   - Refresh token (random string, 7 day expiration)
4. Refresh token stored in database
5. Both tokens returned to frontend
6. Frontend stores both tokens in localStorage

### Token Refresh Flow

1. Frontend makes API request with expired access token
2. Backend returns 401 Unauthorized
3. `authenticatedFetch()` intercepts 401
4. Automatically calls `/api/auth/refresh` with refresh token
5. Backend validates refresh token:
   - Checks token exists in database
   - Checks not revoked
   - Checks not expired
6. Backend rotates token:
   - Marks old refresh token as revoked
   - Generates new refresh token
   - Stores new token in database
7. Backend returns new access token + new refresh token
8. Frontend stores new tokens
9. Frontend retries original request with new access token
10. Request succeeds

### Logout Flow

1. User initiates logout
2. Frontend calls `/api/auth/logout` with refresh token
3. Backend marks refresh token as revoked
4. Frontend clears localStorage
5. Frontend updates session state

### Token Rotation

Refresh tokens are rotated on every use:
- Old token is immediately revoked
- New token is generated and stored
- This prevents replay attacks
- Stolen tokens become invalid after first use

## Security Features

### 1. Token Rotation
- Refresh tokens are single-use
- Each refresh generates a new token
- Old tokens are immediately revoked
- Limits window for stolen token exploitation

### 2. Database Storage
- Refresh tokens stored server-side
- Can be revoked at any time
- Track token usage and metadata
- Support for device tracking

### 3. Expiration
- Access tokens: 30 minutes (short-lived)
- Refresh tokens: 7 days (configurable)
- Both enforced server-side

### 4. Revocation
- Individual token revocation
- Bulk revocation (logout from all devices)
- Cascade delete on user deletion

### 5. Secure Generation
- Cryptographically secure random tokens
- 48 bytes of entropy (64 characters base64)
- Uses Python's `secrets` module

### 6. Automatic Refresh
- Frontend handles refresh transparently
- No user intervention needed
- Failed refresh triggers re-authentication

## Configuration

### Backend Environment Variables

```bash
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Refresh Token Configuration
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=postgresql://user:pass@host/db
```

### Frontend Environment Variables

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Database Migration

The refresh tokens table is automatically created when running:
```bash
python -m backend.src.database.init_db
```

Or when starting the FastAPI app (if auto-migration is enabled).

**Table Schema:**
```sql
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY,
    token VARCHAR UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    revoked_at TIMESTAMP,
    device_info VARCHAR(500)
);

CREATE INDEX idx_refresh_tokens_token ON refresh_tokens(token);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
CREATE INDEX idx_refresh_tokens_revoked ON refresh_tokens(revoked);
```

## Usage Examples

### Frontend: Using Authenticated Fetch

```typescript
import { authenticatedFetch, authenticatedPost } from '@/lib/api-client';

// Automatic token refresh on 401
const response = await authenticatedFetch('/api/tasks', {
  method: 'GET'
});

// Or use convenience methods
const response = await authenticatedPost('/api/tasks', {
  title: 'New Task',
  description: 'Task description'
});
```

### Frontend: Manual Token Refresh

```typescript
import { useAuth } from '@/components/auth/provider';

function MyComponent() {
  const { refreshToken } = useAuth();

  const handleRefresh = async () => {
    const success = await refreshToken();
    if (success) {
      console.log('Token refreshed successfully');
    } else {
      console.log('Token refresh failed, please log in again');
    }
  };
}
```

### Backend: Revoking All User Tokens

```python
from core.security import revoke_all_user_refresh_tokens

# Revoke all tokens for a user (e.g., on password change)
count = revoke_all_user_refresh_tokens(user_id, db)
print(f"Revoked {count} tokens")
```

## Testing

### Test Token Refresh

1. Log in to get tokens
2. Wait 30+ minutes for access token to expire
3. Make an authenticated API call
4. Verify automatic refresh occurs
5. Verify request succeeds with new token

### Test Token Rotation

1. Log in to get refresh token
2. Call `/api/auth/refresh` with refresh token
3. Verify new tokens returned
4. Try to use old refresh token again
5. Verify it fails (token revoked)

### Test Logout

1. Log in to get tokens
2. Call `/api/auth/logout` with refresh token
3. Try to use refresh token
4. Verify it fails (token revoked)

## Monitoring

Recommended monitoring:
- Track refresh token usage
- Alert on high refresh rates (potential attack)
- Monitor revoked token usage attempts
- Track token expiration dates
- Alert on expired tokens in database (cleanup needed)

## Maintenance

### Token Cleanup

Periodically clean up expired/revoked tokens:

```python
from datetime import datetime
from models.refresh_token import RefreshToken

# Delete expired tokens older than 30 days
cutoff = datetime.utcnow() - timedelta(days=30)
db.query(RefreshToken).filter(
    RefreshToken.expires_at < cutoff
).delete()
db.commit()
```

Consider setting up a cron job or background task for automatic cleanup.

## Future Improvements

1. **Token Fingerprinting**: Add client fingerprinting to detect token theft
2. **Rate Limiting**: Limit refresh attempts per user
3. **Notification**: Notify users of new device logins
4. **Suspicious Activity**: Detect and block suspicious token usage patterns
5. **httpOnly Cookies**: Move from localStorage to httpOnly cookies for XSS protection
6. **Sliding Expiration**: Extend refresh token expiration on use
7. **Token Families**: Track token lineage to detect parallel usage
8. **Geolocation**: Track and validate token usage location

## Troubleshooting

### Token refresh fails with 401
- Check refresh token is valid in database
- Verify token not expired
- Check token not revoked
- Verify user still exists

### Frontend doesn't refresh automatically
- Check `authenticatedFetch()` is being used
- Verify refresh token is stored in localStorage
- Check console for refresh errors
- Verify backend `/auth/refresh` endpoint is accessible

### Tokens not being stored
- Check localStorage is available
- Verify CORS settings allow credentials
- Check response contains both tokens
- Verify no errors in browser console

## References

- JWT Best Practices: https://tools.ietf.org/html/rfc8725
- OAuth 2.0 Refresh Tokens: https://tools.ietf.org/html/rfc6749#section-1.5
- Token Rotation: https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation
