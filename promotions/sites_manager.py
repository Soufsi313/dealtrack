# sites_manager.py
import json
import os

SITES_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'sites_config.json')

SITES = [
    "Amazon.fr",
    "Instant Gaming",
    "Google"
]

def load_config():
    if os.path.exists(SITES_CONFIG_FILE):
        with open(SITES_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {site: True for site in SITES}

def save_config(config):
    with open(SITES_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def show_config():
    config = load_config()
    print("Sites surveillés :")
    for site in SITES:
        status = "[X]" if config.get(site, True) else "[ ]"
        print(f"{status} {site}")

def toggle_site(site_name):
    config = load_config()
    if site_name in SITES:
        config[site_name] = not config.get(site_name, True)
        save_config(config)
        print(f"{site_name} est maintenant {'activé' if config[site_name] else 'désactivé'}.")
    else:
        print(f"Site inconnu : {site_name}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gestion des sites surveillés DealTrack")
    parser.add_argument("action", choices=["show", "toggle"], help="Action à effectuer")
    parser.add_argument("site", nargs="?", help="Nom du site à activer/désactiver")
    args = parser.parse_args()

    if args.action == "show":
        show_config()
    elif args.action == "toggle" and args.site:
        toggle_site(args.site)
    else:
        parser.print_help()
