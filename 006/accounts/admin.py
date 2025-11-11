# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "nickname", "is_staff", "date_joined"]
    fieldsets = UserAdmin.fieldsets + (
        ("추가 정보", {"fields": ("nickname", "profile_image", "bio")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("추가 정보", {"fields": ("nickname", "profile_image", "bio")}),
    )
