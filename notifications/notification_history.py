import os
import json

NOTIF_HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'notifications_history.json')

def get_notifications_history(username):
    if os.path.exists(NOTIF_HISTORY_FILE):
        with open(NOTIF_HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get(username, [])
    return []

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Afficher l'historique des notifications pour un utilisateur DealTrack")
    parser.add_argument("--user", help="Nom d'utilisateur", default="default")
    args = parser.parse_args()
    history = get_notifications_history(args.user)
    if history:
        for notif in history:
            print(f"{notif['timestamp']} | {notif['title']} | {notif['message']} | {notif.get('url','')}")
    else:
        print("Aucune notification enregistrée pour cet utilisateur.")
