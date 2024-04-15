# collection/admin.py
from django.contrib import admin
from .models import Quiz

class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "stars_count")
    search_fields = ("title", "owner__email")  # Search by title and owner's email


admin.site.register(Quiz, QuizAdmin)