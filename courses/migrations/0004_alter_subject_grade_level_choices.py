# Generated manually: alter Subject.grade_level to restrict to 6-12 with choices
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_progress_unique_together_progress_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='grade_level',
            field=models.IntegerField(choices=[(i, f"Class {i}") for i in range(6, 13)]),
        ),
    ]


