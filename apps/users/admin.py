from django.contrib import admin

from apps.users.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("user__email", "user__username")
