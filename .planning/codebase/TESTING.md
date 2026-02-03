# Testing Patterns

**Analysis Date:** 2026-02-03

## Test Framework

**Runner:**
- Pytest [7.4.0+] - Backend Python tests
- Config: `pyproject.toml` (Poetry configuration)
- Run Commands:
```bash
pytest                          # Run all tests
pytest --cov=src               # Run with coverage
pytest tests/unit             # Run unit tests only
pytest tests/integration    # Run integration tests only
```

**Assertion Library:**
- Pytest built-in assertions

**Frontend Testing:**
- Not currently implemented (no *.test.* or *.spec.* files found)

## Test File Organization

**Location:**
- Backend tests: `backend/tests/` directory with subdirectories for different test types
- Unit tests: `backend/tests/unit/`
- Integration tests: `backend/tests/integration/`
- Contract tests: `backend/tests/contract/`

**Naming:**
- Test files: `test_*.py` or `*_test.py` pattern
- Test functions: `test_*` prefix (e.g., `test_register_new_user`)

**Structure:**
```
backend/tests/
├── unit/           # Unit tests for individual functions/classes
├── integration/    # Integration tests for API endpoints
├── contract/       # Contract tests for API compliance
└── *.py           # Standalone test files
```

## Test Structure

**Suite Organization:**
```python
def test_specific_behavior():
    """Descriptive docstring explaining what is being tested."""
    # Arrange
    # Setup test data

    # Act
    # Execute the function/method being tested

    # Assert
    # Verify expected outcomes
```

**Patterns:**
- Arrange-Act-Assert structure
- Descriptive function names
- Docstrings for test purpose explanation
- Print statements for debugging test runs

## Mocking

**Framework:** Not explicitly using mock library in current tests

**Patterns:**
- Currently using real HTTP requests to test API endpoints
- Test isolation achieved through unique test data generation (UUIDs)
- Environment variables for test configuration

**What to Mock:**
- External API calls
- Database connections in unit tests
- Time-dependent operations

## Fixtures and Factories

**Test Data:**
```python
# Using UUIDs to generate unique test data
test_email = f"test_{uuid.uuid4()}@example.com"
```

**Location:**
- Test data generated within individual test functions
- No centralized fixture files currently

## Coverage

**Requirements:** Not explicitly enforced in current configuration

**View Coverage:**
```bash
pytest --cov=src --cov-report=html
```

## Test Types

**Unit Tests:**
- Individual function/class testing
- Currently limited in the codebase

**Integration Tests:**
- Full API endpoint testing using HTTP requests
- End-to-end workflow testing
- Example: Authentication system tests (`test_auth.py`)

**E2E Tests:**
- Not implemented in current codebase

## Common Patterns

**Async Testing:**
- Not currently used (FastAPI async endpoints tested with sync HTTP requests)

**Error Testing:**
```python
def test_login_invalid_credentials():
    """Test logging in with invalid credentials."""
    # Test setup
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrong_password"
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

    # Verify error response
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"

    error_response = response.json()
    assert "detail" in error_response
```

**Setup/Cleanup:**
- Test data uniqueness achieved through UUID generation
- No explicit setup/teardown functions in current tests
- Each test creates its own test user to ensure isolation

---

*Testing analysis: 2026-02-03*