import os
import django
import requests
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from django.conf import settings
from apps.users.models import Profile

def debug_steam_api():
    print("=== DEBUGGING STEAM API ===")
    
    # 1. Get the first user with a Steam ID
    profile = Profile.objects.filter(steam_id__isnull=False).first()
    
    if not profile:
        print("No users with Steam ID found in database.")
        return

    steam_id = profile.steam_id
    print(f"Testing with User: {profile.user.username}")
    print(f"Steam ID: {steam_id}")
    
    # 2. Get Owned Games to pick one
    games_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={settings.STEAM_API_KEY}&steamid={steam_id}&format=json&include_appinfo=1"
    print(f"\nFetching Games from: {games_url.replace(settings.STEAM_API_KEY, 'HIDDEN_KEY')}")
    
    try:
        games_resp = requests.get(games_url)
        games_data = games_resp.json()
        
        if not games_data.get('response', {}).get('games'):
            print("ERROR: Could not fetch games. Response:")
            print(games_data)
            return
            
        games = games_data['response']['games']
        print(f"Found {len(games)} games.")
        
        # Pick a game with achievements (e.g., CS2 - 730, or just the first one)
        # Let's try to find a popular one that likely has achievements
        target_game = None
        for game in games:
            if game['appid'] == 730: # CS2
                target_game = game
                break
        
        if not target_game:
            target_game = games[0]
            
        app_id = target_game['appid']
        game_name = target_game['name']
        print(f"\nTesting Achievements for: {game_name} (AppID: {app_id})")
        
        # 3. Test Player Achievements Endpoint
        player_url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={settings.STEAM_API_KEY}&steamid={steam_id}"
        print(f"Fetching Player Stats from: {player_url.replace(settings.STEAM_API_KEY, 'HIDDEN_KEY')}")
        
        player_resp = requests.get(player_url)
        print(f"Status Code: {player_resp.status_code}")
        
        try:
            player_data = player_resp.json()
            print("Response Body (Truncated):")
            print(str(player_data)[:500] + "...")
            
            if not player_data.get('playerstats', {}).get('success'):
                print("\n!!! FAILURE DETECTED !!!")
                print("The API returned success=false or missing data.")
                print("Common causes:")
                print("1. Profile is Private")
                print("2. Game Details are Private (Check Steam Privacy Settings -> Game Details)")
                print("3. Game has no achievements")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            print(player_resp.text)

    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    debug_steam_api()
