import os
import json

CATEGORIES_FILE = os.path.join(os.path.dirname(__file__), 'categories.json')

def load_categories():
    if os.path.exists(CATEGORIES_FILE):
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return ["Jeu", "Console", "Matériel"]

def save_categories(categories):
    with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gestion des catégories DealTrack")
    parser.add_argument("action", choices=["list", "add", "remove"], help="Action à effectuer")
    parser.add_argument("category", nargs="?", help="Catégorie à ajouter ou supprimer")
    args = parser.parse_args()
    cats = load_categories()
    if args.action == "list":
        print("Catégories :", ", ".join(cats))
    elif args.action == "add" and args.category:
        if args.category in cats:
            print("Catégorie déjà présente.")
        else:
            cats.append(args.category)
            save_categories(cats)
            print("Catégorie ajoutée.")
    elif args.action == "remove" and args.category:
        if args.category not in cats:
            print("Catégorie non trouvée.")
        else:
            cats.remove(args.category)
            save_categories(cats)
            print("Catégorie supprimée.")
    else:
        parser.print_help()
