import requests
from django.conf import settings

def get_steam_id(username_or_url):
    """
    Convierte un nombre de usuario (Vanity URL) o URL de perfil en un SteamID64.
    Ej: 'gabelogannewell' -> '76561197960287930'
    """
    # Si el usuario ya metió un ID numérico de 17 dígitos, lo devolvemos directo
    if username_or_url.isdigit() and len(username_or_url) == 17:
        return username_or_url

    # Limpiamos la entrada por si pegaron la URL completa
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
            return players[0] # Devuelve un diccionario con datos del usuario
    except Exception as e:
        print(f"Error conectando con Steam: {e}")
    return None

def get_owned_games(steam_id):
    """
    Obtiene lista de juegos, tiempo jugado e iconos.
    Importante: El perfil del usuario debe ser PÚBLICO para que esto funcione.
    """
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={settings.STEAM_API_KEY}&steamid={steam_id}&format=json&include_appinfo=1&include_played_free_games=1"
    try:
        response = requests.get(url)
        data = response.json()
        games = data.get('response', {}).get('games', [])
        # Ordenar por tiempo de juego (playtime_forever está en minutos)
        games.sort(key=lambda x: x.get('playtime_forever', 0), reverse=True)
        return games
    except Exception as e:
        print(f"Error obteniendo juegos: {e}")
        return []

def get_game_achievements(steam_id, app_id):
    """Obtiene los logros de un juego específico para este usuario, incluyendo detalles (iconos, nombres)"""
    # 1. Obtener progreso del jugador
    player_url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={settings.STEAM_API_KEY}&steamid={steam_id}"
    
    # 2. Obtener esquema del juego (nombres, iconos, descripciones)
    schema_url = f"http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={settings.STEAM_API_KEY}&appid={app_id}&l=spanish"
    
    try:
        # Fetch Player Stats
        player_response = requests.get(player_url)
        player_data = player_response.json()
        
        if not player_data.get('playerstats', {}).get('success'):
            error_msg = player_data.get('playerstats', {}).get('error', 'Error desconocido de Steam')
            print(f"DEBUG: Steam API Error: {error_msg}")
            return [], error_msg
            
        player_ach_list = player_data['playerstats'].get('achievements', [])
        player_achievements = {a['apiname']: a for a in player_ach_list}
        
        # Fetch Schema
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
        print(f"Error obteniendo logros: {e}")
        return [], str(e)

def validate_steam_openid(params):
    """
    Valida la respuesta de autenticación de Steam OpenID.
    Retorna el Steam ID si es válido, o None si falla.
    """
    # Los parámetros para validar deben incluir mode='check_authentication'
    validation_params = params.copy()
    validation_params['openid.mode'] = 'check_authentication'
    
    url = 'https://steamcommunity.com/openid/login'
    
    try:
        response = requests.post(url, data=validation_params)
        if 'is_valid:true' in response.text:
            # Extraer Steam ID de openid.claimed_id
            # Formato: https://steamcommunity.com/openid/id/76561198000000000
            claimed_id = params.get('openid.claimed_id', '')
            if claimed_id:
                return claimed_id.split('/')[-1]
    except Exception as e:
        print(f"Error validando OpenID: {e}")
        
    return None