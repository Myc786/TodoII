# Integration Testing Guide

## Quick Test Commands

### Test Backend (HF Spaces)

```bash
# Health check
curl https://myc786-part2.hf.space/health

# Expected response:
# {"status":"healthy","environment":"production"}
```

### Test Frontend (Vercel)

```bash
# Check if site is up
curl -I https://frontend-mocha-beta-73.vercel.app

# Expected: HTTP/2 200
```

## Complete Integration Test

Run these tests in order to verify full integration:

### 1. Backend Health Check

```bash
curl -X GET https://myc786-part2.hf.space/health
```

**Expected**:
```json
{
  "status": "healthy",
  "environment": "production"
}
```

### 2. Test User Registration

```bash
curl -X POST https://myc786-part2.hf.space/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "name": "Test User",
    "password": "SecurePass123!"
  }'
```

**Expected**:
```json
{
  "id": "uuid-here",
  "email": "testuser@example.com",
  "name": "Test User",
  "created_at": "2024-...",
  "updated_at": "2024-..."
}
```

### 3. Test User Login

```bash
curl -X POST https://myc786-part2.hf.space/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "SecurePass123!"
  }'
```

**Expected**:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

**Save the token** for next tests:
```bash
export TOKEN="eyJ..."
```

### 4. Test Create Task

```bash
curl -X POST https://myc786-part2.hf.space/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Test Task",
    "description": "Testing integration",
    "priority": "high"
  }'
```

**Expected**:
```json
{
  "id": "uuid-here",
  "title": "Test Task",
  "description": "Testing integration",
  "completed": false,
  "priority": "high",
  "user_id": "user-uuid",
  "version": 1,
  "created_at": "2024-...",
  "updated_at": "2024-..."
}
```

**Save task ID**:
```bash
export TASK_ID="uuid-here"
```

### 5. Test Get All Tasks

```bash
curl -X GET https://myc786-part2.hf.space/api/tasks/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected**: Array of tasks including the one created above.

### 6. Test Update Task

```bash
curl -X PUT https://myc786-part2.hf.space/api/tasks/$TASK_ID/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Updated Task",
    "completed": true,
    "version": 1
  }'
```

**Expected**: Updated task with `completed: true` and `version: 2`.

### 7. Test Delete Task

```bash
curl -X DELETE https://myc786-part2.hf.space/api/tasks/$TASK_ID/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected**:
```json
{"message": "Task deleted successfully"}
```

### 8. Test CORS (from browser)

Open browser console on https://frontend-mocha-beta-73.vercel.app and run:

```javascript
fetch('https://myc786-part2.hf.space/health')
  .then(r => r.json())
  .then(d => console.log('CORS works!', d))
  .catch(e => console.error('CORS error:', e))
```

**Expected**: Should log "CORS works!" with health data.

## Frontend Manual Testing

### 1. Registration Flow

1. Visit https://frontend-mocha-beta-73.vercel.app
2. Click "Sign Up"
3. Enter:
   - Name: Your Name
   - Email: your-email@example.com
   - Password: SecurePass123!
4. Click "Sign Up"
5. **Expected**: Redirect to dashboard

### 2. Login Flow

1. Visit https://frontend-mocha-beta-73.vercel.app
2. Click "Login"
3. Enter credentials from registration
4. Click "Login"
5. **Expected**: Redirect to dashboard, see empty task list

### 3. Create Task

1. In dashboard, click "Add Task" or find task form
2. Enter:
   - Title: "Buy groceries"
   - Description: "Milk, bread, eggs"
   - Priority: High
3. Click "Create" or "Save"
4. **Expected**: Task appears in list immediately

### 4. Complete Task

1. Find the task in list
2. Click checkbox or "Complete" button
3. **Expected**: Task marked as complete, visual feedback

### 5. Edit Task

1. Click "Edit" on a task
2. Change title to "Buy groceries and fruits"
3. Save changes
4. **Expected**: Task updates immediately

### 6. Delete Task

1. Click "Delete" on a task
2. Confirm deletion if prompted
3. **Expected**: Task removed from list

### 7. Logout

1. Click "Logout" button (usually in header)
2. **Expected**: Redirect to home/login page

### 8. Token Persistence

1. Login to dashboard
2. Close browser tab
3. Open new tab, visit app
4. **Expected**: Still logged in (if using remember me)

## Automated Test Script

Save this as `test_integration.sh`:

