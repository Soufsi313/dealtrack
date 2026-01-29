def check_promos_for_keyword(item):
    # item : dict {"keyword":..., "category":...}
    from .promo_history import save_promo_to_history if __package__ else (lambda x: None)
    active_sites = get_active_sites()
    kw = item["keyword"]
    for site in active_sites:
        url = site["url"].format(query=kw.replace(' ', '+'))
        print(f"Recherche de promotions pour '{kw}' sur {site['name']}...")
        import webbrowser
        webbrowser.open(url)
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

SITES_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'sites_config.json')

def get_active_sites():
    if os.path.exists(SITES_CONFIG_FILE):
        with open(SITES_CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return [site for site in SITES if config.get(site["name"], True)]
    return SITES

def load_wishlist():
    if not os.path.exists(WISHLIST_FILE):
        return []
    with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_promos(return_results=False):
    wishlist = load_wishlist()
    results = []
    active_sites = get_active_sites()
    for item in wishlist:
        # Supporte ancienne structure (str) et nouvelle (dict)
        if isinstance(item, str):
            kw = item
        else:
            kw = item.get("keyword", "")
        for site in active_sites:
            url = site["url"].format(query=kw.replace(' ', '+'))
            if return_results:
                results.append({
                    "keyword": kw,
                    "site": site["name"],
                    "url": url
                })
            else:
                print(f"Recherche de promotions pour '{kw}' sur {site['name']}...")
                webbrowser.open(url)
    if return_results:
        return results

def main():
    check_promos()

if __name__ == "__main__":
    main()
