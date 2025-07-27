#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
django.setup()

from django.core.management import execute_from_command_line

def create_database():
    """Create database tables and apply migrations"""
    print("Creating database tables...")
    
    # Make migrations
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Apply migrations
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Database created successfully!")

if __name__ == '__main__':
    create_database()
