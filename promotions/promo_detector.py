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
    return_results = False
    import inspect
    # Permet d'appeler check_promos(return_results=True)
    frame = inspect.currentframe().f_back
    if frame and 'return_results' in frame.f_locals:
        return_results = frame.f_locals['return_results']
    wishlist = load_wishlist()
    results = []
    for keyword in wishlist:
        for site in SITES:
            url = site["url"].format(query=keyword.replace(' ', '+'))
            if return_results:
                results.append({
                    "keyword": keyword,
                    "site": site["name"],
                    "url": url
                })
            else:
                print(f"Recherche de promotions pour '{keyword}' sur {site['name']}...")
                webbrowser.open(url)
    if return_results:
        return results

def main():
    check_promos()

if __name__ == "__main__":
    main()
