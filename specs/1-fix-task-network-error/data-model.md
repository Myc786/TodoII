# Data Model: API Configuration and Error Handling

## API Configuration Entity
- **api_base_url**: string - Base URL for API requests (default: http://localhost:8000/api)
- **headers**: object - HTTP headers to include with requests
- **auth_token**: string - Authentication token for protected endpoints
- **timeout**: number - Request timeout in milliseconds

## Network Error Entity
- **error_type**: enum('network', 'authentication', 'validation', 'server') - Type of error that occurred
- **message**: string - Human-readable error message
- **timestamp**: string - ISO date string when error occurred
- **request_details**: object - Details about the failed request
- **resolution_hint**: string - Suggested action for user to resolve issue

## Authentication Token Entity
- **token_value**: string - The JWT token string
- **expires_at**: string - ISO date string for token expiration
- **source**: enum('localStorage', 'nextauth_state', 'session') - Where token was retrieved from
- **user_id**: string - Associated user identifier
- **scopes**: array - Permissions granted by this token

## API Request Entity
- **method**: enum('GET', 'POST', 'PUT', 'PATCH', 'DELETE') - HTTP method
- **endpoint**: string - API endpoint path
- **headers**: object - Request headers
- **payload**: object - Request body data
- **response_status**: number - HTTP status code from response
- **response_data**: object - Response payload

## State Transitions
- API Configuration → Validated (when URL is confirmed accessible)
- Network Error → Resolved (when issue is fixed)
- Authentication Token → Refreshed (when token is renewed before expiration)
- API Request → Success/Failure (based on response status)