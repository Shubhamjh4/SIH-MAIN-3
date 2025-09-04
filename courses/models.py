from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    grade_level = models.IntegerField(
        choices=[(i, f"Class {i}") for i in range(6, 13)],
        validators=[MinValueValidator(6), MaxValueValidator(12)],
    )
    language = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} - Class {self.grade_level}"

def course_thumbnail_path(instance, filename):
    return f'courses/{instance.subject.id}/{instance.id}/thumbnail/{filename}'

class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=20)
    points_available = models.IntegerField(default=0)
    is_offline_available = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to=course_thumbnail_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def class_label(self) -> str:
        return f"Class {self.subject.grade_level}"

def lesson_content_path(instance, filename):
    return f'courses/{instance.course.subject.id}/{instance.course.id}/lessons/{instance.id}/{filename}'

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField()
    estimated_time = models.IntegerField(help_text="Estimated time in minutes")
    points = models.IntegerField(default=0)
    video_url = models.URLField(blank=True, null=True)
    content_file = models.FileField(upload_to=lesson_content_path, null=True, blank=True)
    content_type = models.CharField(max_length=20, choices=[
        ('text', 'Text'),
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('audio', 'Audio'),
        ('interactive', 'Interactive')
    ], default='text')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    passing_score = models.IntegerField(default=70)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('user', 'lesson'), ('user', 'quiz')]


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'course')]

    def __str__(self):
        return f"{self.user.username} -> {self.course.title}"
