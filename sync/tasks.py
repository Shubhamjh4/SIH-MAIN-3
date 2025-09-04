from celery import shared_task
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .models import ContentVersion, SyncQueue, OfflineChange
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_offline_changes(user_id):
    """Process offline changes for a user."""
    changes = OfflineChange.objects.filter(
        user_id=user_id,
        synced=False,
        conflict_resolved=False
    ).select_related('content_type')
    
    for change in changes:
        try:
            with transaction.atomic():
                model_class = change.content_type.model_class()
                
                if change.change_type == 'create':
                    instance = model_class.objects.create(**change.data)
                    create_content_version(instance)
                
                elif change.change_type == 'update':
                    instance = model_class.objects.get(id=change.object_id)
                    for key, value in change.data.items():
                        setattr(instance, key, value)
                    instance.save()
                    create_content_version(instance)
                
                elif change.change_type == 'delete':
                    model_class.objects.filter(id=change.object_id).delete()
                
                change.synced = True
                change.save()
                
                # Invalidate cache
                cache_key = f"{change.content_type.model}_{change.object_id}"
                cache.delete(cache_key)
        
        except Exception as e:
            logger.error(f"Error processing change {change.id}: {str(e)}")
            change.error_message = str(e)
            change.save()

@shared_task
def create_content_version(instance):
    """Create a new version for a content object."""
    content_type = ContentType.objects.get_for_model(instance)
    current_version = ContentVersion.objects.filter(
        content_type=content_type,
        object_id=instance.id
    ).count()
    
    # Create new version
    ContentVersion.objects.create(
        content_type=content_type,
        object_id=instance.id,
        version=current_version + 1,
        data=instance.to_dict() if hasattr(instance, 'to_dict') else {}
    )

@shared_task
def sync_user_content(user_id):
    """Sync content for a specific user."""
    from courses.models import Course, Lesson
    from gamification.models import Badge, Achievement
    
    # Models to sync
    models_to_sync = [Course, Lesson, Badge, Achievement]
    
    for model in models_to_sync:
        content_type = ContentType.objects.get_for_model(model)
        latest_versions = ContentVersion.objects.filter(
            content_type=content_type
        ).values('object_id').annotate(
            latest_version=models.Max('version')
        )
        
        for version_info in latest_versions:
            SyncQueue.objects.get_or_create(
                user_id=user_id,
                content_version=ContentVersion.objects.get(
                    content_type=content_type,
                    object_id=version_info['object_id'],
                    version=version_info['latest_version']
                )
            )
