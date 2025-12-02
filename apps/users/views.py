from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from apps.games.models import Game
from django.shortcuts import render, redirect, get_object_or_404 # Agrega get_object_or_404 arriba
from django.urls import reverse
from .models import Profile
from urllib.parse import urlencode
from apps.api_integrations.steam_service import validate_steam_openid, get_owned_games, get_game_achievements, get_steam_id, get_game_achievement_count

# --- FUNCIÓN AUXILIAR PARA CALCULAR EL RANGO ---
def calculate_rank(level):
    """Devuelve el nombre del rango basado en el nivel del usuario"""
    if level < 5: return "NOVATO"
    if level < 10: return "APRENDIZ"
    if level < 20: return "PROFESIONAL"
    if level < 50: return "VETERANO"
    if level < 100: return "MAESTRO"
    return "LEYENDA"

def home(request):
    top_players = Profile.objects.order_by('-xp')[:3]  # SOLO TOP 3
    games = Game.objects.all().order_by('-rating')[:10]

    return render(request, "home.html", {
        "top_players": top_players,
        "games": games,
    })

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
            user_exists = False
            if User.objects.filter(username=username_or_email).exists():
                user_exists = True
            elif User.objects.filter(email=username_or_email).exists():
                user_exists = True
            
            if not user_exists:
                messages.error(request, 'La cuenta no existe.')
            else:
                messages.error(request, 'Credenciales inválidas. Intenta de nuevo.')
            
            return redirect(request.META.get('HTTP_REFERER', 'users:home'))
    
    # Redirigir al home con el parámetro login=true para abrir el modal
    return redirect('/?login=true')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    return redirect('users:home')

# --- PERFIL OPTIMIZADO (CARGA RÁPIDA) ---
@login_required
def profile(request):
    """
    Perfil del usuario - MODO ULTRA RÁPIDO
    Lee los datos guardados en la base de datos (games_cache) y NO conecta a Steam.
    """
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    # Leemos directamente del caché de la base de datos (Instantáneo)
    steam_games = user_profile.games_cache

    # Lógica de barra de progreso (Matemática local)
    xp_threshold = 1000
    current_xp = user_profile.xp if user_profile.xp else 0
    
    xp_progress = current_xp % xp_threshold
    xp_percentage = (xp_progress / xp_threshold) * 100

    context = {
        'title': 'Mi Perfil',
        'user': request.user,
        'profile': user_profile,
        'steam_games': steam_games,
        'xp_progress': xp_progress,
        'xp_percentage': xp_percentage,
        'xp_threshold': xp_threshold
    }
    return render(request, 'users/profile.html', context)

def rankings_view(request):
    """Muestra el Top 100 de jugadores por XP"""
    # Obtener top 100 ordenados por XP descendente
    top_players = Profile.objects.select_related('user').order_by('-xp')[:100]
    
    # Buscar la posición del usuario actual
    user_rank = None
    if request.user.is_authenticated:
        # Esto es una forma simple de buscar el rank. 
        # En apps grandes se hace con Window functions de SQL, pero esto sirve para empezar.
        all_ids = list(Profile.objects.order_by('-xp').values_list('user_id', flat=True))
        try:
            user_rank = all_ids.index(request.user.id) + 1
        except ValueError:
            user_rank = 0

    context = {
        'title': 'Rankings Globales',
        'top_players': top_players,
        'user_rank': user_rank
    }
    return render(request, 'users/rankings.html', context)



