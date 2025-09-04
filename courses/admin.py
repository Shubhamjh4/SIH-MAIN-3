from django.contrib import admin
from .models import Subject, Course, Lesson, Quiz, Question, Choice, Progress, Enrollment

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'quiz', 'points')
    list_filter = ('quiz',)
    search_fields = ('question_text',)

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'lesson', 'passing_score', 'points')
    list_filter = ('lesson__course',)
    search_fields = ('title', 'description')

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'estimated_time', 'points')
    list_filter = ('course',)
    search_fields = ('title', 'content')
    ordering = ('course', 'order')

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('title', 'class_display', 'subject', 'difficulty_level', 'points_available', 'is_offline_available')
    list_filter = ('subject__grade_level', 'subject', 'difficulty_level', 'is_offline_available')
    search_fields = ('title', 'description')

    def class_display(self, obj):
        return f"Class {obj.subject.grade_level}"
    class_display.short_description = 'Class'

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade_level', 'language')
    list_filter = ('grade_level', 'language')
    search_fields = ('name', 'description')

class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'score', 'last_accessed')
    list_filter = ('completed', 'lesson__course')
    search_fields = ('user__username', 'lesson__title')
    date_hierarchy = 'last_accessed'

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('course', 'user')
    search_fields = ('user__username', 'course__title')

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
