from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import json

class ContentVersion(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    version = models.PositiveIntegerField()
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('content_type', 'object_id', 'version')
        indexes = [
            models.Index(fields=['content_type', 'object_id', 'version'])
        ]

class SyncQueue(models.Model):
    SYNC_STATUS = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_version = models.ForeignKey(ContentVersion, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=SYNC_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['created_at']

class OfflineChange(models.Model):
    CHANGE_TYPE = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    synced = models.BooleanField(default=False)
    conflict_resolved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
