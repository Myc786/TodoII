import requests

def test_api_health():
    """Test the health endpoint of the running API."""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("[SUCCESS] API health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"[ERROR] API health check failed with status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Error connecting to API: {str(e)}")

if __name__ == "__main__":
    test_api_health()