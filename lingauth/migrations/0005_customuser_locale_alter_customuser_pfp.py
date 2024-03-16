# Generated by Django 5.0 on 2024-01-19 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lingauth', '0004_customuser_pfp_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='locale',
            field=models.CharField(blank=True, max_length=10, verbose_name='locale'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='pfp',
            field=models.URLField(blank=True, null=True, verbose_name='profile picture'),
        ),
    ]
