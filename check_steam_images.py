import requests

games = {
    "Cyberpunk 2077": "1091500",
    "Hollow Knight: Silksong": "1030300",
    "Elden Ring": "1245620",
    "God of War Ragnarök": "2322010",
    "Baldur's Gate 3": "1086940",
    "Final Fantasy VII Rebirth": "2930160",
    "Black Myth: Wukong": "2358720"
}

for title, app_id in games.items():
    url = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{app_id}/library_600x900.jpg"
    try:
        response = requests.head(url)
        if response.status_code == 200:
            print(f"[OK] {title}: {url}")
        else:
            print(f"[FAIL] {title}: {url} (Status: {response.status_code})")
            # Try header.jpg as fallback
            fallback = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{app_id}/header.jpg"
            resp2 = requests.head(fallback)
            if resp2.status_code == 200:
                 print(f"   -> Fallback [OK]: {fallback}")
            else:
                 print(f"   -> Fallback [FAIL]: {fallback}")

    except Exception as e:
        print(f"[ERROR] {title}: {e}")
