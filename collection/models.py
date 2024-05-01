
from django.db import models
from lingauth.models import CustomUser  # Correct import path

class Collection(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stars_count = models.IntegerField(("stars count"), default=0)
    gradInt = models.IntegerField(("gradient id"), default=2)
    whoStarred = models.JSONField(default=list)
    title = models.CharField(("title"), max_length=255)
    emoji = models.CharField(("emoji"), max_length=5)
    words = models.JSONField(("words"), default=list)
    language = models.CharField(("language"), max_length=50)
    isPublic = models.BooleanField(("is public"), default=True)
    isDefault = models.BooleanField(("is default"), default=False)
    isForked = models.BooleanField(("is forked"), default=False)
    whoForked = models.JSONField(default=list)
    isOfficial = models.BooleanField(("is official"), default=False)
    isMobile = models.BooleanField(("is mobile"), default=False)
    lastEdited = models.DateTimeField(("last edited"), auto_now_add=True)
    type = models.CharField(("type"), default="dict")
    description = models.CharField(("description"), default="my fancy dictionary")
    socials = models.JSONField(default=list)
    comments = models.JSONField(default=list)


