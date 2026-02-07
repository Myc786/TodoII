#!/usr/bin/env python3
"""
Script to migrate the database schema to add missing columns.
"""

import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def migrate_database():
    print("Starting database migration...")

    conn = sqlite3.connect('todo_app.db')
    cursor = conn.cursor()

    # Check current task table columns
    cursor.execute('PRAGMA table_info(task);')
    existing_columns = [col[1] for col in cursor.fetchall()]
    print(f"Existing task columns: {existing_columns}")

    # Define the columns we need to add based on the current model
    columns_to_add = [
        ('priority', 'TEXT DEFAULT \'medium\''),
        ('due_date', 'DATETIME'),
        ('recurrence_pattern', 'TEXT'),
        ('original_task_id', 'TEXT')  # TEXT instead of CHAR(32) for UUID
    ]

    for col_name, col_def in columns_to_add:
        if col_name not in existing_columns:
            try:
                alter_sql = f"ALTER TABLE task ADD COLUMN {col_name} {col_def};"
                print(f"Adding column {col_name}...")
                cursor.execute(alter_sql)
                print(f"SUCCESS: Successfully added column {col_name}")
            except sqlite3.OperationalError as e:
                print(f"⚠ Could not add column {col_name}: {e}")
        else:
            print(f"- Column {col_name} already exists")

    # Check reminder table as well
    cursor.execute('PRAGMA table_info(reminder);')
    reminder_columns = [col[1] for col in cursor.fetchall()]
    print(f"\nExisting reminder columns: {reminder_columns}")

    # Add missing reminder columns if needed
    reminder_columns_to_add = [
        ('id', 'TEXT PRIMARY KEY'),
        ('created_at', 'DATETIME DEFAULT CURRENT_TIMESTAMP'),
        ('sent_at', 'DATETIME')
    ]

    # For reminder table, we may need to handle differently if columns are missing
    for col_name, col_def in reminder_columns_to_add:
        if col_name not in reminder_columns:
            try:
                if col_name == 'id':
                    # If id is missing, we'd need a more complex migration
                    print(f"Note: Adding primary key {col_name} requires table recreation - skipping for now")
                else:
                    alter_sql = f"ALTER TABLE reminder ADD COLUMN {col_name} {col_def};"
                    print(f"Adding column {col_name} to reminder table...")
                    cursor.execute(alter_sql)
                    print(f"SUCCESS: Successfully added column {col_name} to reminder table")
            except sqlite3.OperationalError as e:
                print(f"⚠ Could not add column {col_name} to reminder: {e}")
        else:
            print(f"- Column {col_name} already exists in reminder table")

    # Check tag table
    cursor.execute('PRAGMA table_info(tag);')
    tag_columns = [col[1] for col in cursor.fetchall()]
    print(f"\nExisting tag columns: {tag_columns}")

    # Check tasktag table
    cursor.execute('PRAGMA table_info(tasktag);')
    tasktag_columns = [col[1] for col in cursor.fetchall()]
    print(f"Existing tasktag columns: {tasktag_columns}")

    conn.commit()
    conn.close()
    print("\nDatabase migration completed!")

if __name__ == "__main__":
    migrate_database()