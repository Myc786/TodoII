#!/usr/bin/env python3
"""
Test script to validate Cohere API 422 error fixes.
"""

import os
import sys
import asyncio
from unittest.mock import Mock, patch

# Add backend src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Add the current directory to Python path to resolve imports
sys.path.insert(0, os.path.dirname(__file__))

from src.ai.config import get_openai_client, get_model_name
from src.ai.agent import ChatAgent


def test_cohere_configuration():
    """Test that Cohere configuration loads properly."""
    print("Testing Cohere configuration...")

    # Set up environment variables for testing
    os.environ['COHERE_API_KEY'] = 'test-key'
    os.environ['OPENAI_COMPAT_BASE_URL'] = 'https://api.cohere.ai/compatibility/v1'
    os.environ['COHERE_MODEL_NAME'] = 'command-r-plus-08-2024'

    # Test client creation
    try:
        client = get_openai_client()
        print(f"[OK] Client created successfully: {type(client).__name__}")
    except Exception as e:
        print(f"[ERROR] Failed to create client: {e}")
        return False

    # Test model name retrieval
    model_name = get_model_name()
    print(f"[OK] Model name retrieved: {model_name}")

    if model_name != 'command-r-plus-08-2024':
        print(f"[ERROR] Expected 'command-r-plus-08-2024', got '{model_name}'")
        return False

    return True


def test_agent_initialization():
    """Test that ChatAgent initializes properly."""
    print("\nTesting ChatAgent initialization...")

    # Set up environment variables for testing
    os.environ['COHERE_API_KEY'] = 'test-key'
    os.environ['OPENAI_COMPAT_BASE_URL'] = 'https://api.cohere.ai/compatibility/v1'
    os.environ['COHERE_MODEL_NAME'] = 'command-r-plus-08-2024'

    try:
        agent = ChatAgent()
        print(f"[OK] Agent created successfully")
        print(f"  - Model: {agent.model}")
        print(f"  - Instructions length: {len(agent.instructions)} chars")
        print(f"  - Number of tools: {len(agent.tools)}")

        # Check that tools are properly formatted
        for tool in agent.tools:
            if 'function' not in tool:
                print(f"[ERROR] Tool missing 'function' key: {tool}")
                return False
            if 'name' not in tool['function']:
                print(f"[ERROR] Tool function missing 'name': {tool}")
                return False

        print("[OK] All tools properly formatted")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to create agent: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_format_message_history():
    """Test message history formatting."""
    print("\nTesting message history formatting...")

    os.environ['COHERE_API_KEY'] = 'test-key'
    os.environ['COHERE_MODEL_NAME'] = 'command-r-plus-08-2024'

    agent = ChatAgent()

    # Test with empty history
    messages = []
    formatted = agent.format_message_history(messages)
    print(f"[OK] Empty history formatted: {len(formatted)} messages")

    # Test with sample messages
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    formatted = agent.format_message_history(messages)

    # Should have system message + user + assistant = 3 total
    if len(formatted) != 3:
        print(f"[ERROR] Expected 3 messages, got {len(formatted)}")
        return False

    if formatted[0]["role"] != "system":
        print(f"[ERROR] First message should be system, got {formatted[0]['role']}")
        return False

    print("[OK] Message history formatting works correctly")
    return True


def run_tests():
    """Run all tests."""
    print("Running Cohere API 422 error fix tests...\n")

    tests = [
        test_cohere_configuration,
        test_agent_initialization,
        test_format_message_history,
    ]

    passed = 0
    total = len(tests)

    for test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_func.__name__} failed")

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("V All tests passed! Cohere API 422 error fixes are working correctly.")
        return True
    else:
        print("X Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)