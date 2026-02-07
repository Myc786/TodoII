import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("BETTER_AUTH_SECRET from environment:", os.getenv("BETTER_AUTH_SECRET"))

# Now start the server with proper env loading
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )