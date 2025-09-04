from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Badge, Achievement, UserBadge, PointsHistory, LearningStreak
from django.contrib.auth.models import User
from .serializers import (
    BadgeSerializer, AchievementSerializer, UserBadgeSerializer,
    PointsHistorySerializer, LearningStreakSerializer
)

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserBadgeViewSet(viewsets.ModelViewSet):
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user)

class PointsHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = PointsHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PointsHistory.objects.filter(user=self.request.user)

    @action(detail=False)
    def total_points(self, request):
        total = self.get_queryset().aggregate(Sum('points'))['points__sum'] or 0
        return Response({'total_points': total})

    @action(detail=False)
    def points_by_type(self, request):
        points_by_type = self.get_queryset().values('point_type').annotate(
            total=Sum('points')
        )
        return Response(points_by_type)

    @action(detail=False, methods=['POST'])
    def track_game(self, request):
        # Expect { name: 'Physics Game', points: 5 }
        name = request.data.get('name') or 'Game Play'
        try:
            points = int(request.data.get('points', 1))
        except Exception:
            points = 1
        PointsHistory.objects.create(
            user=request.user,
            points=points,
            point_type='achievement',
            description=f"Played: {name}"
        )
        return Response({'ok': True, 'awarded': points})

    @action(detail=False, methods=['POST'])
    def track_finish(self, request):
        # Expect { name: 'Physics Game', score: 120, duration_ms: 45000 }
        name = (request.data.get('name') or 'Game').strip()
        try:
            score = max(0, int(request.data.get('score', 0)))
        except Exception:
            score = 0
        try:
            duration_ms = int(request.data.get('duration_ms', 0))
        except Exception:
            duration_ms = 0

        desc = f"GameFinish:{name}|score={score}|duration={duration_ms}ms"
        PointsHistory.objects.create(
            user=request.user,
            points=score,
            point_type='achievement',
            description=desc,
        )
        return Response({'ok': True, 'recorded': True, 'score': score})

class LearningStreakViewSet(viewsets.ModelViewSet):
    serializer_class = LearningStreakSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LearningStreak.objects.filter(user=self.request.user)
        
class LeaderboardView(LoginRequiredMixin, TemplateView):
    template_name = 'gamification/leaderboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add leaderboard data to context
        context['top_users'] = PointsHistory.objects.values('user__id', 'user__username').annotate(
            total_points=Sum('points')
        ).order_by('-total_points')[:10]
        # 7-day leaderboard
        week_ago = timezone.now() - timedelta(days=7)
        context['weekly_users'] = PointsHistory.objects.filter(
            created_at__gte=week_ago
        ).values('user__id', 'user__username').annotate(total_points=Sum('points')).order_by('-total_points')[:10]
        return context
        
class UserAchievementsView(LoginRequiredMixin, TemplateView):
    template_name = 'gamification/achievements.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add user's achievements data to context
        context['user_badges'] = UserBadge.objects.filter(user=self.request.user)
        context['total_points'] = PointsHistory.objects.filter(user=self.request.user).aggregate(
            total=Sum('points')
        )['total'] or 0
        return context
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LearningStreak.objects.filter(user=self.request.user)

    @action(detail=False, methods=['POST'])
    def check_in(self, request):
        streak, created = LearningStreak.objects.get_or_create(
            user=request.user,
            defaults={'last_activity_date': timezone.now().date()}
        )
        
        if not created:
            today = timezone.now().date()
            yesterday = today - timezone.timedelta(days=1)
            
            if streak.last_activity_date == yesterday:
                streak.current_streak += 1
                if streak.current_streak > streak.longest_streak:
                    streak.longest_streak = streak.current_streak
            elif streak.last_activity_date < yesterday:
                streak.current_streak = 1
            
            streak.last_activity_date = today
            streak.save()
        
        return Response({
            'current_streak': streak.current_streak,
            'longest_streak': streak.longest_streak
        })
