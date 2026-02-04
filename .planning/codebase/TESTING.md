# Testing Patterns

**Analysis Date:** 2026-02-04

## Test Framework

**Backend:**
- Runner: pytest (from pyproject.toml dependencies)
- Config: Not explicitly configured in standard pytest.ini/pyproject.toml sections
- Assertion Library: Built-in Python assertions and pytest assertions
- Run Commands:
```bash
pytest                           # Run all tests
pytest --cov                     # Run with coverage
pytest tests/                    # Run tests in specific directory
```

**Frontend:**
- Testing: Not implemented (no Jest, Vitest, or other frontend test frameworks detected)

## Test File Organization

**Location:**
- Backend: `backend/tests/` directory and standalone test files in `backend/`
- Frontend: No test files detected

**Naming:**
- Python: `test_*.py` and `*_test.py` patterns (e.g., `test_crud_endpoints.py`, `test_auth.py`)
- Structure:
```
backend/
├── test_*.py           # Standalone test files
└── tests/              # Test package directory
    ├── test_*.py       # Module-specific tests
    └── conftest.py     # Test configuration (if exists)
```

## Test Structure

**Backend Test Patterns:**
```python
def test_specific_functionality():
    """Descriptive docstring explaining what is being tested."""
    # Setup
    test_data = {...}

    # Execution
    result = function_or_api_call(test_data)

    # Assertions
    assert result.condition == expected_value
    assert "key" in result_dict
```

**API Integration Tests:**
- Use requests library to make actual HTTP calls
- Test both positive and negative cases
- Include comprehensive status code assertions
- Verify response structure and content

**Service Layer Tests:**
- Direct instantiation and method calls
- Database session management
- Transaction rollbacks for cleanup
- Comprehensive CRUD operation testing

## Mocking

**Backend:**
- Framework: Not explicitly using mocking library (unittest.mock or pytest-mock)
- Patterns: Manual test data generation (e.g., uuid.uuid4() for unique emails)
- What to Mock: Not commonly used; prefer real database interactions for integration tests
- What NOT to Mock: Database connections and core business logic

## Fixtures and Factories

**Test Data:**
```python
# Generate unique test data
test_email = f"test_{uuid.uuid4()}@example.com"
test_password = "secure_password_123"
```

**Location:**
- Test data generated inline within test functions
- No centralized fixture files detected

## Coverage

**Requirements:** Not explicitly enforced in configuration
**View Coverage:**
```bash
pytest --cov=src --cov-report=html
```

## Test Types

**Unit Tests:**
- Not detected; backend tests appear to be integration tests

**Integration Tests:**
- API endpoint testing (e.g., `test_auth.py`)
- Full CRUD operation testing (e.g., `test_crud_endpoints.py`)
- Database interaction testing with real sessions
- End-to-end workflow testing

**E2E Tests:**
- Not detected in current codebase

## Common Patterns

**Setup/Teardown:**
- Manual cleanup within tests
- Database record cleanup using service methods
- Unique identifiers to prevent test interference

**Async Testing:**
- Not detected; synchronous testing patterns used

**Error Testing:**
```python
# Positive case
response = requests.post(...)
assert response.status_code == 200

# Negative case
response = requests.post(...)  # Invalid input
assert response.status_code == 401  # Or other appropriate error code
```

**Test Organization:**
- Related tests grouped in functions (e.g., `test_login_valid_credentials`)
- Comprehensive test suites with multiple scenarios
- Descriptive test names indicating specific functionality
- Sequential test execution in single test runs

## Backend Test Categories

**Authentication Tests:** (`test_auth.py`)
- User registration
- Valid/invalid login credentials
- Protected endpoint access
- JWT token validation
- Duplicate registration handling

**CRUD Operation Tests:** (`test_crud_endpoints.py`)
- Full Create, Read, Update, Delete cycle
- Database transaction handling
- Error condition testing
- Data integrity verification

**System Tests:** (`tests/` directory)
- Chatbot integration
- MCP tools unit tests
- Security measures
- Various functional tests

---

*Testing analysis: 2026-02-04*