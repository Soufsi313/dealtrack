# promo_detector.py

import webbrowser
import requests
from bs4 import BeautifulSoup
import os
import json

WISHLIST_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'wishlist', 'wishlist.json')

SITES = [
    {
        "name": "Amazon.fr",
        "url": "https://www.amazon.fr/s?k={query}"
    },
    {
        "name": "Instant Gaming",
        "url": "https://www.instant-gaming.com/fr/rechercher/?q={query}"
    },
    {
        "name": "Google",
        "url": "https://www.google.com/search?q={query}+promo"
    }
]

def load_wishlist():
    if not os.path.exists(WISHLIST_FILE):
        return []
    with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_promos():
    wishlist = load_wishlist()
    for keyword in wishlist:
        for site in SITES:
            url = site["url"].format(query=keyword.replace(' ', '+'))
            print(f"Recherche de promotions pour '{keyword}' sur {site['name']}...")
            # Pour Amazon et Instant Gaming, on pourrait scraper les résultats, ici on ouvre simplement le site
            webbrowser.open(url)
            # Pour un vrai scraping, il faudrait analyser le HTML et détecter les promos
            # (non implémenté ici pour simplicité et respect des conditions d'utilisation)

def main():
    check_promos()

if __name__ == "__main__":
    main()
