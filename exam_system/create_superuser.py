# exam_system/create_superuser.py

import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exam_system.settings")
django.setup()

User = get_user_model()

username = "admin"
email = "admin@example.com"
password = "admin123"  # Change this later!

if not User.objects.filter(username=username).exists():
    print("Creating superuser...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully.")
else:
    print("Superuser already exists.")
