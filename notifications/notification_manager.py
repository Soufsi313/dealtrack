
# notification_manager.py

import os
import platform
import sys
import webbrowser
import json
from datetime import datetime

NOTIF_HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'notifications_history.json')

def save_notification_history(username, title, message, url=None):
    if os.path.exists(NOTIF_HISTORY_FILE):
        with open(NOTIF_HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}
    notif = {
        "title": title,
        "message": message,
        "url": url,
        "timestamp": datetime.now().isoformat(sep=' ', timespec='seconds')
    }
    if username not in data:
        data[username] = []
    data[username].append(notif)
    with open(NOTIF_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def send_notification(title, message, url=None, username="default"):
    save_notification_history(username, title, message, url)
    if platform.system() == "Windows" and url is not None:
        try:
            from win10toast_click import ToastNotifier
            def open_url():
                webbrowser.open(url)
            toaster = ToastNotifier()
            toaster.show_toast(
                title,
                message,
                duration=10,
                threaded=True,
                callback_on_click=open_url
            )
        except ImportError:
            print("Le module 'win10toast_click' est requis pour les notifications interactives. Installez-le avec 'pip install win10toast-click'.")
    else:
        try:
            from plyer import notification
            notification.notify(
                title=title,
                message=message,
                app_name="DealTrack",
                timeout=10
            )
        except ImportError:
            print("Le module 'plyer' est requis pour les notifications. Installez-le avec 'pip install plyer'.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Envoi d'une notification DealTrack")
    parser.add_argument("title", help="Titre de la notification")
    parser.add_argument("message", help="Message de la notification")
    parser.add_argument("--url", help="URL à ouvrir au clic sur la notification", default=None)
    parser.add_argument("--user", help="Nom d'utilisateur (pour l'historique)", default="default")
    args = parser.parse_args()
    send_notification(args.title, args.message, args.url, args.user)
