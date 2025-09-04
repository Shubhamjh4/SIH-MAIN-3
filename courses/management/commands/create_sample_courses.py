from django.core.management.base import BaseCommand
from courses.models import Subject, Course, Lesson


class Command(BaseCommand):
    help = 'Seed core subjects per class; for Classes 11-12 use PCM/PCB/PE/CS set.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset-11-12', action='store_true', default=True,
            help='Remove subjects for classes 11-12 that are not in the required set before seeding.'
        )

    def handle(self, *args, **kwargs):
        base_subjects_6_to_10 = ['English', 'Science', 'Mathematics']
        subjects_11_12 = ['Physics', 'Chemistry', 'Mathematics', 'Biology', 'Physical Education', 'Computer Science']
        
        # Language mappings
        languages = ['en', 'hi', 'or']
        language_names = {
            'en': 'English',
            'hi': 'हिन्दी', 
            'or': 'ଓଡ଼ିଆ'
        }
        
        # Subject translations
        subject_translations = {
            'en': {
                'English': 'English',
                'Science': 'Science', 
                'Mathematics': 'Mathematics',
                'Physics': 'Physics',
                'Chemistry': 'Chemistry',
                'Biology': 'Biology',
                'Physical Education': 'Physical Education',
                'Computer Science': 'Computer Science'
            },
            'hi': {
                'English': 'अंग्रेजी',
                'Science': 'विज्ञान',
                'Mathematics': 'गणित',
                'Physics': 'भौतिकी',
                'Chemistry': 'रसायन विज्ञान',
                'Biology': 'जीव विज्ञान',
                'Physical Education': 'शारीरिक शिक्षा',
                'Computer Science': 'कंप्यूटर विज्ञान'
            },
            'or': {
                'English': 'ଇଂରାଜୀ',
                'Science': 'ବିଜ୍ଞାନ',
                'Mathematics': 'ଗଣିତ',
                'Physics': 'ପଦାର୍ଥ ବିଜ୍ଞାନ',
                'Chemistry': 'ରସାୟନ ବିଜ୍ଞାନ',
                'Biology': 'ଜୀବ ବିଜ୍ଞାନ',
                'Physical Education': 'ଶାରୀରିକ ଶିକ୍ଷା',
                'Computer Science': 'କମ୍ପ୍ୟୁଟର ବିଜ୍ଞାନ'
            }
        }

        reset_11_12 = kwargs.get('reset_11_12', True)

        created_subjects = 0
        created_courses = 0
        removed_subjects = 0

        # Optionally remove any subjects that are not allowed for classes 11 and 12
        if reset_11_12:
            to_delete = Subject.objects.filter(grade_level__in=[11, 12]).exclude(name__in=subjects_11_12)
            removed_subjects = to_delete.count()
            to_delete.delete()

        for grade in range(6, 13):
            names = base_subjects_6_to_10 if grade <= 10 else subjects_11_12
            for name in names:
                for lang_code in languages:
                    translated_name = subject_translations[lang_code][name]
                    subject, s_created = Subject.objects.get_or_create(
                        name=translated_name,
                        grade_level=grade,
                        language=lang_code,
                        defaults={'description': f'{translated_name} for Class {grade}'}
                    )
                    created_subjects += 1 if s_created else 0

                    course, c_created = Course.objects.get_or_create(
                        subject=subject,
                        title=f"{translated_name} - Class {grade}",
                        defaults={
                            'description': f'Core {translated_name} curriculum for Class {grade}',
                            'difficulty_level': 'beginner',
                            'points_available': 100,
                            'is_offline_available': True,
                        }
                    )
                    created_courses += 1 if c_created else 0

                    Lesson.objects.get_or_create(
                        course=course,
                        order=1,
                        defaults={
                            'title': 'Introduction' if lang_code == 'en' else ('परिचय' if lang_code == 'hi' else 'ପରିଚୟ'),
                            'content': f'Welcome to {translated_name} for Class {grade}',
                            'estimated_time': 10,
                            'points': 10,
                        }
                    )

        self.stdout.write(self.style.SUCCESS(
            f'Seeding complete. New subjects: {created_subjects}, new courses: {created_courses}, removed 11-12 subjects: {removed_subjects}'
        ))
