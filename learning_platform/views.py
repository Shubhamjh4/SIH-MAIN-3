from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from courses.models import Course, Subject
from gamification.models import Badge, Achievement, UserBadge, PointsHistory, LearningStreak
from django.db.models import Count, Sum
from django.utils import translation


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current language
        current_language = translation.get_language()
        if not current_language or current_language not in ['en', 'hi', 'or']:
            current_language = 'en'
        
        # Featured courses (popular learning paths)
        featured_courses = Course.objects.select_related('subject').filter(
            subject__language=current_language,
            subject__grade_level__gte=6,
            subject__grade_level__lte=12
        ).annotate(
            enrollment_count=Count('enrollment')
        ).order_by('-enrollment_count')[:6]
        
        context['featured_courses'] = featured_courses
        
        
        # Subject categories similar to the image
        subject_categories = [
            {
                'title': 'Mathematics',
                'icon': 'fas fa-calculator',
                'bg_color': 'bg-blue-600',
                'description': 'Master mathematical concepts and problem-solving skills'
            },
            {
                'title': 'Science',
                'icon': 'fas fa-atom',
                'bg_color': 'bg-green-500',
                'description': 'Explore physics, chemistry, and biology fundamentals'
            },
            {
                'title': 'Introduction to Coding',
                'icon': 'fas fa-code',
                'bg_color': 'bg-purple-600',
                'description': 'Learn programming basics and computational thinking'
            }
        ]
        
        context['subject_categories'] = subject_categories
        
        return context
