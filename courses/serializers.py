from rest_framework import serializers
from .models import Subject, Course, Lesson, Quiz, Question, Choice, Progress

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice_text', 'is_correct')

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, source='choice_set')
    
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'points', 'choices')

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, source='question_set')
    
    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description', 'passing_score', 'points', 'questions')

class LessonSerializer(serializers.ModelSerializer):
    quiz_set = QuizSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'content', 'order', 'estimated_time', 'points', 'quiz_set')

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    
    class Meta:
        model = Course
        fields = ('id', 'subject', 'title', 'description', 'difficulty_level', 
                 'points_available', 'is_offline_available', 'created_at', 
                 'updated_at', 'lessons')

class SubjectSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True, source='course_set')
    
    class Meta:
        model = Subject
        fields = ('id', 'name', 'description', 'grade_level', 'language', 'courses')

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ('id', 'user', 'lesson', 'completed', 'score', 'last_accessed')
