# Debug Signup Error

## Current Status
- ✅ Backend API is working (tested with curl)
- ✅ Registration endpoint returns 200 OK
- ✅ User creation successful in database
- ⚠️ Frontend signup showing error

## Quick Test

### Test Backend Directly
```bash
curl -X POST "https://myc786-part2.hf.space/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test123@example.com","name":"Test User","password":"Password123!"}'
```

**Expected**: Should return user data with 200 OK ✅

## Frontend Debugging Steps

### Step 1: Check Browser Console
1. Visit: https://frontend-mocha-beta-73.vercel.app/signup
2. Open DevTools (F12)
3. Go to "Console" tab
4. Try to sign up
5. Look for error messages

### Step 2: Check Network Tab
1. Stay in DevTools
2. Go to "Network" tab
3. Try to sign up
4. Find the "register" request
5. Check:
   - Status Code
   - Response body
   - Request payload

### Step 3: Common Issues to Check

#### Issue 1: Toast Not Showing
**Symptom**: No error message appears
**Check**: Look for console errors about `useToast`

#### Issue 2: Network Error
**Symptom**: "Network error occurred"
**Possible Causes**:
- CORS issue
- API URL incorrect
- Backend not responding

**Check Network Tab**:
```
Request URL: https://myc786-part2.hf.space/api/auth/register
Status: Should be 200 or show error
```

#### Issue 3: API Response Error
**Symptom**: Backend returns error
**Possible Causes**:
- Validation failed
- Duplicate email
- Database error

#### Issue 4: Environment Variables Not Set
**Check**:
```javascript
// In browser console, run:
console.log('API URL:', process.env.NEXT_PUBLIC_API_URL);
// Should show: https://myc786-part2.hf.space/api
```

## Expected Behavior

### Successful Signup Flow:
1. User fills form (name, email, password, confirm password)
2. Clicks "Sign Up" button
3. Frontend sends POST to `/api/auth/register`
4. Backend creates user
5. Backend returns user data
6. Frontend automatically logs user in
7. Frontend redirects to dashboard
8. Toast shows: "Account created successfully!"

### Error Flow:
1. User fills form
2. Clicks "Sign Up"
3. Frontend/Backend detects error
4. Toast shows error message
5. User stays on signup page

## What to Share

Please check the browser console and share:

### 1. Console Errors
```
Look for errors like:
- "Failed to fetch"
- "Network error"
- "CORS policy"
- Any red error messages
```

### 2. Network Request Details
From Network tab, share:
- **Request URL**:
- **Status Code**:
- **Response Body**:
- **Request Payload**:

### 3. Exact Error Message
What does the error toast say?

## Quick Fixes to Try

### Fix 1: Clear Browser Cache
1. Press Ctrl+Shift+Delete
2. Clear cached images and files
3. Try signup again

### Fix 2: Try Incognito/Private Mode
1. Open incognito window
2. Visit signup page
3. Try creating account

### Fix 3: Check Environment Variables in Vercel
Go to: https://vercel.com/myc786s-projects/frontend/settings/environment-variables

Ensure these are set:
```
NEXT_PUBLIC_API_URL=https://myc786-part2.hf.space/api
NEXT_PUBLIC_BETTER_AUTH_URL=https://myc786-part2.hf.space/api/auth
NEXT_PUBLIC_BETTER_AUTH_SECRET=ghLw-JPwjxA6ed4YsWa5QxB3atOZsA0CZnKK6rgQ_xs
```

If any are missing or different, update and redeploy.

## Manual Test Script

Run this in the browser console on the signup page:

```javascript
// Test registration directly
async function testSignup() {
  const API_URL = 'https://myc786-part2.hf.space/api';

  try {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'consoletest@test.com',
        name: 'Console Test',
        password: 'Password123!'
      })
    });

    const data = await response.json();
    console.log('Status:', response.status);
    console.log('Response:', data);

    if (response.ok) {
      console.log('✅ Registration successful!');
    } else {
      console.log('❌ Registration failed:', data);
    }
  } catch (error) {
    console.error('❌ Network error:', error);
  }
}

testSignup();
```

## Possible Root Causes

### 1. Missing Toaster Component
**Check**: Error should still log to console even if toast doesn't show

### 2. CORS Not Working
**Test**: Run the manual test script above in console
**If it fails**: CORS issue (but our tests show it's working)

### 3. Environment Variable Not Set
**Symptom**: Console shows wrong API URL
**Fix**: Update Vercel environment variables and redeploy

### 4. Validation Error
**Symptom**: Password requirements not met
**Requirements**:
- At least 8 characters
- Password and confirm password must match

### 5. Duplicate Email
**Symptom**: Error message: "User with this email already exists"
**Fix**: Try different email

## Verification Commands

```bash
# 1. Check backend health
curl https://myc786-part2.hf.space/health

# 2. Check CORS
curl -I -X OPTIONS "https://myc786-part2.hf.space/api/auth/register" \
  -H "Origin: https://frontend-mocha-beta-73.vercel.app" \
  -H "Access-Control-Request-Method: POST"

# 3. Test registration
curl -X POST "https://myc786-part2.hf.space/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"curltest@test.com","name":"Curl Test","password":"Password123!"}'
```

## Next Steps

1. **Open frontend signup page**: https://frontend-mocha-beta-73.vercel.app/signup
2. **Open DevTools** (F12)
3. **Try to sign up**
4. **Share**:
   - Console errors
   - Network request details
   - Exact error message shown

This will help identify the exact issue!
