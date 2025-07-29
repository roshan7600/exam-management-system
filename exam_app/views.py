from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Count, Avg
from .models import UserProfile, Course, Exam, Question, Choice, ExamAttempt, StudentAnswer
import json
import random
from .models import UserProfile

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Invalid username or password.')
#     return render(request, 'auth/login.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                role = user.userprofile.role
            except UserProfile.DoesNotExist:
                messages.error(request, 'User role not defined.')
                return redirect('login')

            if role == 'admin':
                return redirect('admin_panel')
            elif role == 'teacher':
                return redirect('teacher_panel')
            elif role == 'student':
                return redirect('student_panel')
            else:
                messages.error(request, 'Unknown user role.')
                return redirect('login')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'auth/login.html')



def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']
        phone = request.POST.get('phone', '')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'auth/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'auth/register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()
        
        UserProfile.objects.create(user=user, role=role, phone=phone)
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    
    return render(request, 'auth/register.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    try:
        profile = request.user.userprofile
        role = profile.role
        
        if role == 'admin':
            return redirect('admin_panel')
        elif role == 'teacher':
            return redirect('teacher_panel')
        elif role == 'student':
            return redirect('student_panel')
    except UserProfile.DoesNotExist:
        # Create a default profile if it doesn't exist
        UserProfile.objects.create(user=request.user, role='student')
        messages.info(request, 'Profile created. Please update your role if needed.')
        return redirect('dashboard')
    except Exception as e:
        messages.error(request, f'Error accessing dashboard: {str(e)}')
        return redirect('login')
    
    return render(request, 'dashboard.html')

# Admin Views
@login_required
def admin_panel(request):
    if request.user.userprofile.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    total_users = User.objects.count()
    total_courses = Course.objects.count()
    total_exams = Exam.objects.count()
    total_attempts = ExamAttempt.objects.count()
    
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_courses = Course.objects.order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_courses': total_courses,
        'total_exams': total_exams,
        'total_attempts': total_attempts,
        'recent_users': recent_users,
        'recent_courses': recent_courses,
    }
    return render(request, 'admin/admin_panel.html', context)

@login_required
def manage_users(request):
    if request.user.userprofile.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    users = User.objects.select_related('userprofile').all()
    return render(request, 'admin/manage_users.html', {'users': users})

@login_required
def manage_courses(request):
    if request.user.userprofile.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    courses = Course.objects.select_related('teacher').all()
    return render(request, 'admin/manage_courses.html', {'courses': courses})

@login_required
def add_course(request):
    if request.user.userprofile.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']
        description = request.POST['description']
        teacher_id = request.POST['teacher']
        
        teacher = get_object_or_404(User, id=teacher_id, userprofile__role='teacher')
        
        if Course.objects.filter(code=code).exists():
            messages.error(request, 'Course code already exists.')
        else:
            Course.objects.create(
                name=name,
                code=code,
                description=description,
                teacher=teacher
            )
            messages.success(request, 'Course created successfully.')
            return redirect('manage_courses')
    
    teachers = User.objects.filter(userprofile__role='teacher')
    return render(request, 'admin/add_course.html', {'teachers': teachers})

@login_required
def edit_course(request, course_id):
    if request.user.userprofile.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        course.name = request.POST['name']
        course.code = request.POST['code']
        course.description = request.POST['description']
        teacher_id = request.POST['teacher']
        course.teacher = get_object_or_404(User, id=teacher_id, userprofile__role='teacher')
        course.is_active = 'is_active' in request.POST
        course.save()
        
        messages.success(request, 'Course updated successfully.')
        return redirect('manage_courses')
    
    teachers = User.objects.filter(userprofile__role='teacher')
    return render(request, 'admin/edit_course.html', {'course': course, 'teachers': teachers})

@login_required
def delete_course(request, course_id):
    if request.user.userprofile.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, 'Course deleted successfully.')
    return redirect('manage_courses')

# Teacher Views
@login_required
def teacher_panel(request):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    my_courses = Course.objects.filter(teacher=request.user)
    my_exams = Exam.objects.filter(course__teacher=request.user)
    total_attempts = ExamAttempt.objects.filter(exam__course__teacher=request.user).count()
    
    context = {
        'my_courses': my_courses,
        'my_exams': my_exams,
        'total_attempts': total_attempts,
    }
    return render(request, 'teacher/teacher_panel.html', context)

@login_required
def my_courses(request):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'teacher/my_courses.html', {'courses': courses})

@login_required
def create_exam(request):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = request.POST['title']
        course_id = request.POST['course']
        description = request.POST['description']
        duration_minutes = int(request.POST['duration_minutes'])
        total_marks = int(request.POST['total_marks'])
        passing_marks = int(request.POST['passing_marks'])
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        
        course = get_object_or_404(Course, id=course_id, teacher=request.user)
        
        exam = Exam.objects.create(
            title=title,
            course=course,
            description=description,
            duration_minutes=duration_minutes,
            total_marks=total_marks,
            passing_marks=passing_marks,
            start_time=start_time,
            end_time=end_time
        )
        
        messages.success(request, 'Exam created successfully.')
        return redirect('exam_details', exam_id=exam.id)
    
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'teacher/create_exam.html', {'courses': courses})

