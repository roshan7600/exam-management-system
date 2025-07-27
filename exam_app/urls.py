from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin URLs
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-courses/', views.manage_courses, name='manage_courses'),
    path('add-course/', views.add_course, name='add_course'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
    
    # Teacher URLs
    path('teacher-panel/', views.teacher_panel, name='teacher_panel'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('create-exam/', views.create_exam, name='create_exam'),
    path('manage-exams/', views.manage_exams, name='manage_exams'),
    path('exam-details/<int:exam_id>/', views.exam_details, name='exam_details'),
    path('add-question/<int:exam_id>/', views.add_question, name='add_question'),
    path('edit-question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('exam-results/<int:exam_id>/', views.exam_results, name='exam_results'),
    
    # Student URLs
    path('student-panel/', views.student_panel, name='student_panel'),
    path('available-exams/', views.available_exams, name='available_exams'),
    path('take-exam/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('submit-exam/<int:exam_id>/', views.submit_exam, name='submit_exam'),
    path('my-results/', views.my_results, name='my_results'),
    path('result-detail/<int:attempt_id>/', views.result_detail, name='result_detail'),
]
