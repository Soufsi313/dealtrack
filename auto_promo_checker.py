# auto_promo_checker.py

import time
import threading
import promotions.promo_detector as promo_detector
from notifications.notification_manager import send_notification

CHECK_INTERVAL = 60 * 60  # 1 heure (en secondes)

class AutoPromoChecker:
    def __init__(self, interval=CHECK_INTERVAL):
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
                        f"{promo['keyword']} - {promo['url']}"
                    )
                    save_promo_to_history(promo)
            time.sleep(self.interval)

if __name__ == "__main__":
    checker = AutoPromoChecker(interval=60)  # Pour test, vérifie toutes les minutes
    checker.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        checker.stop()
