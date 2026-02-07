"""
Test script to verify the authentication endpoints work correctly.
"""
import requests
import json
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

BASE_URL = "http://localhost:8000/api"

def test_forgot_password():
    """Test the forgot password endpoint"""
    print("Testing forgot password endpoint...")

    # Test with a non-existent email
    response = requests.post(f"{BASE_URL}/auth/forgot-password",
                            json={"email": "nonexistent@example.com"})
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json()}")

    # Test with a valid email format (but might not exist)
    response = requests.post(f"{BASE_URL}/auth/forgot-password",
                            json={"email": "test@example.com"})
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json()}")

    print("Forgot password test completed.\n")

def test_reset_password():
    """Test the reset password endpoint"""
    print("Testing reset password endpoint...")

    # Test with invalid data
    response = requests.post(f"{BASE_URL}/auth/reset-password",
                            json={})
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json()}")

    # Test with valid data format (but invalid token)
    response = requests.post(f"{BASE_URL}/auth/reset-password",
                            json={
                                "token": "invalid-token",
                                "new_password": "newpassword123"
                            })
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json()}")

    print("Reset password test completed.\n")

def test_login_and_register():
    """Test the existing login and register endpoints"""
    print("Testing login and register endpoints...")

    # Test registration
    register_data = {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Register response status: {response.status_code}")
    if response.status_code == 200:
        print("Registration successful")
        user_data = response.json()
        print(f"User created: {user_data.get('email')}")
    elif response.status_code == 409:
        print("User already exists (expected for repeated tests)")
    else:
        print(f"Registration failed: {response.json()}")

    # Test login
    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login response status: {response.status_code}")
    if response.status_code == 200:
        print("Login successful")
        auth_data = response.json()
        print(f"Access token received: {'access_token' in auth_data}")
    else:
        print(f"Login failed: {response.json()}")

    print("Login and register test completed.\n")

if __name__ == "__main__":
    print("Starting authentication endpoint tests...\n")

    try:
        # Test existing functionality
        test_login_and_register()

        # Test new functionality
        test_forgot_password()
        test_reset_password()

        print("All tests completed!")

    except Exception as e:
        print(f"Error during testing: {str(e)}")
        print("Make sure the backend server is running on http://localhost:8000")