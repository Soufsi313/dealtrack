# notification_manager.py


import platform
import sys
import webbrowser

def send_notification(title, message, url=None):
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
    args = parser.parse_args()
    send_notification(args.title, args.message, args.url)
