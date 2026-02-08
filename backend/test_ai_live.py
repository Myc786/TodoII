
import os
import sys
from dotenv import load_dotenv

# Add backend src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Load .env file
load_dotenv()

from src.ai.config import get_openai_client, get_model_name

def test_live_ai():
    print("Testing Live Cohere API Connectivity...")
    
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        print("[FAIL] COHERE_API_KEY not found in .env")
        return False

    # Strip any potential trailing/leading whitespace
    api_key = api_key.strip()
    print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")
    
    try:
        client = get_openai_client()
        model = get_model_name()
        
        print(f"Client Base URL: {client.base_url}")
        print(f"Model: {model}")
        
        print("Sending test greeting...")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello, are you working properly?"}],
            max_tokens=50
        )
        
        content = response.choices[0].message.content
        print(f"[SUCCESS] Received response: {content}")
        return True
        
    except Exception as e:
        print(f"[FAIL] AI connectivity test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_live_ai()
