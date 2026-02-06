"""
Configure environment variables (secrets) for Hugging Face Space
This script will set all required secrets for production deployment
"""
import os
from huggingface_hub import HfApi

# Configuration
HF_TOKEN = os.getenv("HF_TOKEN")  # Set HF_TOKEN environment variable
SPACE_ID = "myc786/Part2"

# Generated secure secret
BETTER_AUTH_SECRET = "ghLw-JPwjxA6ed4YsWa5QxB3atOZsA0CZnKK6rgQ_xs"

# Database URL - Neon PostgreSQL
DATABASE_URL = "postgresql://neondb_owner:npg_NvRFm7In8Xxk@ep-ancient-pine-aiy0po7g-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

# AI Chatbot Configuration (Phase III)
# IMPORTANT: Set COHERE_API_KEY environment variable before running this script
COHERE_API_KEY = os.getenv("COHERE_API_KEY")  # Set via environment variable
OPENAI_COMPAT_BASE_URL = "https://api.cohere.ai/v1"
COHERE_MODEL_NAME = "command-r-plus"

# Environment variables to set
SECRETS = {
    "DATABASE_URL": DATABASE_URL,
    "BETTER_AUTH_SECRET": BETTER_AUTH_SECRET,
    "ENVIRONMENT": "production",
    "FRONTEND_URL": "https://frontend-mocha-beta-73.vercel.app",
    "COHERE_API_KEY": COHERE_API_KEY,
    "OPENAI_COMPAT_BASE_URL": OPENAI_COMPAT_BASE_URL,
    "COHERE_MODEL_NAME": COHERE_MODEL_NAME,
}

def set_secrets():
    """Set secrets for the Hugging Face Space."""

    # Validate DATABASE_URL
    if DATABASE_URL == "YOUR_DATABASE_URL_HERE" or not DATABASE_URL.startswith("postgresql://"):
        print("[ERROR] Please set a valid PostgreSQL DATABASE_URL in this script")
        print("\nYour DATABASE_URL should look like:")
        print("postgresql://username:password@hostname.neon.tech:5432/database?sslmode=require")
        print("\nEdit this file and replace 'YOUR_DATABASE_URL_HERE' with your actual connection string")
        return False

    api = HfApi(token=HF_TOKEN)

    print("=" * 60)
    print(f"Configuring secrets for space: {SPACE_ID}")
    print("=" * 60)

    success_count = 0
    for key, value in SECRETS.items():
        try:
            api.add_space_secret(
                repo_id=SPACE_ID,
                key=key,
                value=value,
            )
            # Don't print the actual secret values for security
            print(f"[OK] Set secret: {key}")
            success_count += 1
        except Exception as e:
            print(f"[FAIL] Failed to set {key}: {e}")

    print("\n" + "=" * 60)
    if success_count == len(SECRETS):
        print("[SUCCESS] All secrets configured successfully!")
    else:
        print(f"[WARNING] Configured {success_count}/{len(SECRETS)} secrets")
    print("=" * 60)

    print("\nNext Steps:")
    print("1. The Space will restart automatically (takes ~30 seconds)")
    print("2. Check logs: https://huggingface.co/spaces/myc786/Part2")
    print("3. Test health: curl https://myc786-part2.hf.space/health")
    print("4. Should show: {\"status\":\"healthy\",\"environment\":\"production\"}")

    return success_count == len(SECRETS)

def verify_secrets():
    """Verify secrets are set correctly."""
    print("\nVerifying secrets configuration...")

    import time
    import requests

    # Wait for space to restart
    print("Waiting for space to restart (30 seconds)...")
    time.sleep(30)

    try:
        response = requests.get("https://myc786-part2.hf.space/health")
        data = response.json()

        if data.get("environment") == "production":
            print("[SUCCESS] Backend is running in PRODUCTION mode")
            print(f"   Response: {data}")
            return True
        else:
            print(f"[WARNING] Backend is running in {data.get('environment')} mode")
            print(f"   Response: {data}")
            return False
    except Exception as e:
        print(f"[FAIL] Failed to verify: {e}")
        print("   Check manually: https://myc786-part2.hf.space/health")
        return False

if __name__ == "__main__":
    print("\n=== Hugging Face Space Configuration Tool ===")
    print("\nThis will configure the following secrets:")
    print("  - DATABASE_URL (PostgreSQL connection)")
    print("  - BETTER_AUTH_SECRET (JWT signing key)")
    print("  - ENVIRONMENT (set to 'production')")
    print("  - FRONTEND_URL (CORS configuration)")

    print("\nIMPORTANT: Edit this file and set DATABASE_URL before running!")
    print(f"   Current DATABASE_URL: {DATABASE_URL}")

    if DATABASE_URL == "YOUR_DATABASE_URL_HERE":
        print("\nERROR: Please edit configure_hf_secrets.py and set your DATABASE_URL")
        exit(1)

    print("\nStarting configuration...")

    if set_secrets():
        print("\n=== Configuration complete! ===")
        verify_secrets()
    else:
        print("\nERROR: Configuration failed. Check errors above.")
