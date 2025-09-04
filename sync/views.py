from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.db import models
from .models import ContentVersion, SyncQueue, OfflineChange
from .serializers import (
    ContentVersionSerializer, SyncQueueSerializer, OfflineChangeSerializer
)
from .tasks import process_offline_changes, sync_user_content

class SyncViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['POST'])
    def sync_offline_changes(self, request):
        serializer = OfflineChangeSerializer(data=request.data, many=True)
        if serializer.is_valid():
            changes = serializer.save(user=request.user)
            process_offline_changes.delay(request.user.id)
            return Response({'message': 'Changes queued for processing'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST'])
    def request_sync(self, request):
        sync_user_content.delay(request.user.id)
        return Response({'message': 'Content sync initiated'})
    
    @action(detail=False, methods=['GET'])
    def sync_status(self, request):
        queue_items = SyncQueue.objects.filter(user=request.user)
        serializer = SyncQueueSerializer(queue_items, many=True)
        return Response(serializer.data)

class ContentVersionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ContentVersionSerializer
    
    def get_queryset(self):
        return ContentVersion.objects.filter(
            syncqueue__user=self.request.user,
            syncqueue__status='completed'
        ).distinct()
    
    @action(detail=False)
    def latest_versions(self, request):
        cache_key = f'latest_versions_{request.user.id}'
        result = cache.get(cache_key)
        
        if not result:
            versions = self.get_queryset().values(
                'content_type', 'object_id'
            ).annotate(latest_version=models.Max('version'))
            
            result = {
                f"{v['content_type']}_{v['object_id']}": v['latest_version']
                for v in versions
            }
            cache.set(cache_key, result, timeout=300)  # Cache for 5 minutes
        
        return Response(result)
