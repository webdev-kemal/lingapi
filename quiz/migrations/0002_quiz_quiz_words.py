# Generated by Django 5.0 on 2024-04-09 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='quiz_words',
            field=models.CharField(default='exalter', max_length=255, verbose_name='quiz words'),
        ),
    ]
