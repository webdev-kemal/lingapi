# Generated by Django 5.0 on 2024-01-20 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lingauth', '0010_alter_collection_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='isForked',
            field=models.BooleanField(default=False, verbose_name='is forked'),
        ),
    ]
