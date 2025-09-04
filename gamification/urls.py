from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'badges', views.BadgeViewSet)
router.register(r'achievements', views.AchievementViewSet)
router.register(r'user-badges', views.UserBadgeViewSet, basename='user-badges')
router.register(r'points-history', views.PointsHistoryViewSet, basename='points-history')
router.register(r'learning-streaks', views.LearningStreakViewSet, basename='learning-streaks')

app_name = 'gamification'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Template views
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('achievements/', views.UserAchievementsView.as_view(), name='achievements'),
]
