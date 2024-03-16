# Generated by Django 5.0 on 2024-01-19 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lingauth', '0002_customuser_is_premium'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='email address'),
        ),
    ]