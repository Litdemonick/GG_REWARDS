import os
import sys
import django
from django.conf import settings
from django.template import Engine, Context

# Add project root to sys.path
sys.path.append(os.getcwd())

# Configure settings manually
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'apps.users',
            'apps.games',
        ],
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(os.getcwd(), 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }],
        STATIC_URL='/static/',
        SECRET_KEY='debug_secret_key',
        ROOT_URLCONF='gg_rewards.urls', # Add this
    )
    django.setup()

from django.contrib.auth.models import User

class MockProfile:
    steam_id = '12345'
    avatar = None 
    
class MockUser:
    username = 'TestUser'
    email = 'test@example.com'
    is_authenticated = True

def check_render(path):
    try:
        engine = Engine.get_default()
        template = engine.get_template('users/profile.html')
        
        ctx = Context({
            'user': MockUser(),
            'profile': MockProfile(),
            'steam_games': []
        })
        output = template.render(ctx)
        print(f"SUCCESS: {path} rendered successfully.")
    except Exception as e:
        print(f"ERROR rendering {path}:")
        print(e)

if __name__ == "__main__":
    check_render('users/profile.html')
