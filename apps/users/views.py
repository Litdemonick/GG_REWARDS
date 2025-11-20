from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Importamos el modelo Profile que crearemos
from .models import Profile
from apps.games.models import Game

def home(request):
    '''Página de inicio'''
    context = {
        'title': 'GG Rewards - Inicio',
        'games': Game.objects.all()
    }
    return render(request, 'home.html', context)

@login_required
def profile(request):
    '''Perfil del usuario'''
    # Nos aseguramos de que cada usuario tenga un perfil
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    context = {
        'title': 'Mi Perfil',
        'user': request.user,
        'profile': user_profile
    }
    return render(request, 'users/profile.html', context)

def register_view(request):
    '''Vista para la página de registro independiente'''
    if request.user.is_authenticated:
        return redirect('users:home') # IMPORTANTE: users:home

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'users/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return render(request, 'users/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado')
            return render(request, 'users/register.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {username}!')
            return redirect('users:home') # IMPORTANTE: users:home
        except Exception as e:
            messages.error(request, 'Ocurrió un error al crear la cuenta.')
            return render(request, 'users/register.html')

    return render(request, 'users/register.html')

def login_view(request):
    '''Vista para la página de login independiente'''
    if request.user.is_authenticated:
        return redirect('users:home') # IMPORTANTE: users:home

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            login(request, user)
            return redirect('users:home') # IMPORTANTE: users:home
        else:
            messages.error(request, 'Credenciales inválidas. Intenta de nuevo.')
    
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    # AQUÍ ESTÁ EL ERROR QUE TE SALÍA. 
    # Debe ser 'users:login', no 'login'
    return redirect('users:home')

@login_required
def update_profile(request):
    '''Vista para actualizar el perfil desde el modal'''
    if request.method == 'POST':
        user = request.user
        user_profile = Profile.objects.get(user=user)

        # Actualizar datos de User
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.error(request, 'Ese nombre de usuario ya está en uso.')
                return redirect('users:profile')
            user.username = new_username

        user.email = new_email
        user.save()

        # Actualizar foto de perfil en Profile
        if 'profile_picture' in request.FILES:
            user_profile.avatar = request.FILES['profile_picture']
            user_profile.save()

        messages.success(request, '¡Perfil actualizado con éxito!')
    return redirect('users:profile')