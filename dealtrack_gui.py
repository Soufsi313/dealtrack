# dealtrack_gui.py

import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, END, ttk
import os
import json
import subprocess
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'wishlist'))
import wishlist_manager

WISHLIST_FILE = os.path.join(os.path.dirname(__file__), 'wishlist', 'wishlist.json')
PROMO_DETECTOR = os.path.join(os.path.dirname(__file__), 'promotions', 'promo_detector.py')

class DealTrackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DealTrack")
        self.geometry("400x550")
        self.resizable(False, False)
        self.migrate_wishlist()
        self.listbox = None  # Défini plus tard
        self.current_user = "default"
        self.create_widgets()
        self.after(0, self.load_wishlist)

    def migrate_wishlist(self):
        # Migration automatique de la structure wishlist (str -> dict, puis dict multi-utilisateur)
        if os.path.exists(WISHLIST_FILE):
            with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
                wishlist = json.load(f)
            # Si c'est une liste (ancienne structure), migrer vers dict multi-utilisateur
            if isinstance(wishlist, list):
                # Migration str -> dict si besoin
                if wishlist and isinstance(wishlist[0], str):
                    wishlist = [{"keyword": k, "category": "Jeu"} for k in wishlist]
                # Migration vers structure multi-utilisateur
                wishlist = {"default": wishlist}
                with open(WISHLIST_FILE, 'w', encoding='utf-8') as f2:
                    json.dump(wishlist, f2, ensure_ascii=False, indent=2)

    def create_widgets(self):
        # Chargement dynamique des catégories
        self.load_categories()
        self.label = tk.Label(self, text="Liste de souhaits", font=("Arial", 14))
        self.label.pack(pady=10)

        # Menu déroulant utilisateur
        user_frame = tk.Frame(self)
        user_frame.pack(pady=5)
        tk.Label(user_frame, text="Utilisateur :").pack(side="left")
        self.user_var = tk.StringVar(value=self.current_user)
        self.user_menu = ttk.Combobox(user_frame, textvariable=self.user_var, state="readonly")
        self.refresh_user_list()
        self.user_menu.pack(side="left", padx=5)
        self.user_menu.bind("<<ComboboxSelected>>", self.on_user_change)
        self.add_user_btn = tk.Button(user_frame, text="+", command=self.add_user, width=2)
        self.add_user_btn.pack(side="left")

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
        self.promo_btn.pack(pady=10)

        self.notif_history_btn = tk.Button(self, text="Historique des notifications", command=self.show_notif_history)
        self.notif_history_btn.pack(pady=5)

        # Boutons supplémentaires
        self.filters_btn = tk.Button(self, text="Filtres avancés", command=self.show_filters)
        self.filters_btn.pack(pady=5)

        self.favorites_btn = tk.Button(self, text="Favoris", command=self.show_favorites)
        self.favorites_btn.pack(pady=5)

        # Bouton gestion des catégories placé après la wishlist et les actions
        self.cat_manage_btn = tk.Button(self, text="Gérer les catégories", command=self.manage_categories)
        self.cat_manage_btn.pack(pady=15)
    def show_filters(self):
        win = tk.Toplevel(self)
        win.title("Filtres avancés")
        win.geometry("350x220")
        # Chargement config
        filters_path = os.path.join(os.path.dirname(__file__), 'promotions', 'filters_config.json')
        if os.path.exists(filters_path):
            with open(filters_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {"max_price": None, "exclude_keywords": []}
        # Prix max
        tk.Label(win, text="Prix maximum (€) :").pack()
        price_var = tk.StringVar(value=str(config.get("max_price") or ""))
        price_entry = tk.Entry(win, textvariable=price_var)
        price_entry.pack()
        # Exclusions
        tk.Label(win, text="Mots à exclure (séparés par des virgules) :").pack()
        excl_var = tk.StringVar(value=", ".join(config.get("exclude_keywords", [])))
        excl_entry = tk.Entry(win, textvariable=excl_var, width=40)
        excl_entry.pack()
        def save_filters():
            try:
                max_price = float(price_var.get()) if price_var.get().strip() else None
            except ValueError:
                messagebox.showerror("Erreur", "Le prix maximum doit être un nombre.")
                return
            excl = [w.strip() for w in excl_var.get().split(",") if w.strip()]
            config = {"max_price": max_price, "exclude_keywords": excl}
            with open(filters_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Succès", "Filtres enregistrés !")
            win.destroy()
        tk.Button(win, text="Enregistrer", command=save_filters).pack(pady=10)

    def show_favorites(self):
        win = tk.Toplevel(self)
        win.title("Favoris")
        win.geometry("500x300")
        fav_path = os.path.join(os.path.dirname(__file__), 'promotions', 'favorites.json')
        if os.path.exists(fav_path):
            with open(fav_path, 'r', encoding='utf-8') as f:
                favs = json.load(f)
        else:
            favs = {}
        user_favs = favs.get(self.current_user, [])
        listbox = Listbox(win, width=70, height=15)
        listbox.pack(padx=10, pady=10)
        if user_favs:
            for fav in reversed(user_favs):
                line = f"{fav.get('timestamp','')} | {fav.get('site','')} | {fav.get('keyword','')} | {fav.get('url','')}"
                listbox.insert(END, line)
        else:
            listbox.insert(END, "Aucun favori enregistré pour cet utilisateur.")

    def load_categories(self):
        cat_path = os.path.join(os.path.dirname(__file__), 'wishlist', 'categories_manager.py')
        import importlib.util
        import sys
        spec = importlib.util.spec_from_file_location("categories_manager", cat_path)
        categories_manager = importlib.util.module_from_spec(spec)
        sys.modules["categories_manager"] = categories_manager
        spec.loader.exec_module(categories_manager)
        self.categories = categories_manager.load_categories()

    def manage_categories(self):
        win = tk.Toplevel(self)
        win.title("Gestion des catégories")
        win.geometry("350x300")
        listbox = Listbox(win, width=30, height=10)
        listbox.pack(pady=10)
        for cat in self.categories:
            listbox.insert(END, cat)

        def add_cat():
            new_cat = simpledialog.askstring("Ajouter une catégorie", "Nom de la nouvelle catégorie :", parent=win)
            if new_cat and new_cat not in self.categories:
                self.categories.append(new_cat)
                listbox.insert(END, new_cat)
                self.save_categories_and_refresh()

        def remove_cat():
            sel = listbox.curselection()
            if sel:
                idx = sel[0]
                cat = listbox.get(idx)
                if cat in self.categories:
                    self.categories.remove(cat)
                    listbox.delete(idx)
                    self.save_categories_and_refresh()

        add_btn = tk.Button(win, text="Ajouter", command=add_cat)
        add_btn.pack(side="left", padx=10, pady=5)
        del_btn = tk.Button(win, text="Supprimer", command=remove_cat)
        del_btn.pack(side="right", padx=10, pady=5)

    def save_categories_and_refresh(self):
        cat_path = os.path.join(os.path.dirname(__file__), 'wishlist', 'categories_manager.py')
        import importlib.util
        import sys
        spec = importlib.util.spec_from_file_location("categories_manager", cat_path)
        categories_manager = importlib.util.module_from_spec(spec)
        sys.modules["categories_manager"] = categories_manager
        spec.loader.exec_module(categories_manager)
        categories_manager.save_categories(self.categories)
        # Recharge les catégories pour la prochaine utilisation
        self.load_categories()

        # Menu déroulant utilisateur
        user_frame = tk.Frame(self)
        user_frame.pack(pady=5)
        tk.Label(user_frame, text="Utilisateur :").pack(side="left")
        self.user_var = tk.StringVar(value=self.current_user)
        self.user_menu = ttk.Combobox(user_frame, textvariable=self.user_var, state="readonly")
        self.refresh_user_list()
        self.user_menu.pack(side="left", padx=5)
        self.user_menu.bind("<<ComboboxSelected>>", self.on_user_change)
        self.add_user_btn = tk.Button(user_frame, text="+", command=self.add_user, width=2)
        self.add_user_btn.pack(side="left")

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
        self.promo_btn.pack(pady=10)

        self.notif_history_btn = tk.Button(self, text="Historique des notifications", command=self.show_notif_history)
        self.notif_history_btn.pack(pady=5)
    def show_notif_history(self):
        import importlib.util
        import sys
        notif_history_path = os.path.join(os.path.dirname(__file__), 'notifications', 'notification_history.py')
        spec = importlib.util.spec_from_file_location("notification_history", notif_history_path)
        notif_history = importlib.util.module_from_spec(spec)
        sys.modules["notification_history"] = notif_history
        spec.loader.exec_module(notif_history)
        history = notif_history.get_notifications_history(self.current_user)
        win = tk.Toplevel(self)
        win.title(f"Historique des notifications - {self.current_user}")
        win.geometry("500x300")
        listbox = Listbox(win, width=70, height=15)
        listbox.pack(padx=10, pady=10)
        if history:
            for notif in reversed(history):
                line = f"{notif['timestamp']} | {notif['title']} | {notif['message']}"
                if notif.get('url'):
                    line += f" | {notif['url']}"
                listbox.insert(END, line)
        else:
            listbox.insert(END, "Aucune notification enregistrée pour cet utilisateur.")

        # Connecte la recherche après la création de la listbox
        self.search_var.trace("w", self.update_filter)

    def refresh_user_list(self):
        data = wishlist_manager.load_wishlist_all()
        users = list(data.keys()) if data else ["default"]
        if self.current_user not in users:
            users.append(self.current_user)
        self.user_menu['values'] = users
        self.user_var.set(self.current_user)

    def on_user_change(self, event=None):
        self.current_user = self.user_var.get()
        self.load_wishlist()

    def add_user(self):
        new_user = simpledialog.askstring("Nouvel utilisateur", "Nom du nouvel utilisateur :")
        if new_user:
            data = wishlist_manager.load_wishlist_all()
            if new_user in data:
                messagebox.showinfo("Info", "Cet utilisateur existe déjà.")
            else:
                data[new_user] = []
                with open(WISHLIST_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self.current_user = new_user
                self.refresh_user_list()
                self.load_wishlist()

    def update_filter(self, *args):
        if not self.listbox:
            return
        search = self.search_var.get().lower()
        self.listbox.delete(0, END)
        wishlist = wishlist_manager.load_wishlist(self.current_user)
        for item in wishlist:
            if search in item["keyword"].lower():
                self.listbox.insert(END, f"{item['keyword']} [{item['category']}]" )

    def load_wishlist(self):
        self.update_filter()

    def add_keyword(self):
        keyword = simpledialog.askstring("Ajouter", "Entrez le mot-clé à ajouter :")
        if not keyword:
            return
        self.load_categories()  # Recharge les catégories à jour
        cat_win = tk.Toplevel(self)
        cat_win.title("Choisir une catégorie")
        tk.Label(cat_win, text="Catégorie :").pack(pady=5)
        cat_var = tk.StringVar(value=self.categories[0] if self.categories else "")
        for cat in self.categories:
            tk.Radiobutton(cat_win, text=cat, variable=cat_var, value=cat).pack(anchor="w")
        def on_ok():
            category = cat_var.get()
            cat_win.destroy()
            wishlist = wishlist_manager.load_wishlist(self.current_user)
            if any(item["keyword"].lower() == keyword.lower() for item in wishlist):
                messagebox.showinfo("Info", "Mot-clé déjà présent.")
                return
            wishlist.append({"keyword": keyword, "category": category})
            wishlist_manager.save_wishlist(wishlist, self.current_user)
            self.load_wishlist()
        tk.Button(cat_win, text="OK", command=on_ok).pack(pady=10)

    def remove_keyword(self):
        selected = self.listbox.curselection()
        if selected:
            idx = selected[0]
            display = self.listbox.get(idx)
            keyword = display.split(' [')[0]
            wishlist = wishlist_manager.load_wishlist(self.current_user)
            wishlist = [item for item in wishlist if item["keyword"] != keyword]
            wishlist_manager.save_wishlist(wishlist, self.current_user)
            self.load_wishlist()
        else:
            messagebox.showinfo("Info", "Sélectionnez un mot-clé à supprimer.")

    def search_promos(self):
        selected = self.listbox.curselection()
        wishlist = wishlist_manager.load_wishlist(self.current_user)
        if selected:
            idx = selected[0]
            display = self.listbox.get(idx)
            keyword = display.split(' [')[0]
            for item in wishlist:
                if item["keyword"] == keyword:
                    import importlib.util
                    import sys
                    spec = importlib.util.spec_from_file_location("promo_detector", PROMO_DETECTOR)
                    promo_detector = importlib.util.module_from_spec(spec)
                    sys.modules["promo_detector"] = promo_detector
                    spec.loader.exec_module(promo_detector)
                    promo_detector.check_promos_for_keyword(item)
                    messagebox.showinfo("Recherche", f"Recherche de promotions lancée pour : {keyword}")
                    return
        # Sinon, comportement par défaut (tous les mots-clés de l'utilisateur)
        # On peut passer la wishlist de l'utilisateur à promo_detector si besoin
        subprocess.Popen([os.sys.executable, PROMO_DETECTOR])
        messagebox.showinfo("Recherche", "Recherche de promotions lancée pour toute la liste de l'utilisateur !")

if __name__ == "__main__":
    app = DealTrackApp()
    app.mainloop()
