# auto_promo_checker.py


import time
import threading
import promotions.promo_detector as promo_detector
from notifications.notification_manager import send_notification
import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'auto_promo_config.json')

def get_check_interval():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return int(config.get('check_interval_minutes', 60)) * 60
    return 60 * 60

class AutoPromoChecker:
    def __init__(self, interval):
        self.interval = interval
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def run(self):
        from promotions.promo_history import save_promo_to_history
        while self.running:
            promos = promo_detector.check_promos(return_results=True)
            if promos:
                for promo in promos:
                    send_notification(
                        f"Promo trouvée : {promo['site']}",
                        f"{promo['keyword']} - {promo['url']}",
                        url=promo['url']
                    )
                    save_promo_to_history(promo)
            time.sleep(self.interval)

if __name__ == "__main__":
    interval = get_check_interval()
    checker = AutoPromoChecker(interval=interval)
    checker.start()
    print(f"Vérification automatique toutes les {interval//60} minutes. Appuyez sur Ctrl+C pour arrêter.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        checker.stop()
