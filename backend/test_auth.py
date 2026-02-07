"""
Authentication System Test Suite

This script tests the authentication functionality of the backend application,
including user registration, login, logout, and protected endpoints.
"""

import pytest
import requests
import json
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
import uuid

# Base URL for the API (adjust as needed for your setup)
BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8000/api")

def test_register_new_user():
    """Test registering a new user account."""
    print("Testing user registration...")

    # Generate a unique email for testing
    test_email = f"test_{uuid.uuid4()}@example.com"
    test_password = "secure_password_123"
    test_name = "Test User"

    register_data = {
        "email": test_email,
        "name": test_name,
        "password": test_password
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)

    print(f"Register Response Status: {response.status_code}")
    print(f"Register Response: {response.json()}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Verify the response contains user data
    user_data = response.json()
    assert "id" in user_data
    assert user_data["email"] == test_email
    assert user_data["name"] == test_name

    print("✓ User registration successful")
    return user_data


def test_login_valid_credentials():
    """Test logging in with valid credentials."""
    print("\nTesting login with valid credentials...")

    # First, register a test user
    test_email = f"login_test_{uuid.uuid4()}@example.com"
    test_password = "secure_password_123"
    test_name = "Login Test User"

    register_data = {
        "email": test_email,
        "name": test_name,
        "password": test_password
    }

    register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    assert register_response.status_code == 200

    # Now try to login
    login_data = {
        "email": test_email,
        "password": test_password
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

    print(f"Login Response Status: {response.status_code}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Verify the response contains access token and user data
    login_response = response.json()
    assert "access_token" in login_response
    assert login_response["token_type"] == "bearer"
    assert "user" in login_response
    assert login_response["user"]["email"] == test_email

    print("✓ Login with valid credentials successful")
    return login_response


def test_login_invalid_credentials():
    """Test logging in with invalid credentials."""
    print("\nTesting login with invalid credentials...")

    # Try to login with non-existent user
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrong_password"
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

    print(f"Invalid Login Response Status: {response.status_code}")

    # Should return 401 Unauthorized
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"

    error_response = response.json()
    assert "detail" in error_response
    print(f"Error detail: {error_response['detail']}")

    print("✓ Login with invalid credentials correctly rejected")


def test_login_missing_credentials():
    """Test logging in with missing credentials."""
    print("\nTesting login with missing credentials...")

    # Try to login with empty data
    login_data = {}

    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

    print(f"Missing Credentials Response Status: {response.status_code}")

    # Should return 400 Bad Request
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    error_response = response.json()
    assert "detail" in error_response
    print(f"Error detail: {error_response['detail']}")

    print("✓ Login with missing credentials correctly rejected")


def test_protected_endpoint_without_token():
    """Test accessing a protected endpoint without a token."""
    print("\nTesting access to protected endpoint without token...")

    # Try to access /me endpoint without authorization header
    response = requests.get(f"{BASE_URL}/auth/me")

    print(f"Protected Endpoint Response Status: {response.status_code}")

    # Should return 401 Unauthorized
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"

    error_response = response.json()
    assert "detail" in error_response
    print(f"Error detail: {error_response['detail']}")

    print("✓ Protected endpoint correctly rejects requests without token")


def test_protected_endpoint_with_valid_token():
    """Test accessing a protected endpoint with a valid token."""
    print("\nTesting access to protected endpoint with valid token...")

    # First, register and login to get a token
    test_email = f"protected_test_{uuid.uuid4()}@example.com"
    test_password = "secure_password_123"
    test_name = "Protected Test User"

    # Register user
    register_data = {
        "email": test_email,
        "name": test_name,
        "password": test_password
    }

    register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    assert register_response.status_code == 200

    # Login to get token
    login_data = {
        "email": test_email,
        "password": test_password
    }

    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # Now access protected endpoint with token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)

    print(f"Protected Endpoint with Token Response Status: {response.status_code}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    user_data = response.json()
    assert user_data["email"] == test_email
    assert user_data["name"] == test_name

    print("✓ Protected endpoint successfully accessed with valid token")


def test_logout():
    """Test the logout functionality."""
    print("\nTesting logout functionality...")

    # First, register and login to get a token
    test_email = f"logout_test_{uuid.uuid4()}@example.com"
    test_password = "secure_password_123"
    test_name = "Logout Test User"

    # Register user
    register_data = {
        "email": test_email,
        "name": test_name,
        "password": test_password
    }

    register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    assert register_response.status_code == 200

    # Login to get token
    login_data = {
        "email": test_email,
        "password": test_password
    }

    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # Call logout endpoint
    response = requests.post(f"{BASE_URL}/auth/logout")

    print(f"Logout Response Status: {response.status_code}")

    # In JWT-based systems, logout typically returns 200 with success message
    # since the token is managed client-side
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    logout_response = response.json()
    assert "message" in logout_response
    assert logout_response["message"] == "Successfully logged out"

    print("✓ Logout functionality works as expected")


def test_duplicate_email_registration():
    """Test registering a user with an email that already exists."""
    print("\nTesting duplicate email registration...")

    # Register first user
    test_email = f"duplicate_test_{uuid.uuid4()}@example.com"
    test_password = "secure_password_123"
    test_name = "Duplicate Test User"

    register_data = {
        "email": test_email,
        "name": test_name,
        "password": test_password
    }

    register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    assert register_response.status_code == 200

    # Try to register another user with the same email
    duplicate_register_data = {
        "email": test_email,  # Same email
        "name": "Another User",
        "password": "another_password"
    }

    duplicate_response = requests.post(f"{BASE_URL}/auth/register", json=duplicate_register_data)

    print(f"Duplicate Registration Response Status: {duplicate_response.status_code}")

    # Should return 409 Conflict
    assert duplicate_response.status_code == 409, f"Expected 409, got {duplicate_response.status_code}"

    error_response = duplicate_response.json()
    assert "detail" in error_response
    print(f"Error detail: {error_response['detail']}")

    print("✓ Duplicate email registration correctly rejected")


def test_jwt_token_validation():
    """Test JWT token structure and validation."""
    print("\nTesting JWT token validation...")

    # Register and login to get a valid token
    test_email = f"jwt_test_{uuid.uuid4()}@example.com"
    test_password = "secure_password_123"
    test_name = "JWT Test User"

    register_data = {
        "email": test_email,
        "name": test_name,
        "password": test_password
    }

    register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    assert register_response.status_code == 200

    login_data = {
        "email": test_email,
        "password": test_password
    }

    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # Decode the token to verify its structure (without verification)
    try:
        decoded_token = jwt.decode(access_token, key="fake_key_for_testing", options={"verify_signature": False})
        print(f"Decoded token: {decoded_token}")

        # Check that token contains required claims
        assert "sub" in decoded_token, "Token missing 'sub' claim"
        assert "email" in decoded_token, "Token missing 'email' claim"
        assert "exp" in decoded_token, "Token missing 'exp' claim"

        # Verify that 'sub' contains user ID and 'email' contains email
        assert decoded_token["sub"] is not None, "'sub' claim should not be None"
        assert decoded_token["email"] == test_email, "Token email should match user email"

        print("✓ JWT token structure is valid")

    except JWTError as e:
        print(f"✗ JWT token validation failed: {e}")
        raise


def run_all_tests():
    """Run all authentication tests."""
    print("=" * 60)
    print("RUNNING AUTHENTICATION SYSTEM TESTS")
    print("=" * 60)

    try:
        test_register_new_user()
        test_login_valid_credentials()
        test_login_invalid_credentials()
        test_login_missing_credentials()
        test_protected_endpoint_without_token()
        test_protected_endpoint_with_valid_token()
        test_logout()
        test_duplicate_email_registration()
        test_jwt_token_validation()

        print("\n" + "=" * 60)
        print("ALL AUTHENTICATION TESTS PASSED! ✓")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        print("=" * 60)
        raise


if __name__ == "__main__":
    # Check if the API server is running
    try:
        health_check = requests.get(f"{BASE_URL}/docs", timeout=5)
        print(f"✓ API server is accessible at {BASE_URL}")
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to API server at {BASE_URL}")
        print("Please make sure your FastAPI server is running before executing tests.")
        exit(1)

    run_all_tests()