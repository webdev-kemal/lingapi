# Generated by Django 5.0 on 2024-01-19 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lingauth', '0006_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='changedUsername',
            field=models.BooleanField(default=False, verbose_name='set username once'),
        ),
    ]
