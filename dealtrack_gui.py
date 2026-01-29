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
        self.migrate_wishlist()
        self.listbox = None  # Défini plus tard
        self.create_widgets()
        self.after(0, self.load_wishlist)

    def migrate_wishlist(self):
        # Migration automatique de la structure wishlist (str -> dict)
        if os.path.exists(WISHLIST_FILE):
            with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
                wishlist = json.load(f)
            if wishlist and isinstance(wishlist[0], str):
                wishlist = [{"keyword": k, "category": "Jeu"} for k in wishlist]
                with open(WISHLIST_FILE, 'w', encoding='utf-8') as f2:
                    json.dump(wishlist, f2, ensure_ascii=False, indent=2)

    def create_widgets(self):
        self.categories = ["Jeu", "Console", "Matériel"]
        self.label = tk.Label(self, text="Liste de souhaits", font=("Arial", 14))
        self.label.pack(pady=10)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self, textvariable=self.search_var, width=30)
        self.search_entry.pack(pady=5)
        self.search_entry.insert(0, "Rechercher...")
        self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.delete(0, END) if self.search_entry.get() == "Rechercher..." else None)

        self.listbox = Listbox(self, width=50, height=10)
        self.listbox.pack(pady=10)

        self.add_btn = tk.Button(self, text="Ajouter un mot-clé", command=self.add_keyword)
        self.add_btn.pack(pady=5)

        self.remove_btn = tk.Button(self, text="Supprimer le mot-clé sélectionné", command=self.remove_keyword)
        self.remove_btn.pack(pady=5)

        self.promo_btn = tk.Button(self, text="Rechercher des promotions", command=self.search_promos)
        self.promo_btn.pack(pady=20)

        # Connecte la recherche après la création de la listbox
        self.search_var.trace("w", self.update_filter)

    def update_filter(self, *args):
        if not self.listbox:
            return
        search = self.search_var.get().lower()
        self.listbox.delete(0, END)
        if os.path.exists(WISHLIST_FILE):
            with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
                wishlist = json.load(f)
            # Migration auto si ancienne structure
            if wishlist and isinstance(wishlist[0], str):
                wishlist = [{"keyword": k, "category": "Jeu"} for k in wishlist]
                with open(WISHLIST_FILE, 'w', encoding='utf-8') as f2:
                    json.dump(wishlist, f2, ensure_ascii=False, indent=2)
            for item in wishlist:
                if search in item["keyword"].lower():
                    self.listbox.insert(END, f"{item['keyword']} [{item['category']}]" )

    def load_wishlist(self):
        self.update_filter()

    def add_keyword(self):
        keyword = simpledialog.askstring("Ajouter", "Entrez le mot-clé à ajouter :")
        if not keyword:
            return
        cat_win = tk.Toplevel(self)
        cat_win.title("Choisir une catégorie")
        tk.Label(cat_win, text="Catégorie :").pack(pady=5)
        cat_var = tk.StringVar(value=self.categories[0])
        for cat in self.categories:
            tk.Radiobutton(cat_win, text=cat, variable=cat_var, value=cat).pack(anchor="w")
        def on_ok():
            category = cat_var.get()
            cat_win.destroy()
            if os.path.exists(WISHLIST_FILE):
                with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
                    wishlist = json.load(f)
            else:
                wishlist = []
            # Migration auto si ancienne structure
            if wishlist and isinstance(wishlist[0], str):
                wishlist = [{"keyword": k, "category": "Jeu"} for k in wishlist]
            if any(item["keyword"].lower() == keyword.lower() for item in wishlist):
                messagebox.showinfo("Info", "Mot-clé déjà présent.")
                return
            wishlist.append({"keyword": keyword, "category": category})
            with open(WISHLIST_FILE, 'w', encoding='utf-8') as f:
                json.dump(wishlist, f, ensure_ascii=False, indent=2)
            self.load_wishlist()
        tk.Button(cat_win, text="OK", command=on_ok).pack(pady=10)

    def remove_keyword(self):
        selected = self.listbox.curselection()
        if selected:
            idx = selected[0]
            display = self.listbox.get(idx)
            keyword = display.split(' [')[0]
            with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
                wishlist = json.load(f)
            # Migration auto si ancienne structure
            if wishlist and isinstance(wishlist[0], str):
                wishlist = [{"keyword": k, "category": "Jeu"} for k in wishlist]
            wishlist = [item for item in wishlist if item["keyword"] != keyword]
            with open(WISHLIST_FILE, 'w', encoding='utf-8') as f:
                json.dump(wishlist, f, ensure_ascii=False, indent=2)
            self.load_wishlist()
        else:
            messagebox.showinfo("Info", "Sélectionnez un mot-clé à supprimer.")

    def search_promos(self):
        selected = self.listbox.curselection()
        if selected:
            idx = selected[0]
            display = self.listbox.get(idx)
            keyword = display.split(' [')[0]
            # Charger la wishlist pour retrouver la catégorie exacte
            if os.path.exists(WISHLIST_FILE):
                with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
                    wishlist = json.load(f)
                for item in wishlist:
                    if item["keyword"] == keyword:
                        # Appel direct à promo_detector pour ce mot-clé
                        import importlib.util
                        import sys
                        spec = importlib.util.spec_from_file_location("promo_detector", PROMO_DETECTOR)
                        promo_detector = importlib.util.module_from_spec(spec)
                        sys.modules["promo_detector"] = promo_detector
                        spec.loader.exec_module(promo_detector)
                        promo_detector.check_promos_for_keyword(item)
                        messagebox.showinfo("Recherche", f"Recherche de promotions lancée pour : {keyword}")
                        return
        # Sinon, comportement par défaut (tous les mots-clés)
        subprocess.Popen([os.sys.executable, PROMO_DETECTOR])
        messagebox.showinfo("Recherche", "Recherche de promotions lancée pour toute la liste !")

if __name__ == "__main__":
    app = DealTrackApp()
    app.mainloop()
