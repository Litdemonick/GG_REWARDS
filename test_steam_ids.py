import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.users.models import Profile
from apps.api_integrations.steam_service import get_owned_games

print("=== TESTING STEAM IDS ===\n")

# Get all profiles with Steam ID
profiles = Profile.objects.filter(steam_id__isnull=False)

for profile in profiles:
    print(f"User: {profile.user.username}")
    print(f"Steam ID: {profile.steam_id}")
    
    # Get games for this Steam ID
    games = get_owned_games(profile.steam_id)
    
    if games:
        print(f"Total games: {len(games)}")
        print("Top 5 games:")
        for game in games[:5]:
            playtime_hours = game.get('playtime_forever', 0) / 60
            print(f"  - {game['name']}: {playtime_hours:.1f} hours")
    else:
        print("No games found or profile is private")
    
    print("-" * 50)