```bash
#!/bin/bash

BASE_URL="https://myc786-part2.hf.space"
FRONTEND_URL="https://frontend-mocha-beta-73.vercel.app"

echo "=== Testing Backend Integration ==="

# 1. Health check
echo "\n1. Testing health endpoint..."
curl -s "$BASE_URL/health" | jq .

# 2. Register user
echo "\n2. Testing user registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"test$(date +%s)@example.com\",
    \"name\": \"Test User\",
    \"password\": \"SecurePass123!\"
  }")
echo $REGISTER_RESPONSE | jq .

# 3. Login
echo "\n3. Testing login..."
EMAIL=$(echo $REGISTER_RESPONSE | jq -r .email)
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"SecurePass123!\"
  }")
echo $LOGIN_RESPONSE | jq .

TOKEN=$(echo $LOGIN_RESPONSE | jq -r .access_token)

# 4. Create task
echo "\n4. Testing create task..."
TASK_RESPONSE=$(curl -s -X POST "$BASE_URL/api/tasks/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"title\": \"Integration Test Task\",
    \"description\": \"Created by automated test\",
    \"priority\": \"high\"
  }")
echo $TASK_RESPONSE | jq .

TASK_ID=$(echo $TASK_RESPONSE | jq -r .id)

# 5. Get tasks
echo "\n5. Testing get tasks..."
curl -s -X GET "$BASE_URL/api/tasks/" \
  -H "Authorization: Bearer $TOKEN" | jq .

# 6. Update task
echo "\n6. Testing update task..."
curl -s -X PUT "$BASE_URL/api/tasks/$TASK_ID/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"title\": \"Updated Integration Test Task\",
    \"completed\": true,
    \"version\": 1
  }" | jq .

# 7. Delete task
echo "\n7. Testing delete task..."
curl -s -X DELETE "$BASE_URL/api/tasks/$TASK_ID/" \
  -H "Authorization: Bearer $TOKEN" | jq .

echo "\n=== Integration Tests Complete ==="
```

Run with:
```bash
chmod +x test_integration.sh
./test_integration.sh
```

## Common Issues and Solutions

### Issue: CORS Error

**Symptom**: Browser console shows "CORS policy" error

**Check**:
```bash
# Test CORS headers
curl -I -X OPTIONS https://myc786-part2.hf.space/api/tasks/ \
  -H "Origin: https://frontend-mocha-beta-73.vercel.app" \
  -H "Access-Control-Request-Method: GET"
```

**Fix**: Ensure backend `FRONTEND_URL` includes your Vercel domain.

### Issue: 401 Unauthorized

**Symptom**: All API calls return 401

**Check**:
```bash
# Verify token is valid
echo $TOKEN

# Try to decode JWT (requires jq and base64)
echo $TOKEN | cut -d. -f2 | base64 -d | jq .
```

**Fix**: Token might be expired. Login again to get new token.

### Issue: 500 Internal Server Error

**Symptom**: Backend returns 500 error

**Check**: HF Space logs at https://huggingface.co/spaces/myc786/Part2

**Common causes**:
- Database connection error
- Missing environment variables
- Code errors

### Issue: Network Error

**Symptom**: "Failed to fetch" in frontend

**Check**:
```bash
# Verify backend is running
curl https://myc786-part2.hf.space/health

# Check DNS
nslookup myc786-part2.hf.space

# Check from frontend domain
curl -H "Origin: https://frontend-mocha-beta-73.vercel.app" \
  https://myc786-part2.hf.space/health
```

## Performance Testing

### Response Time Test

```bash
# Test backend response time
time curl https://myc786-part2.hf.space/health

# Should be under 500ms
```

### Load Test (simple)

```bash
# Test 10 concurrent requests
for i in {1..10}; do
  curl -s https://myc786-part2.hf.space/health &
done
wait
```

## Security Testing

### Test Authentication Required

```bash
# Should fail without token
curl -X GET https://myc786-part2.hf.space/api/tasks/

# Expected: 401 Unauthorized
```

### Test Invalid Token

```bash
# Should fail with invalid token
curl -X GET https://myc786-part2.hf.space/api/tasks/ \
  -H "Authorization: Bearer invalid-token"

# Expected: 401 Unauthorized
```

### Test SQL Injection Protection

```bash
# Should not cause SQL injection
curl -X POST https://myc786-part2.hf.space/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com OR 1=1--",
    "password": "anything"
  }'

# Expected: 401 Unauthorized (not SQL error)
```

## Success Criteria

All tests should pass with:
- ✅ Backend health returns 200 OK
- ✅ User registration creates account
- ✅ Login returns valid JWT token
- ✅ Tasks can be created, read, updated, deleted
- ✅ CORS allows frontend requests
- ✅ Authentication required for protected routes
- ✅ Frontend can interact with backend
- ✅ No console errors in browser
- ✅ Response times under 1 second
- ✅ SSL/HTTPS working on both domains
