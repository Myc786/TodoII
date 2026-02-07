import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def test_connectivity():
    print(f"Testing connectivity to {BASE_URL}...")
    
    # 1. Check Health (we know this might be 404, but checking if it connects)
    try:
        resp = requests.get(f"http://localhost:8000/health")
        print(f"GET /health: {resp.status_code}")
    except Exception as e:
        print(f"GET /health FAILED: {e}")

    # 2. Check Tasks (Unauthorized expected)
    try:
        resp = requests.get(f"{BASE_URL}/tasks/")
        print(f"GET /tasks/: {resp.status_code}")
        # If 401, it means passing auth check -> Router is mounted!
        # If 404, router not mounted.
    except Exception as e:
        print(f"GET /tasks/ FAILED connecting: {e}")

    # 3. Create Task (Unauthorized expected)
    try:
        resp = requests.post(f"{BASE_URL}/tasks/", json={"title": "Test Ping"})
        print(f"POST /tasks/: {resp.status_code}")
    except Exception as e:
        print(f"POST /tasks/ FAILED connecting: {e}")

if __name__ == "__main__":
    test_connectivity()
