from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string
from django.utils.crypto import get_random_string
from .managers import CustomUserManager  # Update import path
from .defcollections import default_collections 



class CustomUser(AbstractUser):

    username = models.CharField(("username"), max_length=26, unique=True, null=True, blank=True)
    email = models.EmailField(("email address"), unique=True, db_index=True)
    is_premium = models.BooleanField(("premium status"), default=False)
    changedUsername = models.BooleanField(("set username once"), default=False)

    pfp = models.URLField(("profile picture"), null=True, blank=True)
    first_name = models.CharField(("first name"), max_length=30, blank=True)
    last_name = models.CharField(("last name"), max_length=30, blank=True)
    locale = models.CharField(("locale"), max_length=10, blank=True)

    credits = models.IntegerField(default=30)
    # collections = models.ManyToManyField(Collection, related_name="users", blank=True)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            random_number = ''.join(random.choices(string.digits, k=7))
            self.username = random_number

        super().save(*args, **kwargs)


    def __str__(self):
        return self.email
    
    def get_collection_count(self):
        return self.collection_set.count()
    
    def deduct_credits(self, amount):
        if self.credits >= amount:
            self.credits -= amount
            self.save()
            return True
        return False
    
    def add_credits(self, amount):
        self.credits += amount
        self.save()
        return True



        # if not self.collections.exists():
        #     for collection_data in default_collections:
        #         collection_data['owner'] = self
        #         collection = Collection.objects.create(**collection_data)
        #         self.collections.add(collection)
    # from collection.models import Collection
# collections = models.ForeignKey('collection.Collection')