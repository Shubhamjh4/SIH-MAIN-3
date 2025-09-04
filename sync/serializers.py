from rest_framework import serializers
from .models import ContentVersion, SyncQueue, OfflineChange

class ContentVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentVersion
        fields = ('id', 'content_type', 'object_id', 'version', 'data', 'created_at')

class SyncQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyncQueue
        fields = ('id', 'user', 'content_version', 'status', 'created_at', 
                 'updated_at', 'error_message')

class OfflineChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineChange
        fields = ('id', 'user', 'content_type', 'object_id', 'change_type', 
                 'data', 'created_at', 'synced', 'conflict_resolved')
