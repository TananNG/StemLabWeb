# Generated by Django 4.2.3 on 2023-12-28 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_student_classroom_student_classr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='classR',
            new_name='classRoom',
        ),
    ]