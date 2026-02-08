# Task Endpoint 401 Issue - Investigation Report

## Problem Statement

Task endpoints (`/api/tasks`, `/api/tasks/{id}`) were returning 401 "Invalid or missing Authorization header" errors even when valid Bearer tokens were provided. The same tokens worked correctly for authentication endpoints like `/api/auth/me`.

## Root Cause

The issue was caused by **HTTP 307 Temporary Redirects** from Hugging Face Spaces infrastructure when endpoints were accessed without proper trailing slashes. During HTTP redirects, most clients **drop the Authorization header** for security reasons, causing authentication to fail on the redirected request.

## Investigation Steps

### 1. Initial Testing
- Confirmed tokens worked for `/api/auth/me` (200 OK)
- Confirmed same tokens failed for `/api/tasks` (401 Unauthorized)
- Error message: "Invalid or missing Authorization header"

### 2. Debug Logging
Added comprehensive debug logging to `backend/src/api/deps.py`:
- Logged incoming Authorization headers
- Logged token extraction and validation steps
- Logged database user lookups

### 3. HTTP Header Analysis
Used `curl -v` to inspect HTTP responses:
```bash
curl -X GET "https://myc786-part2.hf.space/api/tasks" -H "Authorization: Bearer token" -v
```

**Key Finding**: Received `307 Temporary Redirect` response:
```
< HTTP/1.1 307 Temporary Redirect
< location: http://myc786-part2.hf.space/api/tasks/
```

The redirect from `/api/tasks` → `/api/tasks/` was **dropping the Authorization header**.

### 4. Testing with Trailing Slashes
Tested endpoints with and without trailing slashes:

| Endpoint | Without Slash | With Slash | Result |
|----------|--------------|------------|---------|
| GET /api/tasks | 307 Redirect (loses auth) | 200 OK | ✓ Use slash |
| POST /api/tasks | 307 Redirect (loses auth) | 200 OK | ✓ Use slash |
| PUT /api/tasks/{id} | 200 OK | 401 Unauthorized | ✓ No slash |
| DELETE /api/tasks/{id} | 200 OK | 401 Unauthorized | ✓ No slash |

## Solution

### Trailing Slash Rules for Hugging Face Spaces

**Collection Endpoints** (GET list, POST create):
- ✅ **Use trailing slash**: `/api/tasks/`
- ❌ Without slash: Gets redirected, loses auth header

**Item Endpoints** (GET one, PUT update, DELETE):
- ✅ **No trailing slash**: `/api/tasks/{id}`
- ❌ With slash: Returns 401

### Implementation

Update API clients to follow these rules:

```python
# Correct usage
GET    /api/tasks/                    # List all tasks
POST   /api/tasks/                    # Create task
GET    /api/tasks/{id}                # Get specific task
PUT    /api/tasks/{id}                # Update task
DELETE /api/tasks/{id}                # Delete task
```

## Additional Fixes Applied

### 1. Pydantic 2.10 Compatibility
Fixed `default_factory` issues in models that were causing validation errors:

**Task Model** (`backend/src/models/task.py`):
```python
# Before (caused errors)
id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
created_at: datetime = Field(default_factory=datetime.utcnow)

# After (works)
id: Optional[uuid.UUID] = Field(default=None, primary_key=True)
created_at: Optional[datetime] = Field(default=None)
```

**Task Service** (`backend/src/services/task_service.py`):
```python
# Manually set values in create_task()
task_data['id'] = uuid.uuid4()
task_data['created_at'] = datetime.utcnow()
task_data['updated_at'] = datetime.utcnow()
```

## Testing Results

### Final Production Test (100% Pass Rate)

```
1. User Registration            ✓ 200 OK
2. User Login                   ✓ 200 OK (with refresh token)
3. Token Validation (/auth/me)  ✓ 200 OK
4. Token Refresh                ✓ 200 OK (rotation working)
5. Create Task (POST /tasks/)   ✓ 200 OK
6. Get Tasks (GET /tasks/)      ✓ 200 OK
7. Update Task (PUT /tasks/id)  ✓ 200 OK
8. Delete Task (DELETE /tasks/id) ✓ 200 OK
9. Old Token Rejection          ✓ 401 (correct)
10. Logout                      ✓ 200 OK
11. Post-Logout Token Rejection ✓ 401 (correct)
```

All features now working correctly in production!

## Why This Happens

### HTTP Redirect Behavior

1. **Security Measure**: Browsers and HTTP clients drop Authorization headers during redirects to prevent credentials from being sent to potentially malicious redirect targets.

2. **FastAPI Routing**: FastAPI's default behavior is to redirect URLs without trailing slashes to versions with trailing slashes for collection endpoints.

3. **Hugging Face Proxy**: The HF Spaces infrastructure adds another layer that enforces redirect policies.

### Why Collection vs Item Endpoints Differ

- **Collection endpoints** (`/tasks`) are treated as directories → redirect to `/tasks/`
- **Item endpoints** (`/tasks/123`) are treated as files → no redirect needed

## Recommendations

### For Frontend Developers

1. **Always use correct trailing slashes** when calling the API
2. **Don't rely on redirects** - they will lose authentication
3. **Use helper functions** to ensure correct URL formatting:

```typescript
// Helper to ensure correct task endpoint format
const getTaskUrl = (taskId?: string) => {
  const base = `${API_URL}/tasks`;
  return taskId ? `${base}/${taskId}` : `${base}/`;
};

// Usage
await fetch(getTaskUrl(), { headers: { Authorization: `Bearer ${token}` } });
await fetch(getTaskUrl(id), { method: 'PUT', ... });
```

### For Backend Developers

1. **Document trailing slash requirements** clearly in API documentation
2. **Consider adding redirects that preserve headers** (though this is complex)
3. **Add API versioning** to allow flexibility in endpoint structure changes

## Files Modified

### Debug Logging Added
- `backend/src/api/deps.py` - Added debug logging to `get_current_user()`
- `backend/src/api/routes/tasks.py` - Added debug logging to task endpoints

### Model Fixes
- `backend/src/models/task.py` - Fixed Pydantic 2.10 compatibility
- `backend/src/models/user.py` - Fixed Pydantic 2.10 compatibility (previously)
- `backend/src/models/refresh_token.py` - Fixed Pydantic 2.10 compatibility (previously)

### Service Updates
- `backend/src/services/task_service.py` - Manually set UUID and datetime fields

## Test Scripts Created

1. **test_debug_task.py** - Initial debugging script
2. **test_production_fixed.py** - Comprehensive production test with correct trailing slashes
3. **check_refresh_tokens.py** - Database verification script

## Lessons Learned

1. **HTTP redirects can break authentication** - Always be aware of trailing slash behavior
2. **Test with actual deployment environment** - Local testing doesn't always reveal proxy/redirect issues
3. **Debug logging is essential** - Helped identify that auth headers were missing, not invalid
4. **curl -v is your friend** - Shows actual HTTP response codes and redirects
5. **Model validation changes** - Pydantic 2.x has stricter validation requiring different patterns

## Status

✅ **RESOLVED** - All task endpoints now working correctly in production with proper trailing slash usage.

---

**Date**: 2026-02-08
**Environment**: Hugging Face Spaces + Vercel
**Backend**: https://myc786-part2.hf.space/api
**Frontend**: https://frontend-mocha-beta-73.vercel.app
**Status**: Production Ready - 100% test pass rate
