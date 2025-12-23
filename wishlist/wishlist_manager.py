# wishlist_manager.py

import json
import os

WISHLIST_FILE = os.path.join(os.path.dirname(__file__), 'wishlist.json')

def load_wishlist():
    if not os.path.exists(WISHLIST_FILE):
        return []
    with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_wishlist(wishlist):
    with open(WISHLIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(wishlist, f, ensure_ascii=False, indent=2)

def add_keyword(keyword):
    wishlist = load_wishlist()
    if keyword not in wishlist:
        wishlist.append(keyword)
        save_wishlist(wishlist)
        print(f"Mot-clé ajouté : {keyword}")
    else:
        print(f"Mot-clé déjà présent : {keyword}")

def remove_keyword(keyword):
    wishlist = load_wishlist()
    if keyword in wishlist:
        wishlist.remove(keyword)
        save_wishlist(wishlist)
        print(f"Mot-clé supprimé : {keyword}")
    else:
        print(f"Mot-clé non trouvé : {keyword}")

def show_wishlist():
    wishlist = load_wishlist()
    if wishlist:
        print("Votre liste de souhaits :")
        for i, kw in enumerate(wishlist, 1):
            print(f"{i}. {kw}")
    else:
        print("Votre liste de souhaits est vide.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gestion de la liste de souhaits DealTrack")
    parser.add_argument("action", choices=["add", "remove", "show"], help="Action à effectuer")
    parser.add_argument("keyword", nargs="?", help="Mot-clé à ajouter ou supprimer")
    args = parser.parse_args()

    if args.action == "add" and args.keyword:
        add_keyword(args.keyword)
    elif args.action == "remove" and args.keyword:
        remove_keyword(args.keyword)
    elif args.action == "show":
        show_wishlist()
    else:
        parser.print_help()
