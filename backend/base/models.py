from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    EDUCATOR = 'Educator'
    STUDENT = 'Student'
    ADMINISTRATOR = 'Administrator'
    ROLE_CHOICES = [
        (EDUCATOR, 'Educator'),
        (STUDENT, 'Student'),
        (ADMINISTRATOR, 'Administrator'),
    ]
    role = models.CharField(max_length=13, choices=ROLE_CHOICES, default=STUDENT)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_courses')
    thumbnail_image = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    difficulty_level = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    additional_resources = models.TextField(blank=True, null=True)
    order = models.IntegerField()

    def __str__(self):
        return f"{self.module.title} - {self.title}"

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    introduction = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class UserQuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    score = models.IntegerField(default=0)
    date_attempted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - Attempt on {self.date_attempted.strftime('%Y-%m-%d')}"

class CourseProgress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress_records')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_progress')
    completion_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.completion_percentage}%"

class LessonProgress(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_progress')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {'Completed' if self.completed else 'Incomplete'}"

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title

class UserAssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignment_submissions')
    submitted_file = models.FileField(upload_to='assignments/')
    submission_date = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.assignment.title} - Submitted on {self.submission_date.strftime('%Y-%m-%d')}"

class CourseNotice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notices')
    title = models.CharField(max_length=255)
    message = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"
