from django.db import models
from django.contrib.auth.models import User
from courses.models import Course, Lesson

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField()
    points_required = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    points = models.IntegerField()

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge']

class PointsHistory(models.Model):
    POINT_TYPES = (
        ('lesson', 'Lesson Completion'),
        ('quiz', 'Quiz Score'),
        ('achievement', 'Achievement Unlocked'),
        ('daily', 'Daily Login'),
        ('streak', 'Learning Streak')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    point_type = models.CharField(max_length=20, choices=POINT_TYPES)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.points} points - {self.point_type}"

class LearningStreak(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.current_streak} days"
