# Generated by Django 4.2.3 on 2023-12-29 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_subject_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='rate',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='slot',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]