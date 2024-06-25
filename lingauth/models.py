from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string
from django.utils.crypto import get_random_string
from .managers import CustomUserManager  # Update import path
from .defcollections import default_collections 
from django.utils import timezone

notifications = [{
                'notification_emoji': '⭐',
                'item_id': 0,
                'type': 'welcome',
                'item_name': 'Hoşgeldiniz!',
                'date': str(timezone.now())
            }]

current_day = timezone.now().strftime('%A')

default_week_data = [
            {"day":"Monday", "user_activity": False, "hasPassed": False, "isToday":  current_day == "Monday"},
            {"day":"Tuesday", "user_activity": False, "hasPassed": False, "isToday":  current_day == "Tuesday"},
            {"day":"Wednesday", "user_activity": False, "hasPassed": False, "isToday":  current_day == "Wednesday"},
            {"day":"Thursday", "user_activity": False, "hasPassed": False, "isToday":  current_day == "Thursday"},
            {"day":"Friday", "user_activity": False, "hasPassed": False, "isToday":  current_day == "Friday"},
            {"day":"Saturday", "user_activity": False, "hasPassed": False, "isToday":  current_day == "Saturday"},
            {"day":"Sunday", "user_activity": False, "hasPassed": False, "isToday":  current_day == "Sunday"}
        ]

class CustomUser(AbstractUser):

    username = models.CharField(("username"), max_length=26, unique=True, null=True, blank=True)
    email = models.EmailField(("email address"), unique=True, db_index=True)
    is_premium = models.BooleanField(("premium status"), default=False)
    changedUsername = models.BooleanField(("set username once"), default=False)

    pfp = models.URLField(("profile picture"), null=True, blank=True)
    first_name = models.CharField(("first name"), max_length=30, blank=True)
    last_name = models.CharField(("last name"), max_length=30, blank=True)
    locale = models.CharField(("locale"), max_length=10, blank=True, null=True)

    credits = models.IntegerField(default=30)
    quiz_data = models.JSONField(("quiz data"), default=list)
    # collections = models.ManyToManyField(Collection, related_name="users", blank=True)
    notifications = models.JSONField(("notifications data"), default=notifications)
    old_notifications = models.JSONField(("notifications data"), default=list)
    saved_items = models.JSONField(("saved items"), default=list)

    activity = models.JSONField(("activity"), default=list)
    streak = models.IntegerField(default=0)
    current_week_data = models.JSONField(("current_week"), default=default_week_data)

    lastRefillDate = models.DateTimeField(("last 30 refill"), auto_now_add=True, blank=True, null=True)
    lastPurchaseDate = models.DateTimeField(("last edited"), auto_now_add=False, blank=True, null=True)
    lastNicknameChange = models.DateTimeField(("last edited"), auto_now_add=False, blank=True, null=True)
    paymentMethods = models.JSONField(("card details"), default=list)
    studyPreference = models.IntegerField(default=1)
    studyProgress = models.JSONField(("official sets finished"), default=list)
    greenWall = models.JSONField(("github green wall"), default=list)



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