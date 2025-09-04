from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.shortcuts import redirect
from . import views

router = DefaultRouter()
router.register(r'subjects', views.SubjectViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'quizzes', views.QuizViewSet)
router.register(r'progress', views.ProgressViewSet, basename='progress')

app_name = 'courses'

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Template URLs
    path('', views.CourseListView.as_view(), name='course-list'),
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('debug-language/', views.debug_language, name='debug-language'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:pk>/download/', views.CourseViewSet.as_view({'get': 'download_content'}), name='course-download'),
    path('courses/<int:pk>/enroll', views.CourseViewSet.as_view({'post': 'enroll'}), name='course-enroll'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course-create'),
    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject-detail'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/download/', views.LessonViewSet.as_view({'get': 'download'}), name='lesson-download'),
    path('lessons/<int:pk>/complete/', views.MarkLessonCompleteView.as_view(), name='mark-lesson-complete'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/<int:pk>/submit/', views.QuizSubmitView.as_view(), name='quiz-submit'),
    path('my-progress/', views.MyProgressView.as_view(), name='my-progress'),
    # Games
    path('games/', views.GamesListView.as_view(), name='games-list'),
    # Convenience redirect: /courses/admin -> /admin
    path('admin', lambda request: redirect('/admin/', permanent=False)),
    path('admin/', lambda request: redirect('/admin/', permanent=False)),
]
