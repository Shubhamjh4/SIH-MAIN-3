from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from io import BytesIO
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from .models import Subject, Course, Lesson, Quiz, Question, Choice, Progress, Enrollment
from django.conf import settings
import os
from .serializers import (
    SubjectSerializer, CourseSerializer, LessonSerializer,
    QuizSerializer, QuestionSerializer, ChoiceSerializer, ProgressSerializer
)

# --- Progress helpers ---
def recompute_course_progress(user, course: Course) -> None:
    total_lessons = course.lesson_set.count()
    completed_lessons = Progress.objects.filter(
        user=user,
        course=course,
        lesson__isnull=False,
        completed=True,
    ).count()
    percentage = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0

    course_prog = (
        Progress.objects.filter(user=user, course=course, lesson__isnull=True, quiz__isnull=True)
        .order_by('id')
        .first()
    )
    if not course_prog:
        course_prog = Progress(user=user, course=course, completed=False)
    course_prog.percentage = percentage
    course_prog.completed = (percentage == 100)
    # Sum points from completed lessons
    course_prog.points = Progress.objects.filter(
        user=user,
        course=course,
        lesson__isnull=False,
        completed=True,
    ).aggregate(total=models.Sum('points'))['total'] or 0
    course_prog.save()

def get_or_create_unique_lesson_progress(user, lesson: Lesson) -> Progress:
    existing = (
        Progress.objects.filter(user=user, lesson=lesson)
        .order_by('id')
        .first()
    )
    if existing:
        return existing
    return Progress.objects.create(user=user, lesson=lesson, course=lesson.course)

