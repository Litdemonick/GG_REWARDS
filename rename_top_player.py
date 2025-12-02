import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()
from django.contrib.auth.models import User
from apps.users.models import Profile

def set_top_player_name():
    target_username = "CaTAcLysMGoD"
    
    # 1. Check if the target username already exists
    existing_user = User.objects.filter(username=target_username).first()
    
    # 2. Get the current top player (highest XP)
    top_profile = Profile.objects.order_by('-xp').first()
    
    if not top_profile:
        print("No profiles found.")
        return

    current_top_user = top_profile.user
    print(f"Current top player: {current_top_user.username} with {top_profile.xp} XP")

    if current_top_user.username == target_username:
        print(f"Top player is already {target_username}.")
        return

    # 3. Handle conflict if target username exists but is not the top player
    if existing_user:
        print(f"User {target_username} already exists. Swapping names...")
        # Temporary name for the existing user
        temp_name = f"{target_username}_temp"
        existing_user.username = temp_name
        existing_user.save()
        
        # Rename top player to target
        old_name = current_top_user.username
        current_top_user.username = target_username
        current_top_user.save()
        
        # Rename the originally existing user to the old top player's name (swap)
        existing_user.username = old_name
        existing_user.save()
        print(f"Swapped: {old_name} <-> {target_username}")
        
    else:
        # Simple rename
        print(f"Renaming {current_top_user.username} to {target_username}")
        current_top_user.username = target_username
        current_top_user.save()

if __name__ == '__main__':
    set_top_player_name()
