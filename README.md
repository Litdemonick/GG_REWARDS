<<<<<<< HEAD
# Twittor — Mini Twitter con Django + Tailwind (CDN)
=======
# 🎮 GG Rewards – Plataforma de Logros y Recompensas Gamers  
Proyecto Final – DSWV  
Grupo: Los 5 Furiosos
>>>>>>> origin/main

Proyecto educativo minimalista que imita lo básico de Twitter: timeline, publicar (texto + imagen), likes, respuestas, perfiles y seguir/dejar de seguir.

<<<<<<< HEAD
## Requisitos
- Python 3.10+
- pip y venv (recomendado)
- (Opcional) Node NO es necesario: usamos Tailwind por CDN.
=======
## 📌 Descripción del Proyecto
GG Rewards es una plataforma web diseñada para que los gamers puedan registrar sus videojuegos, desbloquear logros, ganar puntos y competir en rankings globales. Cada usuario cuenta con un perfil personalizado donde se muestran sus logros, medallas, nivel de experiencia y estadísticas de juego.
>>>>>>> origin/main

## Instalación
```bash
cd twittor
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser  # opcional
python manage.py runserver
```

<<<<<<< HEAD
Visita: http://127.0.0.1:8000/

## Funcionalidades
- Registro, login, logout (Django auth)
- Timeline: tus posts + los de la gente que sigues
- Crear publicación (hasta 280 caracteres, imagen opcional)
- Likes y respuestas
- Perfiles con avatar y bio
- Seguir / dejar de seguir

## Notas
- Archivos subidos (avatars, imágenes) se guardan en `media/`.
- En producción: cambia `SECRET_KEY`, desactiva `DEBUG`, configura `ALLOWED_HOSTS` y un servidor para estáticos/media.

=======
## 🚀 Características Principales

### 🔥 Must (Imprescindible)
- Registro/Login de usuarios  
- Catálogo de videojuegos con CRUD  
- Sistema de logros asignados manualmente desde el panel admin  

### ⭐ Should (Muy Recomendable)
- Ranking global por puntos y logros  
- Historial de logros en el perfil del usuario  
- Perfiles personalizables (avatar, bio, juegos favoritos)  
- Clasificación de logros (Bronce, Plata, Oro, Platino)  

### 🌀 Could (Extras Atractivos)
- Integración con APIs de Steam, Riot, Xbox, PlayStation, Epic  
- Medallas digitales especiales  
- Exportar logros a PDF/Excel  
- Sistema de niveles y experiencia (XP)  
- Módulo social: amigos, comentarios y chat gamer  
>>>>>>> origin/main

## Novedades
- Retuits y citas (quote tweet)
- Búsqueda y hashtags con linkify
- Notificaciones por likes, comentarios, follows y retuits/citas
- Botón de like con HTMX (no recarga)

<<<<<<< HEAD
**Importante:** como se agregaron campos nuevos, ejecuta:
```bash
python manage.py makemigrations
python manage.py migrate
```
=======
## 🛠 Tecnologías Utilizadas
- Backend: Django / Spring Boot / Node.js  
- Frontend: HTML5, Tailwind CSS, JavaScript  
- Base de Datos: SQLite3 / MySQL / PostgreSQL  
- APIs externas: IGDB, Steam Web API (opcional)  
>>>>>>> origin/main


<<<<<<< HEAD
## Poblar con datos de demostración

Instala Faker y ejecuta el comando `seed`:
=======
## 🧱 Arquitectura del Sistema

    /GG-Rewards
    │── src/
    │   ├── backend/
    │   ├── frontend/
    │   ├── database/
    │   └── api/
    │
    │── docs/
    │── assets/
    │── README.md
    │── LICENSE

---

## 📸 Capturas (Opcional)
> (Aquí puedes agregar screenshots del login, dashboard, perfiles, rankings, etc.)
>>>>>>> origin/main

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed --fresh --users 25 --tweets 150 --images --superuser
# usuario superuser (opcional): admin / admin12345
# usuarios normales: contraseña por defecto demo12345
```

<<<<<<< HEAD
Parámetros útiles:
- `--users N` cantidad de usuarios (por defecto 25)
- `--tweets N` cantidad de publicaciones base (por defecto 150)
- `--retweet_ratio 0.15` proporción de retuits respecto a tweets base
- `--quote_ratio 0.10` proporción de citas
- `--like_factor 0.25` fracción aproximada de usuarios que dan like a cada tweet
- `--comment_factor 0.20` fracción de tweets con 1–3 comentarios
- `--images` genera imágenes dummy para algunos tweets
- `--fresh` elimina datos previos (excepto superusuarios)
- `--password` cambia la contraseña por defecto de los usuarios demo
=======
## 👥 Integrantes del Proyecto – Los 5 Furiosos
| Nombre | Rol |
|--------|------|
| Carlos Miranda | Backend / Base de datos |
| Brayan Quintero | Frontend / UI |
| Eliecias Cubilla | Lógica del sistema / API |
| Harold Morales | Documentación / Testing |
| Eddie Man | Integración / DevOps |

---

## 🏁 Objetivo del Proyecto
Crear una plataforma funcional, escalable y atractiva para demostrar dominio en:
- CRUD avanzados  
- Diseño responsivo  
- Seguridad y roles  
- Conexión con APIs  
- Gamificación  
- Buenas prácticas de desarrollo  

---

## 📄 Licencia
Este proyecto está bajo la licencia MIT.  
Puedes usarlo, modificarlo y distribuirlo libremente.

---

## 💬 Contacto
Si deseas contribuir, mejorar el proyecto o reportar errores, no dudes en abrir un issue o enviar un pull request.
>>>>>>> origin/main
