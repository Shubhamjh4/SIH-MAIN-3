from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default='student')
    preferred_language = models.CharField(max_length=10, default='english')
    grade_level = models.IntegerField(null=True, blank=True)
    school_name = models.CharField(max_length=200, blank=True)
    village = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    offline_access_enabled = models.BooleanField(default=True)
    last_sync_date = models.DateTimeField(auto_now=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    verification_token_created = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