@login_required
def manage_exams(request):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    exams = Exam.objects.filter(course__teacher=request.user)
    return render(request, 'teacher/manage_exams.html', {'exams': exams})

@login_required
def exam_details(request, exam_id):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    exam = get_object_or_404(Exam, id=exam_id, course__teacher=request.user)
    questions = exam.questions.all()
    return render(request, 'teacher/exam_details.html', {'exam': exam, 'questions': questions})

@login_required
def add_question(request, exam_id):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    exam = get_object_or_404(Exam, id=exam_id, course__teacher=request.user)
    
    if request.method == 'POST':
        question_text = request.POST['question_text']
        question_type = request.POST['question_type']
        marks = int(request.POST['marks'])
        
        question = Question.objects.create(
            exam=exam,
            question_text=question_text,
            question_type=question_type,
            marks=marks
        )
        
        if question_type == 'mcq':
            choices = [
                request.POST.get('choice1', ''),
                request.POST.get('choice2', ''),
                request.POST.get('choice3', ''),
                request.POST.get('choice4', '')
            ]
            correct_choice = int(request.POST['correct_choice']) - 1
            
            for i, choice_text in enumerate(choices):
                if choice_text.strip():
                    Choice.objects.create(
                        question=question,
                        choice_text=choice_text,
                        is_correct=(i == correct_choice)
                    )
        
        messages.success(request, 'Question added successfully.')
        return redirect('exam_details', exam_id=exam.id)
    
    return render(request, 'teacher/add_question.html', {'exam': exam})

@login_required
def edit_question(request, question_id):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    question = get_object_or_404(Question, id=question_id, exam__course__teacher=request.user)
    
    if request.method == 'POST':
        question.question_text = request.POST['question_text']
        question.marks = int(request.POST['marks'])
        question.save()
        
        if question.question_type == 'mcq':
            # Update choices
            choices = question.choices.all()
            choice_texts = [
                request.POST.get('choice1', ''),
                request.POST.get('choice2', ''),
                request.POST.get('choice3', ''),
                request.POST.get('choice4', '')
            ]
            correct_choice = int(request.POST['correct_choice']) - 1
            
            for i, choice in enumerate(choices):
                if i < len(choice_texts) and choice_texts[i].strip():
                    choice.choice_text = choice_texts[i]
                    choice.is_correct = (i == correct_choice)
                    choice.save()
        
        messages.success(request, 'Question updated successfully.')
        return redirect('exam_details', exam_id=question.exam.id)
    
    return render(request, 'teacher/edit_question.html', {'question': question})

@login_required
def delete_question(request, question_id):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    question = get_object_or_404(Question, id=question_id, exam__course__teacher=request.user)
    exam_id = question.exam.id
    question.delete()
    messages.success(request, 'Question deleted successfully.')
    return redirect('exam_details', exam_id=exam_id)

