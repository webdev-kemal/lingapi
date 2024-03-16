from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from lingauth.models import CustomUser  # Import your CustomUser model
from .models import Collection
from .defcollections import default_collections 

@receiver(post_save, sender=CustomUser)
def create_default_collections(sender, instance, created, **kwargs):
    if created:
        # Collection = apps.get_model('collection', 'Collection')  # Use apps.get_model to get the Collection model dynamically
        for collection_data in default_collections:
            Collection.objects.create(owner=instance, **collection_data)