# Template Views
def debug_language(request):
    from django.utils import translation
    current_lang = translation.get_language()
    from courses.models import Course
    courses_count = Course.objects.filter(subject__language=current_lang).count()
    return JsonResponse({
        'current_language': current_lang,
        'courses_count': courses_count,
        'available_languages': ['en', 'hi', 'or']
    })

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        from django.utils import translation
        
        queryset = (
            Course.objects.select_related('subject')
            .annotate(
                lessons_count=models.Count('lesson', distinct=True),
                quizzes_count=models.Count('lesson__quiz', distinct=True),
            )
        )
        # Restrict to classes 6-12
        queryset = queryset.filter(subject__grade_level__gte=6, subject__grade_level__lte=12)
        
        # Filter by current language - with fallback to English
        current_language = translation.get_language()
        if not current_language or current_language not in ['en', 'hi', 'or']:
            current_language = 'en'
        
        queryset = queryset.filter(subject__language=current_language)

        # Optional grade filter via query param e.g. ?grade=8
        grade = self.request.GET.get('grade')
        if grade and grade.isdigit():
            grade_int = int(grade)
            if 6 <= grade_int <= 12:
                queryset = queryset.filter(subject__grade_level=grade_int)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                models.Q(title__icontains=search_query) |
                models.Q(description__icontains=search_query) |
                models.Q(subject__name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grades'] = list(range(6, 13))
        selected = self.request.GET.get('grade')
        context['selected_grade'] = int(selected) if selected and selected.isdigit() else None
        # Provide subjects for the selected class
        if context['selected_grade']:
            context['subjects_for_selected_grade'] = Subject.objects.filter(
                grade_level=context['selected_grade']
            ).order_by('name')
        else:
            context['subjects_for_selected_grade'] = Subject.objects.none()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grades'] = list(range(6, 13))
        selected = self.request.GET.get('grade')
        context['selected_grade'] = int(selected) if selected and selected.isdigit() else None
        return context

class SubjectListView(ListView):
    model = Subject
    template_name = 'courses/subject_list.html'
    context_object_name = 'subjects'

class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'courses/subject_detail.html'
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = self.object.course_set.all()
        return context

class MyProgressView(LoginRequiredMixin, ListView):
    model = Progress
    template_name = 'courses/my_progress.html'
    context_object_name = 'progress_items'

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Ensure every enrollment has a unique course-level Progress row
        for enroll in Enrollment.objects.filter(user=user).select_related('course'):
            course_prog = (
                Progress.objects.filter(user=user, course=enroll.course, lesson__isnull=True, quiz__isnull=True)
                .order_by('id')
                .first()
            )
            if not course_prog:
                Progress.objects.create(user=user, course=enroll.course, completed=False)

        # Build course-level progress entries
        course_progress_entries = []
        course_progress_qs = (
            Progress.objects.filter(user=user, course__isnull=False, lesson__isnull=True, quiz__isnull=True)
            .select_related('course', 'course__subject')
        )
        for p in course_progress_qs:
            course = p.course
            total_lessons = course.lesson_set.count()
            completed_lessons = Progress.objects.filter(user=user, course=course, lesson__isnull=False, completed=True).count()
            total_quizzes = Quiz.objects.filter(lesson__course=course).count()
            completed_quizzes = Progress.objects.filter(user=user, course=course, quiz__isnull=False, completed=True).count()
            course_progress_entries.append({
                'course': course,
                'percentage': p.percentage,
                'points': p.points,
                'completed': p.completed,
                'completed_lessons_count': completed_lessons,
                'total_lessons_count': total_lessons,
                'completed_quizzes_count': completed_quizzes,
                'total_quizzes_count': total_quizzes,
            })

        context['course_progress'] = course_progress_entries
        # Stats expected by template
        context['completed_count'] = sum(1 for e in course_progress_entries if e['percentage'] == 100)
        context['total_points'] = sum(e['points'] for e in course_progress_entries)
        context['quizzes_passed'] = sum(1 for e in course_progress_entries if e['completed_quizzes_count'] > 0)
        # Count any enrolled course not yet completed as in progress (including 0%)
        context['in_progress_count'] = sum(1 for e in course_progress_entries if e['percentage'] < 100)
        return context

# API Views
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def offline_content(self, request, pk=None):
        subject = self.get_object()
        courses = subject.course_set.filter(is_offline_available=True)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = self.object.lesson_set.all().order_by('order')
        context['quizzes'] = Quiz.objects.filter(lesson__course=self.object)
        if self.request.user.is_authenticated:
            # Ensure course-level progress is up-to-date for this view
            recompute_course_progress(self.request.user, self.object)
            context['progress'] = Progress.objects.filter(
                user=self.request.user,
                course=self.object,
                lesson__isnull=True,
                quiz__isnull=True,
            ).first()
            context['completed_lesson_ids'] = list(
                Progress.objects.filter(
                    user=self.request.user,
                    course=self.object,
                    lesson__isnull=False,
                    completed=True,
                ).values_list('lesson_id', flat=True)
            )
            context['completed_quiz_ids'] = list(
                Progress.objects.filter(
                    user=self.request.user,
                    course=self.object,
                    quiz__isnull=False,
                    completed=True,
                ).values_list('quiz_id', flat=True)
            )
            context['is_enrolled'] = Enrollment.objects.filter(user=self.request.user, course=self.object).exists()
        return context

@method_decorator(login_required, name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    template_name = 'courses/course_form.html'
    fields = ['title', 'description', 'subject', 'difficulty_level', 'points_available', 'is_offline_available', 'thumbnail']
    success_url = reverse_lazy('courses:course-list')
    
    def get_context_data(self, **kwargs):
        from django.utils import translation
        
        context = super().get_context_data(**kwargs)
        current_language = translation.get_language()
        context['subjects'] = Subject.objects.filter(language=current_language).order_by('name')
        context['courses'] = Course.objects.filter(subject__language=current_language).order_by('title')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Course created successfully!')
        return super().form_valid(form)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Course.objects.select_related('subject').filter(
            subject__grade_level__gte=6,
            subject__grade_level__lte=12,
        )
        grade = self.request.query_params.get('grade') if hasattr(self, 'request') else None
        if grade and grade.isdigit():
            grade_int = int(grade)
            if 6 <= grade_int <= 12:
                queryset = queryset.filter(subject__grade_level=grade_int)
        return queryset

    @action(detail=True)
    def download_content(self, request, pk=None):
        course = self.get_object()
        if not course.is_offline_available:
            return Response(
                {'error': 'This course is not available for offline access'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import cm
        except Exception:
            return Response(
                {
                    'error': 'PDF generator not available. Please install reportlab.',
                    'fix': 'pip install reportlab'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 2 * cm
        p.setFont("Helvetica-Bold", 16)
        p.drawString(2 * cm, y, f"{course.title}")
        y -= 0.8 * cm
        p.setFont("Helvetica", 11)
        p.drawString(2 * cm, y, f"Class: {course.subject.grade_level} | Subject: {course.subject.name}")
        y -= 0.6 * cm
        p.drawString(2 * cm, y, f"Difficulty: {course.difficulty_level} | Points: {course.points_available}")
        y -= 1.0 * cm

        # Description block
        p.setFont("Helvetica-Bold", 12)
        p.drawString(2 * cm, y, "Description")
        y -= 0.6 * cm
        p.setFont("Helvetica", 11)
        desc = course.description or ""
        # simple wrap
        max_chars = 95
        for i in range(0, len(desc), max_chars):
            line = desc[i:i + max_chars]
            if y < 3 * cm:
                p.showPage(); y = height - 2 * cm; p.setFont("Helvetica", 11)
            p.drawString(2 * cm, y, line)
            y -= 0.5 * cm

        # Lessons
        y -= 0.5 * cm
        p.setFont("Helvetica-Bold", 12)
        if y < 3 * cm:
            p.showPage(); y = height - 2 * cm
        p.drawString(2 * cm, y, "Lessons")
        y -= 0.6 * cm
        p.setFont("Helvetica", 11)
        lessons = course.lesson_set.all().order_by('order')
        if not lessons:
            p.drawString(2 * cm, y, "No lessons available.")
            y -= 0.5 * cm
        else:
            for lesson in lessons:
                line = f"{lesson.order or 0}. {lesson.title} (Points: {lesson.points}, Est: {lesson.estimated_time} min)"
                if y < 3 * cm:
                    p.showPage(); y = height - 2 * cm; p.setFont("Helvetica", 11)
                p.drawString(2 * cm, y, line)
                y -= 0.5 * cm
        
        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        filename = f"{course.title.replace(' ', '_')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    @action(detail=True, methods=['POST'])
    def enroll(self, request, pk=None):
        course = self.get_object()
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        # Ensure progress object exists for course level visibility
        Progress.objects.get_or_create(user=request.user, course=course, defaults={'completed': False})
        return Response({'enrolled': True, 'created': created})

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'courses/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            progress = get_or_create_unique_lesson_progress(self.request.user, self.object)
            context['progress'] = progress
        
        # Add file extension information for template
        if self.object.content_file:
            file_url = str(self.object.content_file.url).lower()
            context['is_pdf'] = file_url.endswith('.pdf')
            context['is_video'] = file_url.endswith('.mp4') or file_url.endswith('.avi') or file_url.endswith('.mov')
        else:
            context['is_pdf'] = False
            context['is_video'] = False
            
        return context

    @action(detail=True)
    def download_pdf(self, request, pk=None):
        # This method will not be used here; see LessonViewSet for API download
        pass

class MarkLessonCompleteView(LoginRequiredMixin, DetailView):
    model = Lesson

    def post(self, request, *args, **kwargs):
        lesson = self.get_object()
        # Be tolerant of accidental duplicates by selecting first if multiple exist
        progress = get_or_create_unique_lesson_progress(request.user, lesson)
        progress.completed = True
        # Award lesson points when completed
        progress.points = lesson.points
        progress.save()
        # Recompute the parent course progress
        recompute_course_progress(request.user, lesson.course)
        
        messages.success(request, 'Lesson marked as complete!')
        return redirect('courses:course-detail', pk=lesson.course.pk)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def download(self, request, pk=None):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import cm
        except Exception:
            return Response({'error': 'reportlab not installed'}, status=500)

        lesson = self.get_object()
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 2 * cm
        p.setFont("Helvetica-Bold", 16)
        p.drawString(2 * cm, y, lesson.title)
        y -= 0.8 * cm
        p.setFont("Helvetica", 11)
        p.drawString(2 * cm, y, f"Course: {lesson.course.title}")
        y -= 0.6 * cm
        p.drawString(2 * cm, y, f"Class: {lesson.course.subject.grade_level} | Subject: {lesson.course.subject.name}")
        y -= 1.0 * cm

        p.setFont("Helvetica-Bold", 12)
        p.drawString(2 * cm, y, "Content")
        y -= 0.6 * cm
        p.setFont("Helvetica", 11)
        text = lesson.content or ""
        text = str(text)
        max_chars = 95
        for i in range(0, len(text), max_chars):
            line = text[i:i + max_chars]
            if y < 3 * cm:
                p.showPage(); y = height - 2 * cm; p.setFont("Helvetica", 11)
            p.drawString(2 * cm, y, line)
            y -= 0.5 * cm

        p.showPage(); p.save(); buffer.seek(0)
        resp = HttpResponse(buffer.read(), content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="{lesson.title.replace(" ", "_")}.pdf"'
        return resp

class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'courses/quiz_detail.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['progress'] = Progress.objects.filter(
                user=self.request.user,
                quiz=self.object
            ).first()
        return context

class QuizSubmitView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'courses/quiz_submit.html'
    context_object_name = 'quiz'

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        answers = request.POST
        score = 0
        total_points = 0
        
        for question in quiz.question_set.all():
            total_points += question.points
            answer_key = f'question_{question.id}'
            if answer_key in answers:
                selected_choice = question.choice_set.filter(
                    id=answers[answer_key]
                ).first()
                if selected_choice and selected_choice.is_correct:
                    score += question.points
        
        percentage = (score / total_points) * 100 if total_points > 0 else 0
        passed = percentage >= quiz.passing_score

        Progress.objects.update_or_create(
            user=request.user,
            quiz=quiz,
            course=quiz.course,
            defaults={
                'score': score,
                'completed': True
            }
        )

        # Recompute the parent course progress (in case quizzes count towards completion later)
        recompute_course_progress(request.user, quiz.course)

        messages.success(request, f'Quiz submitted! Score: {percentage:.1f}%')
        return redirect('courses:course-detail', pk=quiz.course.pk)

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['POST'])
    def submit(self, request, pk=None):
        quiz = self.get_object()
        answers = request.data.get('answers', {})
        score = 0
        total_points = 0
        
        for question in quiz.question_set.all():
            total_points += question.points
            if str(question.id) in answers:
                selected_choice = question.choice_set.filter(
                    id=answers[str(question.id)]
                ).first()
                if selected_choice and selected_choice.is_correct:
                    score += question.points
        
        percentage = (score / total_points) * 100 if total_points > 0 else 0
        passed = percentage >= quiz.passing_score
        
        return Response({
            'score': score,
            'total_points': total_points,
            'percentage': percentage,
            'passed': passed
        })

class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)

    @action(detail=False)
    def my_progress(self, request):
        progress = self.get_queryset()
        serializer = self.get_serializer(progress, many=True)
        return Response(serializer.data)


# Games (static) listing view
class GamesListView(ListView):
    template_name = 'games/list.html'
    context_object_name = 'games'

    def get_queryset(self):
        base_static = getattr(settings, 'BASE_DIR', None)
        if not base_static:
            return []
        games_dir = os.path.join(base_static, 'static', 'games')
        games = []
        if os.path.isdir(games_dir):
            import re
            def extract_title(file_path: str) -> str:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(4096)
                        m = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
                        if m:
                            return re.sub(r"\s+", " ", m.group(1)).strip()
                except Exception:
                    pass
                # Fallback to filename if no title
                base = os.path.basename(file_path)
                name, _ = os.path.splitext(base)
                return name.replace('-', ' ').replace('_', ' ').title()

            for entry in os.listdir(games_dir):
                game_path = os.path.join(games_dir, entry)
                # Case 1: Directory with index.html
                index_path = os.path.join(game_path, 'index.html')
                if os.path.isdir(game_path) and os.path.isfile(index_path):
                    display_name = extract_title(index_path)
                    games.append({
                        'slug': entry,
                        'name': display_name,
                        'url': f"{settings.STATIC_URL}games/{entry}/index.html",
                    })
                # Case 2: Standalone HTML file inside static/games
                elif os.path.isfile(game_path) and entry.lower().endswith('.html'):
                    name = os.path.splitext(entry)[0]
                    display_name = extract_title(game_path)
                    games.append({
                        'slug': name,
                        'name': display_name,
                        'url': f"{settings.STATIC_URL}games/{entry}",
                    })
        return games
