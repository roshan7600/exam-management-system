#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
django.setup()

def setup_database():
    """Set up the database with proper migrations"""
    
    print("Setting up Django environment...")
    
    print("Creating migrations...")
    try:
        # Create migrations for exam_app
        execute_from_command_line(['manage.py', 'makemigrations', 'exam_app'])
        print("✓ Migrations created successfully")
    except Exception as e:
        print(f"Error creating migrations: {e}")
        return False
    
    print("Applying migrations...")
    try:
        # Apply all migrations
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"Error applying migrations: {e}")
        return False
    
    return True

if __name__ == '__main__':
    if setup_database():
        print("\n✓ Database setup completed successfully!")
        print("You can now run: python manage.py runserver")
    else:
        print("\n✗ Database setup failed!")
