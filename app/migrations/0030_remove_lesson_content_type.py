# Generated by Django 4.2.3 on 2024-01-24 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_rename_image_lesson_content_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='content_type',
        ),
    ]