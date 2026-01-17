# Test Scenarios: Secure Auth & JWT Integration

## User Story 1: User Registration & Authentication

### T020: Test registration flow with valid email and password
**Test Case**: Register new user with valid credentials
- Given: User navigates to signup page
- When: User enters valid email, name, and password (8+ chars)
- And: User confirms password correctly
- And: User submits the form
- Then: Account is created successfully
- And: User is logged in automatically
- And: JWT token is stored in localStorage
- And: User is redirected to dashboard

### T021: Test login flow with correct credentials
**Test Case**: Login with correct credentials
- Given: User has a valid account
- When: User navigates to login page
- And: User enters correct email and password
- And: User submits the form
- Then: Authentication succeeds
- And: JWT token is received and stored
- And: User is redirected to dashboard
- And: User profile is accessible

### T022: Test authentication failure with incorrect credentials
**Test Case**: Login with incorrect credentials
- Given: User has a valid account
- When: User navigates to login page
- And: User enters incorrect password
- And: User submits the form
- Then: Authentication fails
- And: Error message is displayed
- And: User remains on login page
- And: No JWT token is stored

## User Story 2: JWT Token Management

### T027: Test JWT attachment to API requests
**Test Case**: Verify JWT token is attached to API requests
- Given: User is authenticated with valid JWT token
- When: User performs an API call (e.g., fetch tasks)
- Then: Authorization header contains "Bearer {valid_token}"
- And: Request is processed successfully
- And: Response contains expected data

### T028: Test token refresh when token expires
**Test Case**: Token refresh functionality
- Given: User has an expiring JWT token
- When: Token is about to expire
- And: User makes an API request
- Then: Token is automatically refreshed
- And: New token is stored
- And: Request proceeds normally

### T029: Test secure token removal on logout
**Test Case**: Logout functionality
- Given: User is authenticated
- When: User clicks logout button
- And: Logout API call is made
- Then: JWT token is removed from localStorage
- And: User is redirected to login page
- And: Subsequent API calls fail with 401

## User Story 3: Backend Security Verification

### T033: Test valid JWT token access to protected endpoints
**Test Case**: Valid token access
- Given: User has a valid JWT token
- When: User makes request to protected endpoint (e.g., /api/tasks)
- Then: Request is processed successfully
- And: Response contains user's data

### T034: Test missing token response with 401 Unauthorized
**Test Case**: Missing token
- Given: User makes request without token
- When: User accesses protected endpoint
- Then: 401 Unauthorized response is returned
- And: Error message indicates authentication required

### T035: Test invalid/expired token response with 401 Unauthorized
**Test Case**: Invalid/expired token
- Given: User has an invalid or expired JWT token
- When: User accesses protected endpoint
- Then: 401 Unauthorized response is returned
- And: Error message indicates invalid credentials

### T036: Verify 99.9% JWT signature verification accuracy
**Test Case**: JWT verification accuracy
- Given: Multiple valid and invalid tokens
- When: Tokens are verified against the secret
- Then: Valid tokens pass verification
- And: Invalid tokens fail verification
- And: Accuracy rate is >= 99.9%

## User Story 4: User Data Isolation

### T040: Test user access to their own tasks
**Test Case**: User accesses own data
- Given: User has created tasks
- When: User fetches their tasks
- Then: Only user's tasks are returned
- And: All tasks belong to the authenticated user

### T041: Test prevention of access to other users' tasks
**Test Case**: User attempts to access others' data
- Given: Another user has created tasks
- When: User attempts to access other user's tasks
- Then: No other user's tasks are returned
- And: Request may return empty result or 404

### T042: Test task modification only for owner's tasks
**Test Case**: User modifies their own task
- Given: User owns a specific task
- When: User updates their task
- Then: Task is updated successfully
- And: Only the owner can modify the task

### T043: Verify zero cross-user data access with 100% accuracy
**Test Case**: Cross-user data isolation
- Given: Multiple users with their own data
- When: Users make requests for data
- Then: Users can only access their own data
- And: No cross-user data leakage occurs
- And: Accuracy is 100%