#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
django.setup()

from django.contrib.auth.models import User
from exam_app.models import UserProfile, Course, Exam, Question, Choice
from django.utils import timezone

def create_sample_data():
    """Create sample data for testing"""
    
    print("Creating sample data...")
    
    # Create sample teachers
    teacher1 = User.objects.create_user(
        username='teacher1',
        email='teacher1@example.com',
        password='teacher123',
        first_name='John',
        last_name='Smith'
    )
    UserProfile.objects.create(user=teacher1, role='teacher', phone='1111111111')
    
    teacher2 = User.objects.create_user(
        username='teacher2',
        email='teacher2@example.com',
        password='teacher123',
        first_name='Jane',
        last_name='Doe'
    )
    UserProfile.objects.create(user=teacher2, role='teacher', phone='2222222222')
    
    # Create sample students
    for i in range(1, 6):
        student = User.objects.create_user(
            username=f'student{i}',
            email=f'student{i}@example.com',
            password='student123',
            first_name=f'Student',
            last_name=f'{i}'
        )
        UserProfile.objects.create(user=student, role='student', phone=f'555000{i:04d}')
    
    # Create sample courses
    course1 = Course.objects.create(
        name='Introduction to Computer Science',
        code='CS101',
        description='Basic concepts of computer science and programming',
        teacher=teacher1
    )
    
    course2 = Course.objects.create(
        name='Database Management Systems',
        code='CS201',
        description='Fundamentals of database design and management',
        teacher=teacher2
    )
    
    course3 = Course.objects.create(
        name='Web Development',
        code='CS301',
        description='Modern web development technologies and frameworks',
        teacher=teacher1
    )
    
    # Create sample exams
    now = timezone.now()
    
    exam1 = Exam.objects.create(
        title='CS101 Midterm Exam',
        course=course1,
        description='Midterm examination covering basic programming concepts',
        duration_minutes=90,
        total_marks=50,
        passing_marks=25,
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=7),
        is_active=True
    )
    
    exam2 = Exam.objects.create(
        title='Database Fundamentals Quiz',
        course=course2,
        description='Quick quiz on database basics',
        duration_minutes=30,
        total_marks=20,
        passing_marks=12,
        start_time=now,
        end_time=now + timedelta(days=3),
        is_active=True
    )
    
    # Create sample questions for exam1
    q1 = Question.objects.create(
        exam=exam1,
        question_text='What is the primary purpose of a compiler?',
        question_type='mcq',
        marks=5
    )
    
    Choice.objects.create(question=q1, choice_text='To execute programs directly', is_correct=False)
    Choice.objects.create(question=q1, choice_text='To translate source code to machine code', is_correct=True)
    Choice.objects.create(question=q1, choice_text='To debug programs', is_correct=False)
    Choice.objects.create(question=q1, choice_text='To manage memory', is_correct=False)
    
    q2 = Question.objects.create(
        exam=exam1,
        question_text='Which of the following is NOT a programming paradigm?',
        question_type='mcq',
        marks=5
    )
    
    Choice.objects.create(question=q2, choice_text='Object-Oriented Programming', is_correct=False)
    Choice.objects.create(question=q2, choice_text='Functional Programming', is_correct=False)
    Choice.objects.create(question=q2, choice_text='Procedural Programming', is_correct=False)
    Choice.objects.create(question=q2, choice_text='Database Programming', is_correct=True)
    
    q3 = Question.objects.create(
        exam=exam1,
        question_text='Explain the difference between a stack and a queue data structure.',
        question_type='descriptive',
        marks=10
    )
    
    # Create sample questions for exam2
    q4 = Question.objects.create(
        exam=exam2,
        question_text='What does SQL stand for?',
        question_type='mcq',
        marks=5
    )
    
    Choice.objects.create(question=q4, choice_text='Structured Query Language', is_correct=True)
    Choice.objects.create(question=q4, choice_text='Simple Query Language', is_correct=False)
    Choice.objects.create(question=q4, choice_text='Standard Query Language', is_correct=False)
    Choice.objects.create(question=q4, choice_text='System Query Language', is_correct=False)
    
    q5 = Question.objects.create(
        exam=exam2,
        question_text='Which of the following is a NoSQL database?',
        question_type='mcq',
        marks=5
    )
    
    Choice.objects.create(question=q5, choice_text='MySQL', is_correct=False)
    Choice.objects.create(question=q5, choice_text='PostgreSQL', is_correct=False)
    Choice.objects.create(question=q5, choice_text='MongoDB', is_correct=True)
    Choice.objects.create(question=q5, choice_text='Oracle', is_correct=False)
    
    print("Sample data created successfully!")
    print("\nSample Users Created:")
    print("Teachers: teacher1/teacher123, teacher2/teacher123")
    print("Students: student1/student123, student2/student123, ..., student5/student123")
    print("\nSample Courses and Exams have been created.")

if __name__ == '__main__':
    create_sample_data()
