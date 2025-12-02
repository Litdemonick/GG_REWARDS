import requests
from django.conf import settings

def get_steam_id(username_or_url):
    """
    Convierte un nombre de usuario (Vanity URL) o URL de perfil en un SteamID64.
    Ej: 'gabelogannewell' -> '76561197960287930'
    """
    if username_or_url.isdigit() and len(username_or_url) == 17:
        return username_or_url

    clean_name = username_or_url.replace('https://steamcommunity.com/id/', '').replace('/', '')
    
    url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={settings.STEAM_API_KEY}&vanityurl={clean_name}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('response', {}).get('success') == 1:
            return data['response']['steamid']
    except Exception as e:
        print(f"Error resolviendo Steam ID: {e}")
    
    return None

def get_player_summary(steam_id):
    """Obtiene avatar, nombre, estado y país"""
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={settings.STEAM_API_KEY}&steamids={steam_id}"
    try:
        response = requests.get(url)
        data = response.json()
        players = data.get('response', {}).get('players', [])
        if players:
            return players[0]
    except Exception as e:
        print(f"Error conectando con Steam: {e}")
    return None

# --- FUNCIÓN AUXILIAR (La moví arriba para poder usarla dentro de get_owned_games) ---
def get_game_achievement_count(steam_id, app_id):
    """
    Retorna una tupla: (desbloqueados, total).
    """
    player_url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={settings.STEAM_API_KEY}&steamid={steam_id}"
    
    try:
        # Timeout muy corto para agilizar la carga masiva
        player_response = requests.get(player_url, timeout=1.5) 
        player_data = player_response.json()
        
        if not player_data.get('playerstats', {}).get('success'):
            return 0, 0
            
        achievements = player_data['playerstats'].get('achievements', [])
        total = len(achievements)
        unlocked = sum(1 for a in achievements if a.get('achieved') == 1)
        
        return unlocked, total

    except Exception:
        # Si falla (juego sin logros o error de red), retornamos 0
        return 0, 0

def get_owned_games(steam_id):
    """
    Obtiene lista de juegos.
    MODIFICADO: Procesa hasta 60 juegos que tengan tiempo jugado.
    """
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={settings.STEAM_API_KEY}&steamid={steam_id}&format=json&include_appinfo=1&include_played_free_games=1"
    try:
        response = requests.get(url)
        data = response.json()
        games = data.get('response', {}).get('games', [])
        
        # 1. Filtramos juegos que nunca se han abierto (playtime_forever > 0)
        played_games = [g for g in games if g.get('playtime_forever', 0) > 0]
        
        # 2. Ordenamos por tiempo de juego (los más jugados primero)
        played_games.sort(key=lambda x: x.get('playtime_forever', 0), reverse=True)
        
        # 3. AUMENTAMOS EL LÍMITE:
        # Antes era [:24]. Ahora ponemos [:60]. 
        # Procesar más de 60 juegos seguidos puede causar que la web se congele por TimeOut.
        top_games = played_games[:60]

        # 4. Inyectamos los logros
        for game in top_games:
            app_id = game.get('appid')
            unlocked, total = get_game_achievement_count(steam_id, app_id)
            
            game['achievements_unlocked'] = unlocked
            game['achievements_total'] = total
            
        return top_games

    except Exception as e:
        print(f"Error obteniendo juegos: {e}")
        return []

def get_game_achievements(steam_id, app_id):
    """Obtiene los logros detallados de un juego específico"""
    player_url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={settings.STEAM_API_KEY}&steamid={steam_id}"
    schema_url = f"http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={settings.STEAM_API_KEY}&appid={app_id}&l=spanish"
    
    try:
        player_response = requests.get(player_url)
        player_data = player_response.json()
        
        if not player_data.get('playerstats', {}).get('success'):
            error_msg = player_data.get('playerstats', {}).get('error', 'Error desconocido')
            return [], error_msg
            
        player_ach_list = player_data['playerstats'].get('achievements', [])
        player_achievements = {a['apiname']: a for a in player_ach_list}
        
        schema_response = requests.get(schema_url)
        schema_data = schema_response.json()
        
        final_achievements = []
        
        if schema_data.get('game', {}).get('availableGameStats', {}).get('achievements'):
            schema_achievements = schema_data['game']['availableGameStats']['achievements']
            
            for sa in schema_achievements:
                api_name = sa['name']
                player_ach = player_achievements.get(api_name)
                
                if player_ach:
                    final_achievements.append({
                        'name': api_name,
                        'displayName': sa.get('displayName', api_name),
                        'description': sa.get('description', ''),
                        'icon': sa.get('icon'),
                        'icon_gray': sa.get('icongray'),
                        'achieved': player_ach.get('achieved') == 1,
                        'unlocktime': player_ach.get('unlocktime')
                    })
                    
        return final_achievements, None

    except Exception as e:
        return [], str(e)

def validate_steam_openid(params):
    validation_params = params.copy()
    validation_params['openid.mode'] = 'check_authentication'
    url = 'https://steamcommunity.com/openid/login'
    try:
        response = requests.post(url, data=validation_params)
        if 'is_valid:true' in response.text:
            claimed_id = params.get('openid.claimed_id', '')
            if claimed_id:
                return claimed_id.split('/')[-1]
    except Exception as e:
        print(f"Error validando OpenID: {e}")
    return None