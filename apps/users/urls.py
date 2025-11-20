from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('login_modal/', views.login_view, name='login_modal'),
    path('register_modal/', views.register_view, name='register_modal'),
    path('logout/', views.logout_view, name='logout'),
]
