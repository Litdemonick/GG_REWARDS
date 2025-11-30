from django.contrib import admin
from .models import Platform, Game, Trophy, UserTrophy

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name']



@admin.register(Trophy)
class TrophyAdmin(admin.ModelAdmin):
    list_display = ['name', 'game', 'rarity', 'points']
    list_filter = ['rarity']
    search_fields = ['name', 'game__title']

@admin.register(UserTrophy)
class UserTrophyAdmin(admin.ModelAdmin):
    list_display = ['user', 'trophy', 'unlocked_at']
    list_filter = ['unlocked_at']
    search_fields = ['user__username', 'trophy__name']
