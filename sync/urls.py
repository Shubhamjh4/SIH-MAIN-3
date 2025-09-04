from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sync', views.SyncViewSet, basename='sync')
router.register(r'versions', views.ContentVersionViewSet, basename='content-versions')

urlpatterns = [
    path('', include(router.urls)),
]
