from django.contrib import admin
from .models import UserProfile, Course, Exam, Question, Choice, ExamAttempt, StudentAnswer

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'teacher', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code']

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'exam', 'question_type', 'marks']
    list_filter = ['question_type', 'exam']
    inlines = [ChoiceInline]

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'duration_minutes', 'total_marks', 'start_time', 'is_active']
    list_filter = ['is_active', 'start_time', 'course']
    search_fields = ['title', 'course__name']
    inlines = [QuestionInline]

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'start_time', 'is_completed', 'score']
    list_filter = ['is_completed', 'start_time']
    search_fields = ['student__username', 'exam__title']

admin.site.register(Choice)
admin.site.register(StudentAnswer)
