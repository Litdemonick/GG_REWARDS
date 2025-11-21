import os
import django
from django.conf import settings
from django.template import Engine

# Setup minimal Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

def check_template(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Attempt to compile the template
        Engine.get_default().from_string(content)
        print(f"SUCCESS: {path} compiled successfully.")
    except Exception as e:
        print(f"ERROR in {path}:")
        print(e)

if __name__ == "__main__":
    check_template('templates/users/profile.html')
