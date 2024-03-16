# lingauth/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "username", "first_name", "last_name", "is_staff", "is_active", "is_premium", "locale")
    list_filter = ("email", "is_staff", "is_active", "is_premium", "locale")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("username", "first_name", "last_name", "locale", "pfp")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_premium",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "username", "password1", "password2", "first_name", "last_name", "locale", "pfp",
                "is_staff", "is_premium", "is_active",
            ),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)
