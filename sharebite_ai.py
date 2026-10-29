"""
ShareBite AI - Smart Food Redistribution Network
Python-only desktop prototype for Python IDLE.
Uses tkinter + JSON local storage. No third-party packages required.

Run:
1. Save this file as sharebite_ai.py
2. Open it in Python IDLE
3. Press F5 (Run > Run Module)

Demo note:
This is a local desktop prototype, not a deployed web app. Demo data is fictional.
"""

import json
import os
import uuid
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

APP_TITLE = "ShareBite AI"
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sharebite_data.json")

BG = "#F3F7F2"
CARD = "#FFFFFF"
GREEN = "#176B45"
GREEN_DARK = "#104B32"
GREEN_LIGHT = "#E4F3E9"
ORANGE = "#F4A340"
TEXT = "#1D2B24"
MUTED = "#6B7B72"
RED = "#C74634"
BORDER = "#DDE7DF"

STATUSES = ["Available", "Reserved", "Pickup Scheduled", "Collected", "Delivered", "Expired", "Rejected"]
CATEGORIES = ["Cooked Meals", "Bakery", "Fruits & Vegetables", "Packaged Food", "Dairy", "Other"]
ROLES = ["Donor", "NGO", "Volunteer", "Admin"]

SAMPLE_DATA = {
    "donations": [
        {
            "id": "SB-1001", "food": "Vegetable Rice Meals", "category": "Cooked Meals",
            "quantity": 18, "unit": "kg", "donor": "Green Leaf College Mess",
            "location": "Tambaram, Chennai", "deadline": (datetime.now()+timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
            "diet": "Vegetarian", "allergens": "May contain nuts", "storage": "Keep warm",
            "status": "Available", "claimed_by": "", "volunteer": "", "notes": "Freshly prepared lunch"
        },
        {
            "id": "SB-1002", "food": "Assorted Bread & Buns", "category": "Bakery",
            "quantity": 8, "unit": "kg", "donor": "Sunrise Bakery",
            "location": "Chromepet, Chennai", "deadline": (datetime.now()+timedelta(hours=9)).strftime("%Y-%m-%d %H:%M"),
            "diet": "Vegetarian", "allergens": "Wheat, gluten", "storage": "Room temperature",
            "status": "Available", "claimed_by": "", "volunteer": "", "notes": "Packed in sealed bags"
        },
        {
            "id": "SB-1003", "food": "Fresh Bananas", "category": "Fruits & Vegetables",
            "quantity": 12, "unit": "kg", "donor": "Daily Basket Market",
            "location": "Selaiyur, Chennai", "deadline": (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
            "diet": "Vegan", "allergens": "None reported", "storage": "Cool, dry place",
            "status": "Reserved", "claimed_by": "Hope Hands NGO", "volunteer": "", "notes": "Ripe and ready to distribute"
        },
        {
            "id": "SB-1004", "food": "Packaged Snack Boxes", "category": "Packaged Food",
            "quantity": 6, "unit": "kg", "donor": "Campus Cafe",
            "location": "Pallavaram, Chennai", "deadline": (datetime.now()+timedelta(hours=12)).strftime("%Y-%m-%d %H:%M"),
            "diet": "Vegetarian", "allergens": "Check individual labels", "storage": "As labelled",
            "status": "Delivered", "claimed_by": "Care Bridge Foundation", "volunteer": "Arun (Demo)", "notes": "Unopened packages"
        }
    ],
    "ngos": [
        {"name": "Hope Hands NGO", "location": "Selaiyur, Chennai", "capacity": 30, "categories": ["Cooked Meals", "Fruits & Vegetables", "Bakery"], "pickup": True, "storage": ["Keep warm", "Room temperature", "Cool, dry place"]},
        {"name": "Care Bridge Foundation", "location": "Tambaram, Chennai", "capacity": 45, "categories": ["Cooked Meals", "Packaged Food", "Bakery", "Fruits & Vegetables"], "pickup": True, "storage": ["Keep warm", "Room temperature", "As labelled", "Cool, dry place"]},
        {"name": "Community Food Bank", "location": "Chromepet, Chennai", "capacity": 20, "categories": ["Bakery", "Packaged Food", "Dairy"], "pickup": False, "storage": ["Room temperature", "As labelled"]},
        {"name": "Helping Hearts Centre", "location": "Pallavaram, Chennai", "capacity": 25, "categories": ["Cooked Meals", "Fruits & Vegetables", "Packaged Food"], "pickup": True, "storage": ["Keep warm", "Cool, dry place", "As labelled"]}
    ],
    "volunteers": [
        {"name": "Arun (Demo)", "area": "Tambaram, Chennai", "available": True},
        {"name": "Meena (Demo)", "area": "Chromepet, Chennai", "available": True},
        {"name": "Kavin (Demo)", "area": "Pallavaram, Chennai", "available": True}
    ],
    "activity": []
}


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key in SAMPLE_DATA:
                data.setdefault(key, [])
            return data
        except (json.JSONDecodeError, OSError):
            pass
    data = json.loads(json.dumps(SAMPLE_DATA))
    save_data(data)
    return data


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def parse_deadline(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M")
    except (TypeError, ValueError):
        return None


class ShareBiteApp:
    def __init__(self, root):
        self.root = root
        self.data = load_data()
        self.role = tk.StringVar(value="Admin")
        self.page = "Dashboard"
        self.search_var = tk.StringVar()
        self.status_filter = tk.StringVar(value="All")
        self.root.title(APP_TITLE + " | Smart Food Redistribution")
        self.root.geometry("1240x790")
        self.root.minsize(1000, 680)
        self.root.configure(bg=BG)
        self.configure_styles()
        self.build_shell()
        self.show_page("Dashboard")

    def configure_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", background=CARD, fieldbackground=CARD, foreground=TEXT,
                        rowheight=31, borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=GREEN_LIGHT, foreground=GREEN_DARK,
                        font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", "#CDE8D6")], foreground=[("selected", TEXT)])
        style.configure("TCombobox", padding=5)

    def build_shell(self):
        self.sidebar = tk.Frame(self.root, bg=GREEN_DARK, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=GREEN_DARK)
        brand.pack(fill="x", padx=18, pady=(24, 26))
        tk.Label(brand, text="🍃 ShareBite", bg=GREEN_DARK, fg="white",
                 font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Label(brand, text="AI FOOD REDISTRIBUTION", bg=GREEN_DARK, fg="#B8D9C4",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(5, 0))

        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", "▦  Dashboard"),
            ("Donations", "♧  Live Donations"),
            ("Create Donation", "＋  Create Donation"),
            ("SmartMatch", "✦  SmartMatch AI"),
            ("Deliveries", "➜  Pickup & Delivery"),
            ("NGOs", "♡  NGO Directory"),
            ("Impact", "◉  Impact Analytics"),
            ("Admin", "⚙  Admin & Reports"),
        ]
        for page, label in nav_items:
            btn = tk.Button(self.sidebar, text=label, anchor="w", relief="flat",
                            bg=GREEN_DARK, fg="#EAF5EE", activebackground=GREEN,
                            activeforeground="white", font=("Segoe UI", 10, "bold"),
                            padx=18, pady=12, cursor="hand2",
                            command=lambda p=page: self.show_page(p))
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[page] = btn

        bottom = tk.Frame(self.sidebar, bg=GREEN_DARK)
        bottom.pack(side="bottom", fill="x", padx=18, pady=18)
        tk.Label(bottom, text="DEMO MODE • LOCAL DATA", bg=GREEN_DARK, fg="#B8D9C4",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(bottom, text="Prototype for portfolio use", bg=GREEN_DARK, fg="#B8D9C4",
                 font=("Segoe UI", 8)).pack(anchor="w", pady=(4, 0))

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)
        self.topbar = tk.Frame(self.main, bg=CARD, height=68, highlightbackground=BORDER, highlightthickness=1)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)
        self.page_title = tk.Label(self.topbar, text="Dashboard", bg=CARD, fg=TEXT,
                                   font=("Segoe UI", 17, "bold"))
        self.page_title.pack(side="left", padx=26)
        right = tk.Frame(self.topbar, bg=CARD)
        right.pack(side="right", padx=22)
        tk.Label(right, text="Demo role:", bg=CARD, fg=MUTED, font=("Segoe UI", 9)).pack(side="left", padx=(0, 8))
        role_box = ttk.Combobox(right, textvariable=self.role, values=ROLES, width=12, state="readonly")
        role_box.pack(side="left")
        role_box.bind("<<ComboboxSelected>>", lambda _e: self.refresh_page())
        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(fill="both", expand=True, padx=24, pady=22)

    def clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def show_page(self, page):
        self.page = page
        self.page_title.config(text=page)
        for name, btn in self.nav_buttons.items():
            btn.configure(bg=GREEN if name == page else GREEN_DARK)
        self.clear_content()
        methods = {
            "Dashboard": self.page_dashboard,
            "Donations": self.page_donations,
            "Create Donation": self.page_create_donation,
            "SmartMatch": self.page_smartmatch,
            "Deliveries": self.page_deliveries,
            "NGOs": self.page_ngos,
            "Impact": self.page_impact,
            "Admin": self.page_admin
        }
        methods.get(page, self.page_dashboard)()

    def refresh_page(self):
        self.show_page(self.page)

    def card(self, parent, title, value, subtitle, accent=GREEN):
        frame = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        tk.Frame(frame, bg=accent, height=4).pack(fill="x")
        inner = tk.Frame(frame, bg=CARD)
        inner.pack(fill="both", expand=True, padx=16, pady=13)
        tk.Label(inner, text=title.upper(), bg=CARD, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(inner, text=str(value), bg=CARD, fg=TEXT,
                 font=("Segoe UI", 24, "bold")).pack(anchor="w", pady=(5, 1))
        tk.Label(inner, text=subtitle, bg=CARD, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w")
        return frame

    def section_title(self, parent, title, subtitle=None):
        tk.Label(parent, text=title, bg=BG, fg=TEXT, font=("Segoe UI", 13, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(parent, text=subtitle, bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(3, 10))
        else:
            tk.Frame(parent, bg=BG, height=10).pack()

    def make_table(self, parent, columns, rows, height=9):
        frame = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=height)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=max(90, int(750 / len(columns))), anchor="w")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scroll.pack(side="right", fill="y", padx=(0, 5), pady=8)
        for row in rows:
            tree.insert("", "end", values=row)
        return frame, tree

    def log(self, message):
        self.data["activity"].insert(0, {"time": now_text(), "message": message})
        self.data["activity"] = self.data["activity"][:100]
        save_data(self.data)

    def page_dashboard(self):
        self.clear_content()
        donations = self.data["donations"]
        delivered = [d for d in donations if d["status"] == "Delivered"]
        available = [d for d in donations if d["status"] == "Available"]
        reserved = [d for d in donations if d["status"] in ("Reserved", "Pickup Scheduled", "Collected")]
        total_kg = sum(float(d.get("quantity", 0)) for d in delivered)
        meals = int(total_kg * 4)
        tk.Label(self.content, text="Good to see you! 👋", bg=BG, fg=TEXT,
                 font=("Segoe UI", 21, "bold")).pack(anchor="w")
        tk.Label(self.content, text="Here's what's happening across your food redistribution network.",
                 bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 18))

        stats = tk.Frame(self.content, bg=BG)
        stats.pack(fill="x")
        cards = [
            ("Total donations", len(donations), "All recorded donations", GREEN),
            ("Available now", len(available), "Ready to be claimed", ORANGE),
            ("In progress", len(reserved), "Reserved or being delivered", "#3A86B7"),
            ("Food redistributed", f"{total_kg:.1f} kg", f"~{meals} estimated meal portions", "#7A65B5")
        ]
        for i, item in enumerate(cards):
            c = self.card(stats, *item)
            c.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 10, 0))
            stats.grid_columnconfigure(i, weight=1)

        body = tk.Frame(self.content, bg=BG)
        body.pack(fill="both", expand=True, pady=(22, 0))
        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        right = tk.Frame(body, bg=BG, width=270)
        right.pack(side="right", fill="y")
        self.section_title(left, "Recent donations", "Latest activity across your network")
        rows = []
        for d in sorted(donations, key=lambda x: x.get("id", ""), reverse=True)[:7]:
            rows.append((d["id"], d["food"], f'{d["quantity"]} {d["unit"]}', d["donor"], d["status"]))
        table, _ = self.make_table(left, ("ID", "Food", "Quantity", "Donor", "Status"), rows, 8)
        table.pack(fill="both", expand=True)

        self.section_title(right, "Quick actions")
        for label, page in [("＋  Create a donation", "Create Donation"), ("♧  Browse donations", "Donations"),
                            ("✦  Find NGO matches", "SmartMatch"), ("➜  Track deliveries", "Deliveries")]:
            tk.Button(right, text=label, anchor="w", command=lambda p=page: self.show_page(p),
                      bg=CARD, fg=GREEN_DARK, activebackground=GREEN_LIGHT, relief="flat",
                      highlightbackground=BORDER, highlightthickness=1, padx=14, pady=12,
                      font=("Segoe UI", 10, "bold"), cursor="hand2").pack(fill="x", pady=5)
        note = tk.Frame(right, bg=GREEN_LIGHT)
        note.pack(fill="x", pady=(15, 0))
        tk.Label(note, text="🌱  Impact note", bg=GREEN_LIGHT, fg=GREEN_DARK,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        tk.Label(note, text="Every safe, successful redistribution can help reduce avoidable food waste. Meal counts are estimates.",
                 bg=GREEN_LIGHT, fg=GREEN_DARK, wraplength=220, justify="left",
                 font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(0, 12))

    def page_create_donation(self):
        self.clear_content()
        self.section_title(self.content, "Create a food donation", "Add accurate details so suitable recipients can collect food safely.")
        outer = tk.Frame(self.content, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        outer.pack(fill="both", expand=True)
        form = tk.Frame(outer, bg=CARD)
        form.pack(fill="both", expand=True, padx=24, pady=18)

        fields = {}
        labels = [
            ("Food name *", "food", ""),
            ("Donor / organization *", "donor", ""),
            ("Pickup location *", "location", "Tambaram, Chennai"),
            ("Quantity (kg) *", "quantity", "5"),
            ("Deadline (YYYY-MM-DD HH:MM) *", "deadline", (datetime.now()+timedelta(hours=6)).strftime("%Y-%m-%d %H:%M")),
            ("Allergens / label notes", "allergens", "Not specified"),
            ("Storage requirements", "storage", "Room temperature"),
            ("Additional notes", "notes", "")
        ]
        for idx, (label, key, default) in enumerate(labels):
            r, c = divmod(idx, 2)
            block = tk.Frame(form, bg=CARD)
            block.grid(row=r, column=c, sticky="ew", padx=(0 if c == 0 else 18, 0), pady=8)
            tk.Label(block, text=label, bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 5))
            ent = tk.Entry(block, font=("Segoe UI", 10), relief="solid", bd=1,
                           highlightthickness=1, highlightbackground=BORDER)
            ent.pack(fill="x", ipady=7)
            ent.insert(0, default)
            fields[key] = ent
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        row = tk.Frame(form, bg=CARD)
        row.grid(row=4, column=0, columnspan=2, sticky="ew", pady=8)
        tk.Label(row, text="Food category", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 10))
        category = ttk.Combobox(row, values=CATEGORIES, state="readonly", width=24)
        category.set(CATEGORIES[0])
        category.pack(side="left", padx=(0, 20))
        tk.Label(row, text="Diet type", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 10))
        diet = ttk.Combobox(row, values=["Vegetarian", "Vegan", "Non-vegetarian", "Mixed"], state="readonly", width=20)
        diet.set("Vegetarian")
        diet.pack(side="left")
        tk.Label(form, text="* Required fields. Confirm food handling and safe-use deadline before offering a donation.",
                 bg=CARD, fg=MUTED, font=("Segoe UI", 9)).grid(row=5, column=0, columnspan=2, sticky="w", pady=(8, 14))

        def submit():
            food = fields["food"].get().strip()
            donor = fields["donor"].get().strip()
            location = fields["location"].get().strip()
            deadline = fields["deadline"].get().strip()
            try:
                qty = float(fields["quantity"].get().strip())
                if qty <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid quantity", "Enter a quantity greater than zero.")
                return
            if not food or not donor or not location:
                messagebox.showerror("Missing information", "Please fill in food name, donor, and pickup location.")
                return
            parsed = parse_deadline(deadline)
            if not parsed:
                messagebox.showerror("Invalid deadline", "Use this format: YYYY-MM-DD HH:MM")
                return
            if parsed <= datetime.now():
                if not messagebox.askyesno("Deadline is in the past", "This deadline is not in the future. Add it anyway for demonstration?"):
                    return
            donation = {
                "id": "SB-" + uuid.uuid4().hex[:6].upper(),
                "food": food, "category": category.get(), "quantity": qty, "unit": "kg",
                "donor": donor, "location": location, "deadline": deadline, "diet": diet.get(),
                "allergens": fields["allergens"].get().strip() or "Not specified",
                "storage": fields["storage"].get().strip() or "Not specified",
                "status": "Available", "claimed_by": "", "volunteer": "",
                "notes": fields["notes"].get().strip()
            }
            self.data["donations"].append(donation)
            self.log(f'{donor} added donation "{food}" ({qty:g} kg).')
            messagebox.showinfo("Donation added", f"Donation {donation['id']} is now available.")
            self.show_page("Donations")

        buttons = tk.Frame(form, bg=CARD)
        buttons.grid(row=6, column=0, columnspan=2, sticky="w", pady=8)
        tk.Button(buttons, text="Publish donation", command=submit, bg=GREEN, fg="white",
                  activebackground=GREEN_DARK, activeforeground="white", relief="flat",
                  font=("Segoe UI", 10, "bold"), padx=22, pady=10, cursor="hand2").pack(side="left")
        tk.Button(buttons, text="Cancel", command=lambda: self.show_page("Dashboard"), bg="#EEF2EF",
                  fg=TEXT, relief="flat", padx=22, pady=10, cursor="hand2").pack(side="left", padx=10)

    def page_donations(self):
        self.clear_content()
        self.section_title(self.content, "Live donations", "Search and manage donations. Sample records are fictional demo data.")
        controls = tk.Frame(self.content, bg=BG)
        controls.pack(fill="x", pady=(0, 12))
        tk.Label(controls, text="Search", bg=BG, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(side="left")
        search = tk.Entry(controls, textvariable=self.search_var, width=30, font=("Segoe UI", 10), relief="solid", bd=1)
        search.pack(side="left", padx=8, ipady=5)
        tk.Label(controls, text="Status", bg=BG, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(16, 5))
        status = ttk.Combobox(controls, textvariable=self.status_filter, values=["All"] + STATUSES,
                              state="readonly", width=18)
        status.pack(side="left")
        table_holder = tk.Frame(self.content, bg=BG)
        table_holder.pack(fill="both", expand=True)
        actionbar = tk.Frame(self.content, bg=BG)
        actionbar.pack(fill="x", pady=(12, 0))
        selected = {"id": None}

        def render():
            for child in table_holder.winfo_children():
                child.destroy()
            query = self.search_var.get().lower().strip()
            chosen_status = self.status_filter.get()
            rows = []
            for d in self.data["donations"]:
                haystack = " ".join(str(d.get(k, "")) for k in ("id", "food", "donor", "location", "category")).lower()
                if query and query not in haystack:
                    continue
                if chosen_status != "All" and d["status"] != chosen_status:
                    continue
                rows.append((d["id"], d["food"], d["category"], f'{d["quantity"]:g} kg', d["donor"], d["location"], d["deadline"], d["status"]))
            frame, tree = self.make_table(table_holder, ("ID", "Food", "Category", "Qty", "Donor", "Location", "Deadline", "Status"), rows, 12)
            frame.pack(fill="both", expand=True)
            def on_select(_event=None):
                picked = tree.selection()
                selected["id"] = tree.item(picked[0], "values")[0] if picked else None
            tree.bind("<<TreeviewSelect>>", on_select)
            selected["tree"] = tree

        def get_selected():
            if not selected.get("id"):
                messagebox.showwarning("Select a donation", "Select a donation row first.")
                return None
            return next((d for d in self.data["donations"] if d["id"] == selected["id"]), None)

        def claim():
            d = get_selected()
            if not d:
                return
            if d["status"] != "Available":
                messagebox.showwarning("Not available", "Only Available donations can be claimed.")
                return
            if self.role.get() not in ("NGO", "Admin"):
                messagebox.showwarning("Role required", "Switch the demo role to NGO or Admin to claim a donation.")
                return
            ngo_names = [n["name"] for n in self.data["ngos"]]
            chooser = tk.Toplevel(self.root)
            chooser.title("Claim donation")
            chooser.configure(bg=BG)
            chooser.geometry("390x190")
            chooser.transient(self.root)
            chooser.grab_set()
            tk.Label(chooser, text="Select receiving NGO", bg=BG, fg=TEXT,
                     font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=22, pady=(22, 8))
            cb = ttk.Combobox(chooser, values=ngo_names, state="readonly", width=36)
            cb.pack(padx=22, anchor="w")
            if ngo_names:
                cb.current(0)
            def confirm():
                name = cb.get()
                if not name:
                    return
                # In this single-user local prototype, the check and status update happen together.
                if d["status"] != "Available":
                    messagebox.showerror("Already claimed", "This donation is no longer available.")
                    chooser.destroy()
                    return
                d["status"] = "Reserved"
                d["claimed_by"] = name
                self.log(f'{name} claimed "{d["food"]}" ({d["id"]}).')
                save_data(self.data)
                chooser.destroy()
                render()
                messagebox.showinfo("Donation reserved", f"{d['food']} reserved for {name}.")
            tk.Button(chooser, text="Confirm claim", command=confirm, bg=GREEN, fg="white",
                      relief="flat", padx=16, pady=8).pack(anchor="w", padx=22, pady=16)

        def change_status():
            d = get_selected()
            if not d:
                return
            chooser = tk.Toplevel(self.root)
            chooser.title("Update donation status")
            chooser.configure(bg=BG)
            chooser.geometry("370x180")
            tk.Label(chooser, text="New status", bg=BG, fg=TEXT,
                     font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20, pady=(20, 8))
            cb = ttk.Combobox(chooser, values=STATUSES, state="readonly", width=26)
            cb.set(d["status"])
            cb.pack(anchor="w", padx=20)
            def apply():
                old = d["status"]
                d["status"] = cb.get()
                self.log(f'Donation {d["id"]} status changed: {old} → {d["status"]}.')
                save_data(self.data)
                chooser.destroy()
                render()
            tk.Button(chooser, text="Save status", command=apply, bg=GREEN, fg="white",
                      relief="flat", padx=16, pady=8).pack(anchor="w", padx=20, pady=15)

        tk.Button(actionbar, text="Claim selected", command=claim, bg=GREEN, fg="white",
                  activebackground=GREEN_DARK, activeforeground="white", relief="flat",
                  font=("Segoe UI", 9, "bold"), padx=15, pady=9).pack(side="left")
        tk.Button(actionbar, text="Update status", command=change_status, bg=CARD, fg=TEXT,
                  relief="flat", highlightbackground=BORDER, highlightthickness=1,
                  padx=15, pady=9).pack(side="left", padx=8)
        tk.Button(actionbar, text="Refresh", command=render, bg=CARD, fg=TEXT,
                  relief="flat", highlightbackground=BORDER, highlightthickness=1,
                  padx=15, pady=9).pack(side="left")
        search.bind("<KeyRelease>", lambda _e: render())
        status.bind("<<ComboboxSelected>>", lambda _e: render())
        render()

    def match_score(self, donation, ngo):
        # Transparent demo heuristic; not a trained AI model.
        score = 0
        reasons = []
        dloc = donation.get("location", "").lower()
        nloc = ngo.get("location", "").lower()
        if dloc and nloc:
            dcity = dloc.split(",")[0].strip()
            ncity = nloc.split(",")[0].strip()
            if dcity == ncity:
                score += 35
                reasons.append("same locality")
            elif any(token in dloc for token in nloc.split(",")[0].split()) or any(token in nloc for token in dcity.split()):
                score += 22
                reasons.append("nearby area")
            else:
                score += 10
                reasons.append("location differs")
        if donation.get("category") in ngo.get("categories", []):
            score += 25
            reasons.append("accepts this food category")
        else:
            reasons.append("category may not fit")
        capacity = float(ngo.get("capacity", 0) or 0)
        qty = float(donation.get("quantity", 0) or 0)
        if capacity >= qty:
            score += 20
            reasons.append("capacity is sufficient")
        elif capacity > 0:
            score += int(20 * capacity / max(qty, 1))
            reasons.append("capacity may be limited")
        if ngo.get("pickup"):
            score += 10
            reasons.append("pickup available")
        if donation.get("storage") in ngo.get("storage", []):
            score += 10
            reasons.append("storage requirement supported")
        return min(100, score), reasons

    def page_smartmatch(self):
        self.clear_content()
        self.section_title(self.content, "✦ SmartMatch Engine", "Transparent rule-based recommendations. Scores are decision support, not a guarantee.")
        available = [d for d in self.data["donations"] if d["status"] == "Available"]
        if not available:
            tk.Label(self.content, text="No available donations to match. Add a donation or change a status.",
                     bg=BG, fg=MUTED, font=("Segoe UI", 11)).pack(anchor="w", pady=20)
            return
        choose_frame = tk.Frame(self.content, bg=BG)
        choose_frame.pack(fill="x", pady=(0, 16))
        tk.Label(choose_frame, text="Choose donation", bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold")).pack(side="left")
        labels = [f'{d["id"]} — {d["food"]} ({d["quantity"]:g} kg)' for d in available]
        cb = ttk.Combobox(choose_frame, values=labels, state="readonly", width=55)
        cb.current(0)
        cb.pack(side="left", padx=10)
        results = tk.Frame(self.content, bg=BG)
        results.pack(fill="both", expand=True)

        def render(_event=None):
            for child in results.winfo_children():
                child.destroy()
            index = cb.current()
            if index < 0:
                return
            donation = available[index]
            tk.Label(results, text=f'Matching recipients for: {donation["food"]}',
                     bg=BG, fg=TEXT, font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 5))
            tk.Label(results, text=f'{donation["quantity"]:g} kg • {donation["category"]} • {donation["location"]} • deadline {donation["deadline"]}',
                     bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 14))
            scored = [(self.match_score(donation, ngo), ngo) for ngo in self.data["ngos"]]
            scored.sort(key=lambda item: item[0][0], reverse=True)
            for (score, reasons), ngo in scored:
                card = tk.Frame(results, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
                card.pack(fill="x", pady=5)
                top = tk.Frame(card, bg=CARD)
                top.pack(fill="x", padx=16, pady=(12, 4))
                tk.Label(top, text=ngo["name"], bg=CARD, fg=TEXT, font=("Segoe UI", 12, "bold")).pack(side="left")
                tk.Label(top, text=f"{score}/100 match", bg=GREEN_LIGHT if score >= 70 else "#FFF0D8",
                         fg=GREEN_DARK if score >= 70 else "#86520C", font=("Segoe UI", 10, "bold"),
                         padx=10, pady=4).pack(side="right")
                tk.Label(card, text=f'{ngo["location"]}  •  Capacity: {ngo["capacity"]} kg  •  Pickup: {"Yes" if ngo["pickup"] else "No"}',
                         bg=CARD, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=16)
                tk.Label(card, text="Why: " + ", ".join(reasons), bg=CARD, fg=TEXT,
                         font=("Segoe UI", 9), wraplength=850, justify="left").pack(anchor="w", padx=16, pady=(5, 12))
        cb.bind("<<ComboboxSelected>>", render)
        render()
        tk.Label(self.content, text="Scoring: locality (35), category compatibility (25), capacity (20), pickup (10), storage compatibility (10).",
                 bg=BG, fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w", pady=(10, 0))

    def page_deliveries(self):
        self.clear_content()
        self.section_title(self.content, "Pickup & delivery tracking", "Track each donation from reservation to delivery.")
        rows = []
        for d in self.data["donations"]:
            if d["status"] in ("Reserved", "Pickup Scheduled", "Collected", "Delivered"):
                rows.append((d["id"], d["food"], d.get("claimed_by") or "Not assigned",
                             d.get("volunteer") or "Unassigned", d["location"], d["status"], d["deadline"]))
        table, tree = self.make_table(self.content, ("ID", "Food", "Receiving NGO", "Volunteer", "Pickup location", "Status", "Deadline"), rows, 12)
        table.pack(fill="both", expand=True)
        actions = tk.Frame(self.content, bg=BG)
        actions.pack(fill="x", pady=12)

        def selected_donation():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select a delivery", "Select a row first.")
                return None
            did = tree.item(selected[0], "values")[0]
            return next((d for d in self.data["donations"] if d["id"] == did), None)

        def assign_volunteer():
            d = selected_donation()
            if not d:
                return
            if self.role.get() not in ("Admin", "Volunteer"):
                messagebox.showwarning("Role required", "Switch to Admin or Volunteer demo role.")
                return
            win = tk.Toplevel(self.root)
            win.title("Assign volunteer")
            win.configure(bg=BG)
            win.geometry("380x190")
            tk.Label(win, text="Assign volunteer to " + d["id"], bg=BG, fg=TEXT,
                     font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20, pady=(20, 10))
            names = [v["name"] for v in self.data["volunteers"]]
            cb = ttk.Combobox(win, values=names, state="readonly", width=32)
            cb.pack(anchor="w", padx=20)
            if names:
                cb.current(0)
            def save():
                if cb.get():
                    d["volunteer"] = cb.get()
                    if d["status"] == "Reserved":
                        d["status"] = "Pickup Scheduled"
                    self.log(f'{cb.get()} assigned to delivery {d["id"]}.')
                    save_data(self.data)
                    win.destroy()
                    self.show_page("Deliveries")
            tk.Button(win, text="Assign", command=save, bg=GREEN, fg="white", relief="flat",
                      padx=18, pady=8).pack(anchor="w", padx=20, pady=14)

        def advance_status():
            d = selected_donation()
            if not d:
                return
            transitions = {
                "Reserved": "Pickup Scheduled",
                "Pickup Scheduled": "Collected",
                "Collected": "Delivered"
            }
            new = transitions.get(d["status"])
            if not new:
                messagebox.showinfo("No next step", "This donation is already delivered or has no delivery transition.")
                return
            if new == "Delivered" and not d.get("volunteer"):
                if not messagebox.askyesno("No volunteer assigned", "No volunteer is assigned. Mark as delivered anyway for this demo?"):
                    return
            old = d["status"]
            d["status"] = new
            self.log(f'Delivery {d["id"]} advanced: {old} → {new}.')
            save_data(self.data)
            self.show_page("Deliveries")
        tk.Button(actions, text="Assign volunteer", command=assign_volunteer, bg=GREEN, fg="white",
                  relief="flat", padx=16, pady=9).pack(side="left")
        tk.Button(actions, text="Advance delivery status", command=advance_status, bg=CARD, fg=TEXT,
                  relief="flat", highlightbackground=BORDER, highlightthickness=1,
                  padx=16, pady=9).pack(side="left", padx=8)

    def page_ngos(self):
        self.clear_content()
        self.section_title(self.content, "NGO directory", "Fictional sample organizations for local demonstration.")
        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="both", expand=True)
        for i, ngo in enumerate(self.data["ngos"]):
            r, c = divmod(i, 2)
            box = tk.Frame(cards, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
            box.grid(row=r, column=c, sticky="nsew", padx=(0 if c == 0 else 10, 0), pady=6)
            tk.Label(box, text="♡  " + ngo["name"], bg=CARD, fg=GREEN_DARK,
                     font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=16, pady=(14, 6))
            tk.Label(box, text="⌖  " + ngo["location"], bg=CARD, fg=MUTED,
                     font=("Segoe UI", 9)).pack(anchor="w", padx=16)
            tk.Label(box, text=f'Capacity: {ngo["capacity"]} kg  •  Pickup: {"Available" if ngo["pickup"] else "Not available"}',
                     bg=CARD, fg=TEXT, font=("Segoe UI", 10)).pack(anchor="w", padx=16, pady=8)
            tk.Label(box, text="Accepted: " + ", ".join(ngo["categories"]), bg=CARD, fg=MUTED,
                     wraplength=430, justify="left", font=("Segoe UI", 9)).pack(anchor="w", padx=16, pady=(0, 14))
            cards.grid_columnconfigure(c, weight=1)
        tk.Label(self.content, text="For a real deployment, verify NGO identities and obtain consent before publishing their contact or location details.",
                 bg=BG, fg=MUTED, font=("Segoe UI", 9), wraplength=850, justify="left").pack(anchor="w", pady=12)

    def page_impact(self):
        self.clear_content()
        self.section_title(self.content, "Impact analytics", "Transparent estimates calculated from delivered donation records.")
        delivered = [d for d in self.data["donations"] if d["status"] == "Delivered"]
        kg = sum(float(d.get("quantity", 0)) for d in delivered)
        meals = int(kg * 4)  # Assumption: 4 estimated portions per kg, adjustable for the demo.
        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x")
        for i, item in enumerate([
            ("Food delivered", f"{kg:.1f} kg", "Sum of delivered donation quantities", GREEN),
            ("Estimated portions", f"{meals:,}", "Assumption: 4 portions per kg", ORANGE),
            ("Completed donations", len(delivered), "Status = Delivered", "#3A86B7"),
            ("Active donors", len(set(d["donor"] for d in self.data["donations"])), "Donors with recorded donations", "#7A65B5")
        ]):
            c = self.card(cards, *item)
            c.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 10, 0))
            cards.grid_columnconfigure(i, weight=1)
        self.section_title(self.content, "Donation status breakdown")
        status_counts = {s: sum(1 for d in self.data["donations"] if d["status"] == s) for s in STATUSES}
        max_count = max(status_counts.values()) if status_counts else 1
        chart = tk.Frame(self.content, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        chart.pack(fill="x", pady=(0, 18))
        for status, count in status_counts.items():
            if count == 0:
                continue
            line = tk.Frame(chart, bg=CARD)
            line.pack(fill="x", padx=18, pady=6)
            tk.Label(line, text=status, bg=CARD, fg=TEXT, width=20, anchor="w",
                     font=("Segoe UI", 9)).pack(side="left")
            bar_bg = tk.Frame(line, bg="#E8EFEA", height=17)
            bar_bg.pack(side="left", fill="x", expand=True, padx=8)
            bar = tk.Frame(bar_bg, bg=GREEN if status == "Delivered" else ORANGE, height=17,
                           width=max(5, int(420 * count / max_count)))
            bar.pack(side="left")
            tk.Label(line, text=str(count), bg=CARD, fg=TEXT, width=4,
                     font=("Segoe UI", 9, "bold")).pack(side="right")
        note = tk.Frame(self.content, bg=GREEN_LIGHT)
        note.pack(fill="x")
        tk.Label(note, text="How estimates work", bg=GREEN_LIGHT, fg=GREEN_DARK,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=14, pady=(12, 4))
        tk.Label(note, text="Meal portions = delivered kilograms × 4. This is a configurable demonstration assumption, not a verified nutritional or environmental measurement. No emissions avoided value is shown because no validated methodology is configured.",
                 bg=GREEN_LIGHT, fg=GREEN_DARK, wraplength=950, justify="left",
                 font=("Segoe UI", 9)).pack(anchor="w", padx=14, pady=(0, 12))

    def page_admin(self):
        self.clear_content()
        self.section_title(self.content, "Admin & reports", "Review activity and export the current demo records.")
        summary = tk.Frame(self.content, bg=BG)
        summary.pack(fill="x", pady=(0, 18))
        for i, item in enumerate([
            ("Registered NGOs", len(self.data["ngos"]), "Fictional demo directory", GREEN),
            ("Volunteers", len(self.data["volunteers"]), "Demo volunteer records", ORANGE),
            ("Activity events", len(self.data["activity"]), "Local audit-style history", "#3A86B7")
        ]):
            c = self.card(summary, *item)
            c.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 10, 0))
            summary.grid_columnconfigure(i, weight=1)
        self.section_title(self.content, "Recent activity")
        rows = [(a.get("time", ""), a.get("message", "")) for a in self.data["activity"][:15]]
        if not rows:
            rows = [("—", "No actions recorded yet. Create a donation or update a delivery to see activity here.")]
        table, _ = self.make_table(self.content, ("Time", "Activity"), rows, 10)
        table.pack(fill="both", expand=True)
        actions = tk.Frame(self.content, bg=BG)
        actions.pack(fill="x", pady=12)

        def export_json():
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sharebite_export.json")
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Export complete", "Exported data to:\n" + path)
            except OSError as exc:
                messagebox.showerror("Export failed", str(exc))

        def reset_demo():
            if messagebox.askyesno("Reset demo data", "This replaces current local data with the original sample records. Continue?"):
                self.data = json.loads(json.dumps(SAMPLE_DATA))
                save_data(self.data)
                self.log("Demo data reset.")
                self.show_page("Admin")
        tk.Button(actions, text="Export JSON data", command=export_json, bg=GREEN, fg="white",
                  relief="flat", padx=16, pady=9).pack(side="left")
        tk.Button(actions, text="Reset demo data", command=reset_demo, bg=CARD, fg=RED,
                  relief="flat", highlightbackground=BORDER, highlightthickness=1,
                  padx=16, pady=9).pack(side="left", padx=8)

    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    ShareBiteApp(root).run()


if __name__ == "__main__":
    main()
