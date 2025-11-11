# blog/admin.py
from django.contrib import admin
from .models import Post, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "is_published", "view_count", "created_at"]
    list_filter = ["is_published", "created_at", "tags"]
    search_fields = ["title", "content"]
    filter_horizontal = ["tags", "likes"]
    readonly_fields = ["view_count", "created_at", "updated_at"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "post", "content", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["content", "author__username"]
