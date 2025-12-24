# promo_history.py
import os
import json
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'promotions', 'promo_history.json')

def save_promo_to_history(promo):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []
    promo["timestamp"] = datetime.now().isoformat(sep=' ', timespec='seconds')
    history.append(promo)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

if __name__ == "__main__":
    history = get_history()
    if history:
        for promo in history:
            print(f"{promo['timestamp']} | {promo['site']} | {promo['keyword']} | {promo['url']}")
    else:
        print("Aucune promotion enregistrée.")