@login_required
def exam_results(request, exam_id):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    exam = get_object_or_404(Exam, id=exam_id, course__teacher=request.user)
    attempts = ExamAttempt.objects.filter(exam=exam, is_completed=True)
    
    # Calculate statistics
    total_attempts = attempts.count()
    passed_count = 0
    total_score = 0
    
    # Add percentage and duration to each attempt
    attempts_with_stats = []
    for attempt in attempts:
        attempt_data = {
            'attempt': attempt,
            'percentage': 0,
            'duration': None
        }
        
        if attempt.score is not None:
            percentage = (attempt.score * 100) / exam.total_marks
            attempt_data['percentage'] = round(percentage, 1)
            total_score += attempt.score
            
            if attempt.score >= exam.passing_marks:
                passed_count += 1
        
        # Calculate duration
        if attempt.end_time and attempt.start_time:
            duration_seconds = (attempt.end_time - attempt.start_time).total_seconds()
            duration_minutes = int(duration_seconds // 60)
            duration_seconds = int(duration_seconds % 60)
            attempt_data['duration'] = f"{duration_minutes}m {duration_seconds}s"
        
        attempts_with_stats.append(attempt_data)
    
    pass_rate = (passed_count * 100 / total_attempts) if total_attempts > 0 else 0
    average_score = (total_score / total_attempts) if total_attempts > 0 else 0
    
    context = {
        'exam': exam,
        'attempts_with_stats': attempts_with_stats,
        'total_attempts': total_attempts,
        'passed_count': passed_count,
        'pass_rate': round(pass_rate, 1),
        'average_score': round(average_score, 1),
    }
    return render(request, 'teacher/exam_results.html', context)

# Student Views
@login_required
def student_panel(request):
    if request.user.userprofile.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    available_exams = Exam.objects.filter(is_active=True, start_time__lte=timezone.now(), end_time__gte=timezone.now())
    my_attempts = ExamAttempt.objects.filter(student=request.user, is_completed=True)
    
    # Calculate average score
    total_score = 0
    total_possible = 0
    for attempt in my_attempts:
        if attempt.score is not None:
            total_score += attempt.score
            total_possible += attempt.exam.total_marks
    
    average_percentage = (total_score * 100 / total_possible) if total_possible > 0 else 0
    
    context = {
        'available_exams': available_exams,
        'my_attempts': my_attempts,
        'average_percentage': round(average_percentage, 1),
    }
    return render(request, 'student/student_panel.html', context)

@login_required
def available_exams(request):
    if request.user.userprofile.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    now = timezone.now()
    exams = Exam.objects.filter(
        is_active=True,
        start_time__lte=now,
        end_time__gte=now
    ).exclude(
        examattempt__student=request.user
    )
    
    return render(request, 'student/available_exams.html', {'exams': exams})

@login_required
def take_exam(request, exam_id):
    if request.user.userprofile.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check if exam is available
    if not exam.is_available():
        messages.error(request, 'Exam is not available.')
        return redirect('available_exams')
    
    # Check if student has already attempted
    if ExamAttempt.objects.filter(student=request.user, exam=exam).exists():
        messages.error(request, 'You have already attempted this exam.')
        return redirect('available_exams')
    
    # Create exam attempt
    attempt = ExamAttempt.objects.create(student=request.user, exam=exam)
    
    # Get questions (shuffle if enabled)
    questions = list(exam.questions.all())
    if exam.shuffle_questions:
        random.shuffle(questions)
    
    context = {
        'exam': exam,
        'questions': questions,
        'attempt': attempt,
    }
    return render(request, 'student/take_exam.html', context)

@login_required
def submit_exam(request, exam_id):
    if request.method == 'POST':
        exam = get_object_or_404(Exam, id=exam_id)
        attempt = get_object_or_404(ExamAttempt, student=request.user, exam=exam, is_completed=False)
        
        total_score = 0
        
        for question in exam.questions.all():
            question_key = f'question_{question.id}'
            
            if question.question_type == 'mcq':
                selected_choice_id = request.POST.get(question_key)
                if selected_choice_id:
                    selected_choice = get_object_or_404(Choice, id=selected_choice_id)
                    is_correct = selected_choice.is_correct
                    marks_obtained = question.marks if is_correct else 0
                    total_score += marks_obtained
                    
                    StudentAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_choice=selected_choice,
                        marks_obtained=marks_obtained,
                        is_correct=is_correct
                    )
            else:  # descriptive
                descriptive_answer = request.POST.get(question_key, '')
                StudentAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    descriptive_answer=descriptive_answer,
                    marks_obtained=0  # To be evaluated manually
                )
        
        # Update attempt
        attempt.end_time = timezone.now()
        attempt.is_completed = True
        attempt.score = total_score
        attempt.save()
        
        messages.success(request, 'Exam submitted successfully!')
        return redirect('result_detail', attempt_id=attempt.id)
    
    return redirect('available_exams')

@login_required
def my_results(request):
    if request.user.userprofile.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    attempts = ExamAttempt.objects.filter(student=request.user, is_completed=True)
    
    # Calculate statistics
    total_exams = attempts.count()
    passed_exams = 0
    total_score = 0
    total_possible = 0
    highest_percentage = 0
    
    # Add percentage to each attempt
    attempts_with_stats = []
    for attempt in attempts:
        attempt_data = {
            'attempt': attempt,
            'percentage': 0
        }
        
        if attempt.score is not None:
            percentage = (attempt.score * 100) / attempt.exam.total_marks
            attempt_data['percentage'] = round(percentage, 1)
            
            total_score += attempt.score
            total_possible += attempt.exam.total_marks
            
            if percentage > highest_percentage:
                highest_percentage = percentage
                
            if attempt.score >= attempt.exam.passing_marks:
                passed_exams += 1
        
        attempts_with_stats.append(attempt_data)
    
    average_percentage = (total_score * 100 / total_possible) if total_possible > 0 else 0
    
    context = {
        'attempts_with_stats': attempts_with_stats,
        'total_exams': total_exams,
        'passed_exams': passed_exams,
        'average_percentage': round(average_percentage, 1),
        'highest_percentage': round(highest_percentage, 1),
    }
    return render(request, 'student/my_results.html', context)

@login_required
def result_detail(request, attempt_id):
    if request.user.userprofile.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=request.user)
    answers = attempt.student_answers.all()
    
    # Calculate percentage
    percentage = 0
    if attempt.score is not None:
        percentage = round((attempt.score * 100) / attempt.exam.total_marks, 1)
    
    # Calculate duration
    duration = None
    if attempt.end_time and attempt.start_time:
        duration_seconds = (attempt.end_time - attempt.start_time).total_seconds()
        duration_minutes = int(duration_seconds // 60)
        duration_seconds = int(duration_seconds % 60)
        duration = f"{duration_minutes}m {duration_seconds}s"
    
    context = {
        'attempt': attempt,
        'answers': answers,
        'percentage': percentage,
        'duration': duration,
    }
    return render(request, 'student/result_detail.html', context)
