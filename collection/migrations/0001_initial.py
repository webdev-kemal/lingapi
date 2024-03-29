# Generated by Django 5.0 on 2024-02-04 10:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('stars_count', models.IntegerField(default=0, verbose_name='stars count')),
                ('whoStarred', models.JSONField(default=list)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('emoji', models.CharField(max_length=5, verbose_name='emoji')),
                ('words', models.JSONField(default=list, verbose_name='words')),
                ('language', models.CharField(max_length=50, verbose_name='language')),
                ('isPublic', models.BooleanField(default=True, verbose_name='is public')),
                ('isDefault', models.BooleanField(default=False, verbose_name='is default')),
                ('isForked', models.BooleanField(default=False, verbose_name='is forked')),
                ('whoForked', models.JSONField(default=list)),
                ('isOfficial', models.BooleanField(default=False, verbose_name='is official')),
                ('isMobile', models.BooleanField(default=False, verbose_name='is mobile')),
                ('lastEdited', models.DateTimeField(auto_now_add=True, verbose_name='last edited')),
                ('type', models.CharField(default='dict', verbose_name='type')),
                ('description', models.CharField(default='my fancy dictionary', verbose_name='description')),
                ('socials', models.JSONField(default=list)),
                ('comments', models.JSONField(default=list)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
