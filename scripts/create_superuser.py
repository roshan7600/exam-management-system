#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
django.setup()

from django.contrib.auth.models import User
from exam_app.models import UserProfile

def create_superuser():
    """Create a superuser for admin access"""
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("Superuser already exists!")
        return
    
    # Create superuser
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        first_name='System',
        last_name='Administrator'
    )
    
    # Create user profile
    UserProfile.objects.create(
        user=admin_user,
        role='admin',
        phone='1234567890'
    )
    
    print("Superuser created successfully!")
    print("Username: admin")
    print("Password: admin123")

if __name__ == '__main__':
    create_superuser()
