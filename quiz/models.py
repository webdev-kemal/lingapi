from django.db import models
from lingauth.models import CustomUser  # Correct import path

# Create your models here.
class Quiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stars_count = models.IntegerField(("stars count"), default=0)
    collection_id = models.IntegerField(("collection id"), default=1)
    whoStarred = models.JSONField(default=list)
    title = models.CharField(("title"), max_length=255)
    quiz_words = models.CharField(("quiz words"), max_length=255, default="exalter")
    questions = models.JSONField(("questions"), default=list)
    language = models.CharField(("language"), max_length=50)
    isPublic = models.BooleanField(("is public"), default=True)
    isForked = models.BooleanField(("is forked"), default=False)
    isAImade = models.BooleanField(("is gpt"), default=False)
    whoForked = models.JSONField(default=list)
    isOfficial = models.BooleanField(("is official"), default=False)
    isMobile = models.BooleanField(("is mobile"), default=False)
    lastEdited = models.DateTimeField(("last edited"), auto_now_add=True)
    type = models.CharField(("type"), default="equivalent")
    description = models.CharField(("description"), default="my fancy quiz")

    socials = models.JSONField(default=list)
    comments = models.JSONField(default=list)
