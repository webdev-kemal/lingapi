# Generated by Django 5.0 on 2024-04-26 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_quiz_collection_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='isAImade',
            field=models.BooleanField(default=False, verbose_name='is gpt'),
        ),
    ]
