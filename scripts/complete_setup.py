#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
django.setup()

from django.contrib.auth.models import User
from django.core.management import execute_from_command_line
from datetime import datetime, timedelta
from django.utils import timezone

def complete_setup():
    """Complete setup of the exam management system"""
    
    print("🚀 Starting Exam Management System Setup...")
    print("=" * 50)
    
    # Step 1: Create migrations
    print("\n📝 Step 1: Creating migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        print("✓ Migrations created successfully")
    except Exception as e:
        print(f"⚠️  Warning: {e}")
    
    # Step 2: Apply migrations
    print("\n🗄️  Step 2: Creating database tables...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error applying migrations: {e}")
        return False
    
    # Step 3: Create superuser
    print("\n👤 Step 3: Creating admin user...")
    try:
        from exam_app.models import UserProfile
        
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='System',
                last_name='Administrator'
            )
            
            UserProfile.objects.create(
                user=admin_user,
                role='admin',
                phone='1234567890'
            )
            print("✓ Admin user created successfully")
            print("   Username: admin")
            print("   Password: admin123")
        else:
            print("✓ Admin user already exists")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False
    
    # Step 4: Create sample data
    print("\n📚 Step 4: Creating sample data...")
    try:
        create_sample_data()
        print("✓ Sample data created successfully")
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False
    
    # Step 5: Create static directory if it doesn't exist
    print("\n📁 Step 5: Creating static directory...")
    try:
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
            print(f"✓ Static directory created at {static_dir}")
        else:
            print("✓ Static directory already exists")
    except Exception as e:
        print(f"⚠️  Warning: Could not create static directory: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 What's been created:")
    print("   • Database tables")
    print("   • Admin user (admin/admin123)")
    print("   • Sample teachers and students")
    print("   • Sample courses and exams")
    print("\n🚀 Next steps:")
    print("   1. Run: python manage.py runserver")
    print("   2. Open: http://127.0.0.1:8000")
    print("   3. Login with admin/admin123")
    
    return True

def create_sample_data():
    """Create sample data for testing"""
    from exam_app.models import UserProfile, Course, Exam, Question, Choice
    
    # Create sample teachers
    if not User.objects.filter(username='teacher1').exists():
        teacher1 = User.objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='teacher123',
            first_name='John',
            last_name='Smith'
        )
        UserProfile.objects.create(user=teacher1, role='teacher', phone='1111111111')
    
    if not User.objects.filter(username='teacher2').exists():
        teacher2 = User.objects.create_user(
            username='teacher2',
            email='teacher2@example.com',
            password='teacher123',
            first_name='Jane',
            last_name='Doe'
        )
        UserProfile.objects.create(user=teacher2, role='teacher', phone='2222222222')
    
    # Create sample students
    for i in range(1, 4):  # Create 3 students
        if not User.objects.filter(username=f'student{i}').exists():
            student = User.objects.create_user(
                username=f'student{i}',
                email=f'student{i}@example.com',
                password='student123',
                first_name=f'Student',
                last_name=f'{i}'
            )
            UserProfile.objects.create(user=student, role='student', phone=f'555000{i:04d}')
    
    # Get teachers
    teacher1 = User.objects.get(username='teacher1')
    teacher2 = User.objects.get(username='teacher2')
    
    # Create sample courses
    if not Course.objects.filter(code='CS101').exists():
        course1 = Course.objects.create(
            name='Introduction to Computer Science',
            code='CS101',
            description='Basic concepts of computer science and programming',
            teacher=teacher1
        )
    
    if not Course.objects.filter(code='CS201').exists():
        course2 = Course.objects.create(
            name='Database Management Systems',
            code='CS201',
            description='Fundamentals of database design and management',
            teacher=teacher2
        )
    
    # Get courses
    course1 = Course.objects.get(code='CS101')
    course2 = Course.objects.get(code='CS201')
    
    # Create sample exams
    now = timezone.now()
    
    if not Exam.objects.filter(title='CS101 Sample Exam').exists():
        exam1 = Exam.objects.create(
            title='CS101 Sample Exam',
            course=course1,
            description='Sample examination for testing the system',
            duration_minutes=60,
            total_marks=30,
            passing_marks=18,
            start_time=now,
            end_time=now + timedelta(days=30),
            is_active=True
        )
        
        # Create sample questions
        q1 = Question.objects.create(
            exam=exam1,
            question_text='What is the primary purpose of a compiler?',
            question_type='mcq',
            marks=10
        )
        
        Choice.objects.create(question=q1, choice_text='To execute programs directly', is_correct=False)
        Choice.objects.create(question=q1, choice_text='To translate source code to machine code', is_correct=True)
        Choice.objects.create(question=q1, choice_text='To debug programs', is_correct=False)
        Choice.objects.create(question=q1, choice_text='To manage memory', is_correct=False)
        
        q2 = Question.objects.create(
            exam=exam1,
            question_text='Which of the following is a programming language?',
            question_type='mcq',
            marks=10
        )
        
        Choice.objects.create(question=q2, choice_text='HTML', is_correct=False)
        Choice.objects.create(question=q2, choice_text='CSS', is_correct=False)
        Choice.objects.create(question=q2, choice_text='Python', is_correct=True)
        Choice.objects.create(question=q2, choice_text='JSON', is_correct=False)
        
        q3 = Question.objects.create(
            exam=exam1,
            question_text='Explain the concept of Object-Oriented Programming.',
            question_type='descriptive',
            marks=10
        )

if __name__ == '__main__':
    complete_setup()
