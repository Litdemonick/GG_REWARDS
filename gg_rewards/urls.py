from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas de Usuarios (Incluye Home, Login, Register, Profile)
    path('', include('apps.users.urls')),
    
    # Rutas de otras aplicaciones
    path('trophies/', include('apps.trophies.urls')),
    path('rankings/', include('apps.rankings.urls')),
    path('api/', include('apps.api_integrations.urls')),
    path('games/', include('apps.games.urls')),
]

# Configuración para servir archivos estáticos y media en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)