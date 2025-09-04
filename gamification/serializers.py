from rest_framework import serializers
from .models import Badge, Achievement, UserBadge, PointsHistory, LearningStreak

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'name', 'description', 'image_url', 'points_required', 'created_at')

class AchievementSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = Achievement
        fields = ('id', 'name', 'description', 'badge', 'course', 'points')

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = UserBadge
        fields = ('id', 'user', 'badge', 'earned_at')

class PointsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsHistory
        fields = ('id', 'user', 'points', 'point_type', 'description', 'created_at')

class LearningStreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningStreak
        fields = ('id', 'user', 'current_streak', 'longest_streak', 'last_activity_date')
