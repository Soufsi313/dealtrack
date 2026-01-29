# dealtrack_gui.py

import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, END
import os
import json
import subprocess

WISHLIST_FILE = os.path.join(os.path.dirname(__file__), 'wishlist', 'wishlist.json')
PROMO_DETECTOR = os.path.join(os.path.dirname(__file__), 'promotions', 'promo_detector.py')

class DealTrackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DealTrack")
        self.geometry("400x400")
        self.resizable(False, False)
        self.create_widgets()
        self.load_wishlist()

    def create_widgets(self):
        self.label = tk.Label(self, text="Liste de souhaits", font=("Arial", 14))
        self.label.pack(pady=10)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_filter)
        self.search_entry = tk.Entry(self, textvariable=self.search_var, width=30)
        self.search_entry.pack(pady=5)
        self.search_entry.insert(0, "Rechercher...")
        self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.delete(0, END) if self.search_entry.get() == "Rechercher..." else None)

        self.listbox = Listbox(self, width=40, height=10)
        self.listbox.pack(pady=10)

        self.add_btn = tk.Button(self, text="Ajouter un mot-clé", command=self.add_keyword)
        self.add_btn.pack(pady=5)

        self.remove_btn = tk.Button(self, text="Supprimer le mot-clé sélectionné", command=self.remove_keyword)
        self.remove_btn.pack(pady=5)

        self.promo_btn = tk.Button(self, text="Rechercher des promotions", command=self.search_promos)
        self.promo_btn.pack(pady=20)

    def update_filter(self, *args):
        search = self.search_var.get().lower()
        self.listbox.delete(0, END)
        if os.path.exists(WISHLIST_FILE):
            with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
                wishlist = json.load(f)
            for kw in wishlist:
                if search in kw.lower():
                    self.listbox.insert(END, kw)

    def load_wishlist(self):
        self.update_filter()

    def add_keyword(self):
        keyword = simpledialog.askstring("Ajouter", "Entrez le mot-clé à ajouter :")
        if keyword:
            if os.path.exists(WISHLIST_FILE):
                with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
                    wishlist = json.load(f)
            else:
                wishlist = []
            if keyword not in wishlist:
                wishlist.append(keyword)
                with open(WISHLIST_FILE, 'w', encoding='utf-8') as f:
                    json.dump(wishlist, f, ensure_ascii=False, indent=2)
                self.load_wishlist()
            else:
                messagebox.showinfo("Info", "Mot-clé déjà présent.")

    def remove_keyword(self):
        selected = self.listbox.curselection()
        if selected:
            idx = selected[0]
            keyword = self.listbox.get(idx)
            with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
                wishlist = json.load(f)
            wishlist.remove(keyword)
            with open(WISHLIST_FILE, 'w', encoding='utf-8') as f:
                json.dump(wishlist, f, ensure_ascii=False, indent=2)
            self.load_wishlist()
        else:
            messagebox.showinfo("Info", "Sélectionnez un mot-clé à supprimer.")

    def search_promos(self):
        # Lance le script promo_detector.py
        subprocess.Popen([os.sys.executable, PROMO_DETECTOR])
        messagebox.showinfo("Recherche", "Recherche de promotions lancée !")

if __name__ == "__main__":
    app = DealTrackApp()
    app.mainloop()
