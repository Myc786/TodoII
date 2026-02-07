#!/usr/bin/env python3
"""
Script to properly initialize the database with all tables and relationships.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.init_db import create_db_and_tables
from sqlmodel import SQLModel
from src.database.session import get_engine

def main():
    print("Initializing database...")

    # Create all tables
    create_db_and_tables()

    # Verify tables were created
    engine = get_engine()

    # Check if all expected tables exist
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    expected_tables = ['user', 'task', 'tag', 'tasktag', 'reminder']
    print(f"Existing tables: {tables}")

    for table in expected_tables:
        if table in tables:
            print(f"✓ Table '{table}' exists")
        else:
            print(f"✗ Table '{table}' missing")

    print("Database initialization completed!")

if __name__ == "__main__":
    main()