def public_profile_view(request, username):
    """
    Muestra el perfil de OTRO usuario.
    INCLUYE AUTO-REPARACIÓN CON FILTRO > 0 LOGROS.
    """
    view_user = get_object_or_404(User, username=username)
    user_profile, created = Profile.objects.get_or_create(user=view_user)
    
    steam_games = user_profile.games_cache

    # Detectamos si los datos son viejos o necesitan actualización
    data_is_stale = False
    if steam_games and len(steam_games) > 0:
        if 'achievements_total' not in steam_games[0]:
            data_is_stale = True
    
    if (data_is_stale or not steam_games) and user_profile.steam_id:
        try:
            updated_games = get_owned_games(user_profile.steam_id)
            
            if updated_games:
                filtered_games = []
                total_xp = 0
                total_trophies = 0
                
                for game in updated_games:
                    ach_unlocked = game.get('achievements_unlocked', 0)
                    
                    # FILTRO: Solo juegos con logros
                    if ach_unlocked > 0:
                        game['hours_played'] = round(game.get('playtime_forever', 0) / 60, 1)
                        filtered_games.append(game)
                        
                        total_xp += (ach_unlocked * 10) 
                        total_trophies += ach_unlocked

                # Guardar datos filtrados
                user_profile.games_cache = filtered_games
                user_profile.xp = total_xp
                user_profile.level = 1 + (total_xp // 1000)
                user_profile.trophies = total_trophies
                user_profile.rank = calculate_rank(user_profile.level)
                user_profile.save()
                
                steam_games = filtered_games
        except Exception as e:
            print(f"Error auto-reparando perfil: {e}")

    # Calculamos la barra de progreso
    xp_threshold = 1000
    current_xp = user_profile.xp if user_profile.xp else 0
    xp_progress = current_xp % xp_threshold
    
    if xp_threshold > 0:
        xp_percentage = int((xp_progress / xp_threshold) * 100)
    else:
        xp_percentage = 0

    context = {
        'title': f'Perfil de {view_user.username}',
        'view_user': view_user,
        'profile': user_profile,
        'steam_games': steam_games,
        'xp_progress': xp_progress,
        'xp_percentage': xp_percentage,
        'xp_threshold': xp_threshold,
        'is_own_profile': (request.user == view_user) 
    }
    return render(request, 'users/public_profile.html', context)

@login_required
def update_profile(request):
    '''Vista para actualizar el perfil desde el modal'''
    if request.method == 'POST':
        user = request.user
        user_profile = Profile.objects.get(user=user)

        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.error(request, 'Ese nombre de usuario ya está en uso.')
                return redirect('users:profile')
            user.username = new_username

        user.email = new_email
        user.save()

        if 'profile_picture' in request.FILES:
            user_profile.avatar = request.FILES['profile_picture']
            user_profile.save()

        messages.success(request, '¡Perfil actualizado con éxito!')
    return redirect('users:profile')

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
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.steam_id = steam_id
        profile.save()
        messages.success(request, '¡Cuenta de Steam vinculada exitosamente! Sincronizando...')
        # Redirigir a sincronización automática
        return redirect('users:sync_steam')
    else:
        messages.error(request, 'Error al vincular la cuenta de Steam.')
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
                messages.success(request, '¡Cuenta de Steam vinculada! Sincronizando...')
                # Redirigir a sincronización automática
                return redirect('users:sync_steam')
            else:
                messages.error(request, 'No se pudo encontrar ese usuario de Steam.')
        else:
            messages.error(request, 'Por favor ingresa un ID o URL.')
    return redirect('users:profile')

@login_required
def unlink_steam(request):
    """Desvincula la cuenta de Steam del usuario"""
    if request.method == 'POST':
        user_profile = Profile.objects.get(user=request.user)
        user_profile.steam_id = None
        # Resetear estadísticas
        user_profile.trophies = 0
        user_profile.xp = 0
        user_profile.level = 1
        user_profile.rank = 'NOVATO' # Resetear rango
        user_profile.games_cache = [] # Limpiar caché
        user_profile.save()
        messages.success(request, 'Cuenta de Steam desvinculada correctamente.')
    
    return redirect('users:profile')

# --- SINCRONIZACIÓN PESADA (AQUÍ SE PROCESAN LOS DATOS Y RANGOS) ---
@login_required
def sync_steam(request):
    """
    Sincroniza manualmente los datos de Steam.
    FILTRO: Solo guarda juegos con al menos 1 logro desbloqueado.
    """
    user_profile = Profile.objects.get(user=request.user)
    
    if not user_profile.steam_id:
        messages.error(request, 'No tienes una cuenta de Steam vinculada.')
        return redirect('users:profile')

    try:
        # Trae los top 60 juegos más jugados (con sus logros ya contados por steam_service)
        all_games = get_owned_games(user_profile.steam_id)
        
        if all_games:
            processed_games = []
            total_xp = 0
            total_trophies = 0
            
            for game in all_games:
                ach_unlocked = game.get('achievements_unlocked', 0)
                
                # --- AQUÍ ESTÁ EL FILTRO MÁGICO ---
                # Solo procesamos y guardamos el juego si tiene al menos 1 logro.
                if ach_unlocked > 0:
                    
                    # Formato de horas
                    game['hours_played'] = round(game.get('playtime_forever', 0) / 60, 1)
                    
                    # Agregamos a la lista final
                    processed_games.append(game)
                    
                    # Calculamos XP y Trofeos
                    total_xp += (ach_unlocked * 10) 
                    total_trophies += ach_unlocked
            
            # Guardamos SOLO los juegos filtrados en la base de datos
            user_profile.games_cache = processed_games
            user_profile.xp = total_xp
            user_profile.level = 1 + (total_xp // 1000)
            user_profile.trophies = total_trophies
            
            # Recalcular Rango
            user_profile.rank = calculate_rank(user_profile.level)
            
            user_profile.save()
            
            count_removed = len(all_games) - len(processed_games)
            messages.success(request, f'¡Sincronización completada! Se ocultaron {count_removed} juegos sin logros.')
        else:
            user_profile.games_cache = []
            user_profile.save()
            messages.warning(request, 'No se encontraron juegos con datos visibles.')

    except Exception as e:
        print(f"Error en sincronización: {e}")
        messages.error(request, 'Ocurrió un error al conectar con Steam.')
    
    return redirect('users:profile')

@login_required
def game_achievements(request, app_id):
    """Muestra los logros de un juego específico"""
    user_profile = Profile.objects.get(user=request.user)
    
    if not user_profile.steam_id:
        messages.error(request, 'Debes vincular tu cuenta de Steam primero.')
        return redirect('users:profile')

    achievements, error_msg = get_game_achievements(user_profile.steam_id, app_id)
    
    game_name = request.GET.get('game_name', 'Juego')

    context = {
        'title': f'Logros - {game_name}',
        'achievements': achievements,
        'error_msg': error_msg,
        'game_name': game_name,
        'app_id': app_id
    }
    return render(request, 'users/game_achievements.html', context)