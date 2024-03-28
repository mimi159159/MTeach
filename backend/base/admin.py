from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import (CustomUser, Course, Module, Lesson, Quiz, Question, 
                     Answer, UserQuizAttempt, CourseProgress, LessonProgress, 
                     Assignment, UserAssignmentSubmission, CourseNotice)

# Custom forms for CustomUser
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'profile_picture')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'profile_picture')

# CustomUserAdmin with additional fields
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'profile_picture')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')



class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'creation_date', 'last_updated', 'difficulty_level')
    search_fields = ('title', 'description', 'creator__username')
    list_filter = ('creation_date', 'difficulty_level', 'creator')

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')
    search_fields = ('title', 'module__title')
    list_filter = ('module',)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson')
    search_fields = ('title', 'lesson__title')
    list_filter = ('lesson',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text', 'quiz__title')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text', 'question__text')
    list_filter = ('is_correct',)

class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'score', 'date_attempted')
    search_fields = ('quiz__title', 'user__username')
    list_filter = ('date_attempted',)

class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'completion_percentage')
    search_fields = ('course__title', 'user__username')
    list_filter = ('course',)

class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'completed')
    search_fields = ('lesson__title', 'user__username')
    list_filter = ('completed',)

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date')
    search_fields = ('title', 'course__title')
    list_filter = ('due_date',)

class UserAssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'user', 'submission_date', 'grade')
    search_fields = ('assignment__title', 'user__username')
    list_filter = ('submission_date',)

class CourseNoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'posted_at')
    search_fields = ('title', 'course__title')
    list_filter = ('posted_at',)



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserQuizAttempt, UserQuizAttemptAdmin)
admin.site.register(CourseProgress, CourseProgressAdmin)
admin.site.register(LessonProgress, LessonProgressAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(UserAssignmentSubmission, UserAssignmentSubmissionAdmin)
admin.site.register(CourseNotice, CourseNoticeAdmin)