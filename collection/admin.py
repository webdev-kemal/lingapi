# collection/admin.py
from django.contrib import admin
from .models import Collection

class CollectionAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "stars_count", "isPublic", "lastEdited", "isOfficial")
    search_fields = ("title", "owner__email")  # Search by title and owner's email
    list_filter = ("isPublic",)

admin.site.register(Collection, CollectionAdmin)
