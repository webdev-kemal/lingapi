# Generated by Django 5.0 on 2024-02-04 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lingauth', '0014_collection_ismobile_alter_collection_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='collections',
        ),
        migrations.DeleteModel(
            name='Collection',
        ),
    ]