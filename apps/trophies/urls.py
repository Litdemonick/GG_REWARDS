from django.urls import path
from . import views

app_name = 'trophies'

urlpatterns = [
    path('games/', views.game_catalog, name='game_catalog'),
]