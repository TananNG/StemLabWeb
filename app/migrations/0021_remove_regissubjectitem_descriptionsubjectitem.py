# Generated by Django 4.2.3 on 2024-01-06 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_regissubjectitem_descriptionsubjectitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regissubjectitem',
            name='descriptionSubjectItem',
        ),
    ]