from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('login_modal/', views.login_view, name='login_modal'),
    path('login/', views.login_view, name='login'),
    path('register_modal/', views.register_view, name='register_modal'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('steam/login/', views.steam_login, name='steam_login'),
    path('steam/callback/', views.steam_callback, name='steam_callback'),
    path('steam/unlink/', views.unlink_steam, name='unlink_steam'),
    path('steam/link/', views.link_steam, name='link_steam'),
    path('steam/sync/', views.sync_steam, name='sync_steam'),
    path('rankings/', views.rankings_view, name='rankings'),
    path('u/<str:username>/', views.public_profile_view, name='public_profile'), # Perfil público
    path('steam/game/<str:app_id>/achievements/', views.game_achievements, name='game_achievements'),
]
