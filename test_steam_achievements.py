import os
import django
import sys
import requests

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from django.conf import settings
from apps.api_integrations.steam_service import get_owned_games

STEAM_ID = '76561198828006966'

def get_game_achievements_debug(steam_id, app_id):
    print(f"DEBUG: Fetching for AppID {app_id}")
    
    # 1. Obtener progreso del jugador
    player_url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={settings.STEAM_API_KEY}&steamid={steam_id}"
    
    # 2. Obtener esquema del juego
    schema_url = f"http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={settings.STEAM_API_KEY}&appid={app_id}&l=spanish"
    
    try:
        # Fetch Player Stats
        print("DEBUG: Requesting Player Stats...")
        player_response = requests.get(player_url)
        print(f"DEBUG: Player Stats Status: {player_response.status_code}")
        player_data = player_response.json()
        
        if not player_data.get('playerstats', {}).get('success'):
            print("DEBUG: Player stats success is False or missing")
            print(f"DEBUG: Player Data: {player_data}")
            return []
            
        player_ach_list = player_data['playerstats'].get('achievements', [])
        print(f"DEBUG: Found {len(player_ach_list)} player achievements raw.")
        
        player_achievements = {a['apiname']: a for a in player_ach_list}
        
        # Fetch Schema
        print("DEBUG: Requesting Schema...")
        schema_response = requests.get(schema_url)
        print(f"DEBUG: Schema Status: {schema_response.status_code}")
        schema_data = schema_response.json()
        
        final_achievements = []
        
        if schema_data.get('game', {}).get('availableGameStats', {}).get('achievements'):
            schema_achievements = schema_data['game']['availableGameStats']['achievements']
            print(f"DEBUG: Found {len(schema_achievements)} schema achievements.")
            
            for sa in schema_achievements:
                api_name = sa['name']
                player_ach = player_achievements.get(api_name)
                
                if player_ach:
                    final_achievements.append({
                        'name': api_name,
                        'displayName': sa.get('displayName', api_name),
                        'achieved': player_ach.get('achieved')
                    })
                else:
                    # Print first missing one to debug
                    if len(final_achievements) == 0:
                        print(f"DEBUG: Mismatch! Schema name '{api_name}' not found in player stats.")
                        
        else:
            print("DEBUG: No achievements in schema")
            
        return final_achievements

    except Exception as e:
        print(f"Error inside function: {e}")
        return []

# 1. Get Owned Games
print("\n--- Fetching Owned Games ---")
games = get_owned_games(STEAM_ID)
if not games:
    sys.exit()

# Find Baldur's Gate 3 (1086940) or just use the first one
target_game = next((g for g in games if g['appid'] == 1086940), games[0])
app_id = target_game['appid']
game_name = target_game['name']

print(f"\n--- Testing Achievements for: {game_name} (AppID: {app_id}) ---")

achievements = get_game_achievements_debug(STEAM_ID, app_id)
print(f"Final Result: {len(achievements)} achievements.")
