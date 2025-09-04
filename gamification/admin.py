from django.contrib import admin
from .models import Badge, Achievement, UserBadge, PointsHistory, LearningStreak

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_required', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('points_required', 'created_at')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'badge', 'course', 'points')
    search_fields = ('name', 'description')
    list_filter = ('badge', 'course', 'points')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'earned_at')
    search_fields = ('user__username', 'badge__name')
    list_filter = ('badge', 'earned_at')
    date_hierarchy = 'earned_at'

@admin.register(PointsHistory)
class PointsHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'point_type', 'created_at')
    search_fields = ('user__username', 'description')
    list_filter = ('point_type', 'created_at')
    date_hierarchy = 'created_at'

@admin.register(LearningStreak)
class LearningStreakAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_streak', 'longest_streak', 'last_activity_date')
    search_fields = ('user__username',)
    list_filter = ('last_activity_date',)
    date_hierarchy = 'last_activity_date'
