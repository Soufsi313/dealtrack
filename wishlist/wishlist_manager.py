# wishlist_manager.py

import json
import os

WISHLIST_FILE = os.path.join(os.path.dirname(__file__), 'wishlist.json')
DEFAULT_USER = "default"


def load_wishlist_all():
    if not os.path.exists(WISHLIST_FILE):
        return {}
    with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_wishlist(username=DEFAULT_USER):
    data = load_wishlist_all()
    return data.get(username, [])

def save_wishlist(wishlist, username=DEFAULT_USER):
    data = load_wishlist_all()
    data[username] = wishlist
    with open(WISHLIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_keyword(keyword, username=DEFAULT_USER):
    wishlist = load_wishlist(username)
    if keyword not in wishlist:
        wishlist.append(keyword)
        save_wishlist(wishlist, username)
        print(f"Mot-clé ajouté : {keyword}")
    else:
        print(f"Mot-clé déjà présent : {keyword}")

def remove_keyword(keyword, username=DEFAULT_USER):
    wishlist = load_wishlist(username)
    if keyword in wishlist:
        wishlist.remove(keyword)
        save_wishlist(wishlist, username)
        print(f"Mot-clé supprimé : {keyword}")
    else:
        print(f"Mot-clé non trouvé : {keyword}")

def show_wishlist(username=DEFAULT_USER):
    wishlist = load_wishlist(username)
    if wishlist:
        print(f"Liste de souhaits de {username} :")
        for i, kw in enumerate(wishlist, 1):
            print(f"{i}. {kw}")
    else:
        print(f"La liste de souhaits de {username} est vide.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gestion de la liste de souhaits DealTrack (multi-utilisateur)")
    parser.add_argument("action", choices=["add", "remove", "show"], help="Action à effectuer")
    parser.add_argument("keyword", nargs="?", help="Mot-clé à ajouter ou supprimer")
    parser.add_argument("--user", default=DEFAULT_USER, help="Nom d'utilisateur (par défaut : default)")
    args = parser.parse_args()

    if args.action == "add" and args.keyword:
        add_keyword(args.keyword, args.user)
    elif args.action == "remove" and args.keyword:
        remove_keyword(args.keyword, args.user)
    elif args.action == "show":
        show_wishlist(args.user)
    else:
        parser.print_help()
