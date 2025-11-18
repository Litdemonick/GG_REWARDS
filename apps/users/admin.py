from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'total_points', 'experience']
    search_fields = ['user__username', 'user__email']
    list_filter = ['level', 'created_at']
