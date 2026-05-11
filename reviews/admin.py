from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["title", "media_type", "rating", "user", "author", "year", "created_at"]
    list_filter = ["media_type", "user"]
    search_fields = ["title", "author"]
    ordering = ["-created_at"]