#!/usr/bin/env python3
"""
Script to create a test user directly in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from src.models.user import User
from src.database.session import get_engine
from src.core.security import get_password_hash
from sqlmodel import Session, select

def create_test_user():
    # Create a test user directly in the database
    engine = get_engine()
    
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == "test@example.com")).first()
        
        if existing_user:
            print("Test user already exists!")
            return
        
        # Create a new test user
        hashed_password = get_password_hash("testpass123")
        test_user = User(
            email="test@example.com",
            name="Test User",
            password=hashed_password
        )
        
        session.add(test_user)
        session.commit()
        session.refresh(test_user)
        
        print(f"Test user created successfully with ID: {test_user.id}")

if __name__ == "__main__":
    create_test_user()