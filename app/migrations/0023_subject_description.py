# Generated by Django 4.2.3 on 2024-01-16 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_subject_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
