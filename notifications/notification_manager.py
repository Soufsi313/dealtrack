# notification_manager.py

import platform
import sys

try:
    from plyer import notification
except ImportError:
    print("Le module 'plyer' est requis pour les notifications. Installez-le avec 'pip install plyer'.")
    sys.exit(1)

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="DealTrack",
        timeout=10
    )

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Envoi d'une notification DealTrack")
    parser.add_argument("title", help="Titre de la notification")
    parser.add_argument("message", help="Message de la notification")
    args = parser.parse_args()
    send_notification(args.title, args.message)
