from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from apps.games.models import Game
from django.urls import reverse
from urllib.parse import urlencode
from apps.api_integrations.steam_service import validate_steam_openid, get_owned_games, get_game_achievements, get_steam_id

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

    steam_games = []
    if user_profile.steam_id:
        steam_games = get_owned_games(user_profile.steam_id)
        # Opcional: Limitar a los top 10 juegos con más horas
        steam_games = steam_games[:10]

    context = {
        'title': 'Mi Perfil',
        'user': request.user,
        'profile': user_profile,
        'steam_games': steam_games
    }
    return render(request, 'users/profile.html', context)

@login_required
def steam_login(request):
    """Inicia el flujo de autenticación con Steam OpenID"""
    steam_openid_url = 'https://steamcommunity.com/openid/login'
    params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': request.build_absolute_uri(reverse('users:steam_callback')),
        'openid.realm': request.build_absolute_uri('/'),
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
    }
    return redirect(f"{steam_openid_url}?{urlencode(params)}")

@login_required
def steam_callback(request):
    """Maneja el retorno de Steam después del login"""
    params = request.GET.dict()
    
    steam_id = validate_steam_openid(params)
    
    if steam_id:
        # Guardar Steam ID en el perfil del usuario
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.steam_id = steam_id
        profile.save()
        messages.success(request, '¡Cuenta de Steam vinculada exitosamente!')
    else:
        messages.error(request, 'Error al vincular la cuenta de Steam.')
        
    return redirect('users:profile')

def register_view(request):
    '''Vista para la página de registro independiente'''
    if request.user.is_authenticated:
        return redirect('users:home')

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
            return redirect('users:home')
        except Exception as e:
            messages.error(request, 'Ocurrió un error al crear la cuenta.')
            return render(request, 'users/register.html')

    return render(request, 'users/register.html')

def login_view(request):
    '''Vista para la página de login independiente'''
    if request.user.is_authenticated:
        return redirect('users:home')

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
            return redirect('users:home')
        else:
            messages.error(request, 'Credenciales inválidas. Intenta de nuevo.')
    
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
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

@login_required
def game_achievements(request, app_id):
    """Muestra los logros de un juego específico"""
    user_profile = Profile.objects.get(user=request.user)
    
    if not user_profile.steam_id:
        messages.error(request, 'Debes vincular tu cuenta de Steam primero.')
        return redirect('users:profile')

    achievements, error_msg = get_game_achievements(user_profile.steam_id, app_id)
    
    # Intentar obtener nombre del juego (esto es un hack porque la API de logros no devuelve el nombre del juego directamente fácil)
    # En una app real, deberíamos tener una base de datos de juegos o hacer otra call a la API.
    # Por ahora lo pasamos como parámetro GET o simplemente mostramos "Logros del Juego"
    game_name = request.GET.get('game_name', 'Juego')

    context = {
        'title': f'Logros - {game_name}',
        'achievements': achievements,
        'error_msg': error_msg,
        'game_name': game_name,
        'app_id': app_id
    }
    return render(request, 'users/game_achievements.html', context)

@login_required
def unlink_steam(request):
    """Desvincula la cuenta de Steam del usuario"""
    if request.method == 'POST':
        user_profile = Profile.objects.get(user=request.user)
        user_profile.steam_id = None
        user_profile.save()
        messages.success(request, 'Cuenta de Steam desvinculada correctamente.')
    
    return redirect('users:profile')

@login_required
def link_steam(request):
    """Vincula la cuenta de Steam manualmente usando ID o URL"""
    if request.method == 'POST':
        steam_input = request.POST.get('steam_input')
        if steam_input:
            steam_id = get_steam_id(steam_input)
            if steam_id:
                profile, created = Profile.objects.get_or_create(user=request.user)
                profile.steam_id = steam_id
                profile.save()
                messages.success(request, '¡Cuenta de Steam vinculada exitosamente!')
            else:
                messages.error(request, 'No se pudo encontrar ese usuario de Steam. Verifica que el perfil sea público o el ID sea correcto.')
        else:
            messages.error(request, 'Por favor ingresa un ID o URL.')
    
    return redirect('users:profile')