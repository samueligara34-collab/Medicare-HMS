"""
MediCare HMS — Role-based Hospital Management System
=====================================================
Requires: Python 3.8+  (tkinter is in the standard library)
Run:      python hospital_management_gui.py

Roles & their dedicated dashboards:
  Administrator  — full system access, user management, analytics
  Doctor         — patient list, diagnosis, prescriptions, ward rounds
  Nurse          — vital signs, nursing notes, ward tasks checklist
  HRIO   — patient registration, appointments, search
  Pharmacist     — prescription queue, drug inventory, dispensing log
  Resident       — progress notes, prescriptions, ward rounds
  Lab Tech       — test results entry, history
  Radiology      — imaging study uploads, history
  RT/PT/Diet     — specialized therapy and nutrition logs
  Social/Case    — social assessments and discharge planning
"""

import json, os, random
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta

# ══════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════
DATA_FILE = "hospital_data.json"
USERS_FILE = "hospital_users.json"
VITALS_FILE = "hospital_vitals.json"
PRESCRIPTIONS_FILE = "hospital_rx.json"
INVENTORY_FILE = "hospital_inventory.json"
APPOINTMENTS_FILE = "hospital_appointments.json"
TASKS_FILE = "hospital_tasks.json"
LAB_RESULTS_FILE = "hospital_lab.json"
IMAGING_FILE = "hospital_imaging.json"
THERAPY_FILE = "hospital_therapy.json"
DIET_FILE = "hospital_diet.json"
SOCIAL_FILE = "hospital_social.json"
MORGUE_FILE = "hospital_morgue.json"

ADMISSION_FEE = 2000
DAILY_BED_RATE = 1500

DEFAULT_USERS = {
    "admin": {"password": "admin123", "role": "Administrator", "full_name": "Admin User"},
    "doctor": {"password": "doc456", "role": "Doctor", "full_name": "Dr. Kamau"},
    "nurse": {"password": "nurse789", "role": "Nurse", "full_name": "Nurse Achieng"},
    "reception": {"password": "rec000", "role": "HRIO", "full_name": "Faith Mwangi"},
    "pharma": {"password": "pharm111", "role": "Pharmacist", "full_name": "Peter Otieno"},
    "morgue": {"password": "morgue123", "role": "Morgue Attendant", "full_name": "John Doe"},
}
ROLES = ["Administrator", "Doctor", "Nurse", "HRIO", "Pharmacist",
         "Resident/Intern", "Lab Technician", "Radiologic Technologist",
         "Respiratory Therapist", "Physical Therapist", "Dietitian",
         "Social Worker", "Case Manager", "Morgue Attendant"]

# ── Palette ────────────────────────────────────────────────────
C_BG = "#F8FAFC"
C_SIDEBAR = "#1E293B"
C_SIDEBAR_H = "#334155"
C_SIDEBAR_T = "#0F172A"
C_CARD = "#FFFFFF"
C_BORDER = "#E2E8F0"
C_TEXT = "#1E293B"
C_MUTED = "#64748B"
C_ACCENT = "#2563EB"
C_DANGER = "#EF4444"
C_SUCCESS = "#10B981"
C_WARN = "#F59E0B"
C_ROW_ALT = "#F1F5F9"
C_HEADER_BG = "#F8FAFC"
C_GOLD = "#B8860B"
C_BLUE = "#1565C0"
C_PURPLE = "#6A1B9A"

ROLE_COLOURS = {
    "Administrator": "#0C5C47",
    "Doctor": "#1565C0",
    "Nurse": "#7B1FA2",
    "HRIO": "#E65100",
    "Pharmacist": "#2E7D32",
    "Resident/Intern": "#0277BD",
    "Lab Technician": "#C62828",
    "Radiologic Technologist": "#283593",
    "Respiratory Therapist": "#00695C",
    "Physical Therapist": "#6A1B9A",
    "Dietitian": "#827717",
    "Social Worker": "#EF6C00",
    "Case Manager": "#37474F",
    "Morgue Attendant": "#2C3E50",
}

# ── Fonts ──────────────────────────────────────────────────────
FONT_H1 = ("Georgia", 15, "bold")
FONT_H2 = ("Georgia", 12, "bold")
FONT_H3 = ("Georgia", 10, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_TINY = ("Segoe UI", 8)
FONT_NUM_S = ("Georgia", 16, "bold")


# ══════════════════════════════════════════════════════════════
#  DATA HELPERS
# ══════════════════════════════════════════════════════════════
def _load(path, default=None):
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            pass
    return default if default is not None else {}


def _save(path, data):
    with open(path, "w") as f: json.dump(data, f, indent=4)


def load_users():     return _load(USERS_FILE) or dict(DEFAULT_USERS)


def save_users(u):    _save(USERS_FILE, u)


def load_data():      return _load(DATA_FILE, {})


def save_data(p):     _save(DATA_FILE, p)


def load_vitals():    return _load(VITALS_FILE, {})


def save_vitals(v):   _save(VITALS_FILE, v)


def load_rx():        return _load(PRESCRIPTIONS_FILE, [])


def save_rx(r):       _save(PRESCRIPTIONS_FILE, r)


def load_inventory(): return _load(INVENTORY_FILE, _default_inventory())


def save_inventory(i): _save(INVENTORY_FILE, i)


def load_appointments(): return _load(APPOINTMENTS_FILE, [])


def save_appointments(a): _save(APPOINTMENTS_FILE, a)


def load_tasks():     return _load(TASKS_FILE, [])


def save_tasks(t):    _save(TASKS_FILE, t)


def load_lab():      return _load(LAB_RESULTS_FILE, [])


def save_lab(l):     _save(LAB_RESULTS_FILE, l)


def load_imaging():  return _load(IMAGING_FILE, [])


def save_imaging(i): _save(IMAGING_FILE, i)


def load_therapy():  return _load(THERAPY_FILE, [])


def save_therapy(t): _save(THERAPY_FILE, t)


def load_diet():     return _load(DIET_FILE, [])


def save_diet(d):    _save(DIET_FILE, d)


def load_social():   return _load(SOCIAL_FILE, [])


def save_social(s):  _save(SOCIAL_FILE, s)


def load_morgue():    return _load(MORGUE_FILE, [])


def save_morgue(m):   _save(MORGUE_FILE, m)


def _default_wards():
    return [
        {"name": "General Ward A", "capacity": 20, "type": "General"},
        {"name": "General Ward B", "capacity": 20, "type": "General"},
        {"name": "ICU", "capacity": 5, "type": "Critical Care"},
        {"name": "Maternity Ward", "capacity": 15, "type": "Maternity"},
        {"name": "Paediatric Ward", "capacity": 15, "type": "Paediatric"},
        {"name": "Isolation Ward", "capacity": 8, "type": "Infectious"},
    ]


def _default_inventory():
    return [
        {"drug": "Amoxicillin 500mg", "category": "Antibiotic", "stock": 240, "unit": "Capsules", "reorder": 50},
        {"drug": "Paracetamol 500mg", "category": "Analgesic", "stock": 500, "unit": "Tablets", "reorder": 100},
        {"drug": "Metformin 500mg", "category": "Antidiabetic", "stock": 180, "unit": "Tablets", "reorder": 60},
        {"drug": "Atorvastatin 20mg", "category": "Statin", "stock": 120, "unit": "Tablets", "reorder": 40},
        {"drug": "Omeprazole 20mg", "category": "Antacid", "stock": 90, "unit": "Capsules", "reorder": 30},
        {"drug": "IV Normal Saline", "category": "IV Fluid", "stock": 45, "unit": "Bags", "reorder": 20},
        {"drug": "Morphine 10mg", "category": "Opioid", "stock": 30, "unit": "Vials", "reorder": 10},
        {"drug": "Salbutamol Inhaler", "category": "Bronchodilator", "stock": 60, "unit": "Inhalers", "reorder": 15},
    ]


def next_pid(patients):
    if not patients: return "P001"
    nums = [int(k[1:]) for k in patients if k.startswith("P") and k[1:].isdigit()]
    return f"P{(max(nums) + 1):03d}" if nums else "P001"


def calc_bill(p):
    return ADMISSION_FEE + DAILY_BED_RATE * p.get("days_admitted", 0) + p.get("treatment_cost", 0)


def fmt_kes(n): return f"KES {n:,.2f}"


def now_str():  return datetime.now().strftime("%Y-%m-%d %H:%M")


def today_str(): return date.today().isoformat()


# ══════════════════════════════════════════════════════════════
#  WIDGET HELPERS  (module-level, shared by all app classes)
# ══════════════════════════════════════════════════════════════
def card_frame(parent, **kw):
    return tk.Frame(parent, bg=C_CARD, relief="flat",
                    highlightbackground=C_BORDER, highlightthickness=1, **kw)


def label(parent, text, font=FONT_BODY, fg=C_TEXT, bg=None, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg,
                    bg=bg or parent["bg"], **kw)


def btn(parent, text, command, bg=C_ACCENT, fg="white",
        padx=16, pady=8, font=FONT_BODY):
    b = tk.Button(parent, text=text, command=command,
                  bg=bg, fg=fg, font=font, relief="flat",
                  padx=padx, pady=pady, cursor="hand2",
                  activebackground=C_SIDEBAR_H, activeforeground="white", bd=0)
    b.bind("<Enter>", lambda e: b.config(bg=C_SIDEBAR_H))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


def entry(parent, textvariable=None, width=28, show=None):
    e = tk.Entry(parent, textvariable=textvariable, width=width,
                 font=FONT_BODY, relief="flat", bg="#F8FAFC", fg=C_TEXT,
                 highlightbackground=C_BORDER, highlightthickness=1, show=show or "")
    e.configure(insertbackground=C_TEXT)
    return e


def combobox(parent, textvariable, values, width=26):
    ttk.Style().configure("HMS.TCombobox", fieldbackground="#EBF5F0",
                          background="#EBF5F0", foreground=C_TEXT)
    return ttk.Combobox(parent, textvariable=textvariable, values=values,
                        width=width, state="readonly",
                        style="HMS.TCombobox", font=FONT_BODY)


def separator(parent, pady=6):
    tk.Frame(parent, bg=C_BORDER, height=1).pack(fill="x", pady=pady)


def toast(parent_win, msg, kind="success"):
    colours = {"success": (C_SUCCESS, "#D1FAE5"), "error": (C_DANGER, "#FEE2E2"), "warn": (C_WARN, "#FEF3C7")}
    fg, bg = colours.get(kind, colours["success"])
    top = tk.Toplevel(parent_win)
    top.overrideredirect(True);
    top.attributes("-topmost", True);
    top.configure(bg=bg)
    pw, ph = parent_win.winfo_width(), parent_win.winfo_height()
    px, py = parent_win.winfo_rootx(), parent_win.winfo_rooty()
    tk.Label(top, text=f"  {msg}  ", font=FONT_BODY, fg=fg, bg=bg, pady=8).pack()
    tw = max(len(msg) * 7 + 24, 220)
    top.geometry(f"{tw}x36+{px + pw // 2 - tw // 2}+{py + ph - 70}")
    top.after(2800, top.destroy)


def build_tree(parent, columns, col_widths=None, height=14):
    style = ttk.Style()
    style.configure("HMS.Treeview", background=C_CARD, foreground=C_TEXT,
                    rowheight=26, fieldbackground=C_CARD, font=FONT_BODY)
    style.configure("HMS.Treeview.Heading", background=C_HEADER_BG,
                    foreground=C_ACCENT, font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("HMS.Treeview",
              background=[("selected", C_ACCENT)], foreground=[("selected", "white")])
    frame = tk.Frame(parent, bg=C_CARD)
    tree = ttk.Treeview(frame, columns=columns, show="headings",
                        height=height, style="HMS.Treeview", selectmode="browse")
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y");
    tree.pack(side="left", fill="both", expand=True)
    for i, col in enumerate(columns):
        w = col_widths[i] if col_widths else 120
        tree.heading(col, text=col);
        tree.column(col, width=w, anchor="w", minwidth=40)
    tree.tag_configure("alt", background=C_ROW_ALT)
    return frame, tree


def kpi_card(parent, label_text, value, icon, colour):
    card = tk.Frame(parent, bg=C_CARD, relief="flat",
                    highlightbackground=C_BORDER, highlightthickness=1)
    card.pack(side="left", expand=True, fill="x", padx=(0, 10), ipady=12, ipadx=8)
    # Accent bar on the left
    tk.Frame(card, bg=colour, width=4).pack(side="left", fill="y")
    inner = tk.Frame(card, bg=C_CARD);
    inner.pack(side="left", padx=12, fill="both", expand=True)

    top = tk.Frame(inner, bg=C_CARD);
    top.pack(fill="x", pady=(2, 0))
    tk.Label(top, text=icon, font=("Segoe UI", 16), bg=C_CARD, fg=colour).pack(side="left")

    tk.Label(inner, text=value, font=("Georgia", 18, "bold"), fg=C_TEXT, bg=C_CARD).pack(anchor="w", pady=(2, 0))
    tk.Label(inner, text=label_text.upper(), font=("Segoe UI", 7, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")


# ══════════════════════════════════════════════════════════════
#  LOGIN
# ══════════════════════════════════════════════════════════════
class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root;
        self.on_success = on_success
        self.users = load_users()
        self.root.title("MediCare HMS — Login")
        self.root.configure(bg=C_BG);
        self.root.resizable(False, False)
        w, h = 440, 560
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")
        self._build()

    def _build(self):
        outer = tk.Frame(self.root, bg=C_BG);
        outer.pack(fill="both", expand=True)
        tk.Frame(outer, bg=C_ACCENT, height=6).pack(fill="x")
        lf = tk.Frame(outer, bg=C_BG);
        lf.pack(pady=(32, 0))
        box = tk.Frame(lf, bg=C_ACCENT, width=68, height=68)
        box.pack_propagate(False);
        box.pack()
        tk.Label(box, text="✚", font=("Segoe UI", 30, "bold"),
                 fg="white", bg=C_ACCENT).place(relx=.5, rely=.5, anchor="center")
        label(outer, "MediCare HMS", font=("Georgia", 19, "bold"), fg=C_ACCENT, bg=C_BG).pack(pady=(12, 2))
        label(outer, "Hospital Management System", font=FONT_SMALL, fg=C_MUTED, bg=C_BG).pack()

        card = card_frame(outer);
        card.pack(padx=44, pady=20, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=26, pady=22, fill="x")

        self.err_var = tk.StringVar()
        self.err_lbl = tk.Label(inner, textvariable=self.err_var, font=FONT_SMALL,
                                fg=C_DANGER, bg="#FEE2E2", wraplength=280, pady=5)

        for lt, attr, show in [("Username", "user_var", None), ("Password", "pass_var", "•")]:
            tk.Label(inner, text=lt, font=("Segoe UI", 9, "bold"),
                     fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            setattr(self, attr, tk.StringVar())
            e = entry(inner, textvariable=getattr(self, attr), width=34, show=show)
            e.pack(fill="x", pady=(2, 12))
            if attr == "user_var":
                self._ue = e
            else:
                e.bind("<Return>", lambda ev: self._login())

        btn(inner, "  Sign In  →", self._login, pady=9).pack(fill="x")
        separator(inner, pady=12)
        link_row = tk.Frame(inner, bg=C_CARD);
        link_row.pack()
        tk.Label(link_row, text="New staff?", font=FONT_SMALL,
                 fg=C_MUTED, bg=C_CARD).pack(side="left")
        sl = tk.Label(link_row, text="  Create an account",
                      font=("Segoe UI", 9, "underline"), fg=C_ACCENT,
                      bg=C_CARD, cursor="hand2")
        sl.pack(side="left");
        sl.bind("<Button-1>", lambda e: SignupWindow(self.root, self.users))
        hint = "Logins: admin/admin123 · doctor/doc456 · nurse/nurse789\n reception/rec000 · pharma/pharm111 · (New roles available in signup)"
        label(inner, hint, font=("Segoe UI", 8), fg=C_MUTED, bg=C_CARD,
              justify="center").pack(pady=(10, 0))
        self._ue.focus()

    def _login(self):
        u = self.user_var.get().strip().lower()
        p = self.pass_var.get()
        self.users = load_users()
        if u in self.users and self.users[u]["password"] == p:
            self.on_success(u, self.users[u]["role"])
        else:
            self.err_var.set("  ✘  Invalid username or password.")
            self.err_lbl.pack(fill="x", pady=(0, 10));
            self.pass_var.set("")


# ══════════════════════════════════════════════════════════════
#  SIGN-UP
# ══════════════════════════════════════════════════════════════
class SignupWindow:
    def __init__(self, parent, users):
        self.parent = parent;
        self.users = users
        self.win = tk.Toplevel(parent)
        self.win.title("Create Account");
        self.win.configure(bg=C_BG)
        self.win.resizable(False, False)
        w, h = 420, 500
        sw, sh = parent.winfo_screenwidth(), parent.winfo_screenheight()
        self.win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")
        self.win.grab_set();
        self._build()

    def _build(self):
        tk.Frame(self.win, bg=C_ACCENT, height=6).pack(fill="x")
        label(self.win, "Create Staff Account", font=("Georgia", 15, "bold"),
              fg=C_ACCENT, bg=C_BG).pack(pady=(28, 4))
        card = card_frame(self.win);
        card.pack(padx=38, pady=16, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=22, pady=20, fill="x")
        self.fn_v = tk.StringVar();
        self.user_v = tk.StringVar()
        self.role_v = tk.StringVar(value=ROLES[2])
        self.pass_v = tk.StringVar();
        self.conf_v = tk.StringVar()
        self.err_var = tk.StringVar()
        self.err_lbl = tk.Label(inner, textvariable=self.err_var, font=FONT_SMALL,
                                fg=C_DANGER, bg="#FEE2E2", wraplength=300, pady=4)
        for lt, var, show in [("Full Name", self.fn_v, None), ("Username", self.user_v, None)]:
            tk.Label(inner, text=lt, font=("Segoe UI", 9, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            entry(inner, textvariable=var, width=34, show=show).pack(fill="x", pady=(2, 10))
        tk.Label(inner, text="Role", font=("Segoe UI", 9, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, self.role_v, ROLES, width=32).pack(anchor="w", pady=(2, 10))
        for lt, var in [("Password", self.pass_v), ("Confirm Password", self.conf_v)]:
            tk.Label(inner, text=lt, font=("Segoe UI", 9, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            entry(inner, textvariable=var, width=34, show="•").pack(fill="x", pady=(2, 10))
        btn(inner, "  Create Account", self._signup, pady=8).pack(fill="x")

    def _signup(self):
        fn = self.fn_v.get().strip();
        user = self.user_v.get().strip().lower()
        role = self.role_v.get();
        pw = self.pass_v.get();
        conf = self.conf_v.get()
        if not fn or not user: self._err("Name and username required."); return
        if len(user) < 3: self._err("Username ≥ 3 chars."); return
        if user in self.users: self._err(f"'{user}' already taken."); return
        if len(pw) < 6: self._err("Password ≥ 6 chars."); return
        if pw != conf: self._err("Passwords don't match."); return
        self.users[user] = {"password": pw, "role": role, "full_name": fn}
        save_users(self.users);
        self.win.destroy()
        toast(self.parent, f"Account created — sign in as '{user}'")

    def _err(self, msg):
        self.err_var.set(f"  ✘  {msg}");
        self.err_lbl.pack(fill="x", pady=(0, 8))


# ══════════════════════════════════════════════════════════════
#  BASE APP  — shared layout scaffold + common panels
# ══════════════════════════════════════════════════════════════
class BaseApp:
    # Subclasses set these class attributes:
    ROLE_LABEL = "User"
    SIDEBAR_SECTIONS = []  # [("SECTION", [("key","▦ Label"), ...]), ...]
    PANEL_MAP = {}  # {"key": "_method_name"}
    DEFAULT_PANEL = "dashboard"

    def __init__(self, root, username, role):
        self.root = root
        self.username = username
        self.role = role
        self.patients = load_data()
        self.accent = ROLE_COLOURS.get(role, C_ACCENT)

        self.root.title(f"MediCare HMS — {role} Dashboard")
        self.root.configure(bg=C_BG)
        w, h = 1160, 730
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")
        root.minsize(980, 600)
        root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._build_layout()
        self.show_panel(self.DEFAULT_PANEL)

    # ── Shell ──────────────────────────────────────────────────
    def _build_layout(self):
        topbar = tk.Frame(self.root, bg=self.accent, height=54)
        topbar.pack(fill="x");
        topbar.pack_propagate(False)
        tk.Label(topbar, text="✚  MediCare HMS",
                 font=("Georgia", 13, "bold"), fg="white",
                 bg=self.accent).pack(side="left", padx=20)
        # role badge
        badge_bg = self._darken(self.accent)
        tk.Label(topbar, text=f"  {self.role}  ",
                 font=("Segoe UI", 8, "bold"), fg="white",
                 bg=badge_bg, pady=3).pack(side="left", padx=4)
        right = tk.Frame(topbar, bg=self.accent);
        right.pack(side="right", padx=14)
        tk.Label(right, text=f"  {self.username}  ",
                 font=FONT_SMALL, fg="#BDEFDF",
                 bg=self.accent).pack(side="left")
        btn(right, "Sign out", self._logout,
            bg=badge_bg, fg="white", padx=10, pady=4,
            font=FONT_SMALL).pack(side="left", padx=(6, 0))

        body = tk.Frame(self.root, bg=C_BG);
        body.pack(fill="both", expand=True)
        self.sidebar = tk.Frame(body, bg=self.accent, width=210)
        self.sidebar.pack(side="left", fill="y");
        self.sidebar.pack_propagate(False)
        self._build_sidebar()
        self.content = tk.Frame(body, bg=C_BG)
        self.content.pack(side="left", fill="both", expand=True)

    def _darken(self, hex_col):
        r, g, b = int(hex_col[1:3], 16), int(hex_col[3:5], 16), int(hex_col[5:7], 16)
        r, g, b = max(0, r - 30), max(0, g - 30), max(0, b - 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _build_sidebar(self):
        tk.Frame(self.sidebar, bg=self.accent, height=10).pack()
        self.nav_buttons = {}
        hover = self._lighten(self.accent)
        for section, items in self.SIDEBAR_SECTIONS:
            tk.Label(self.sidebar, text=section, font=("Segoe UI", 7, "bold"),
                     fg="#A8DFCB", bg=self.accent, anchor="w").pack(
                fill="x", padx=14, pady=(10, 2))
            for key, lbl_text in items:
                b = tk.Button(self.sidebar, text=lbl_text,
                              font=FONT_SMALL, fg="white", bg=self.accent,
                              relief="flat", anchor="w", padx=14, pady=7,
                              cursor="hand2", bd=0,
                              activebackground=hover, activeforeground="white",
                              command=lambda k=key: self.show_panel(k))
                b.pack(fill="x");
                self.nav_buttons[key] = b

    def _lighten(self, hex_col):
        r, g, b = int(hex_col[1:3], 16), int(hex_col[3:5], 16), int(hex_col[5:7], 16)
        r, g, b = min(255, r + 40), min(255, g + 40), min(255, b + 40)
        return f"#{r:02x}{g:02x}{b:02x}"

    def show_panel(self, key):
        for w in self.content.winfo_children(): w.destroy()
        hover = self._lighten(self.accent)
        for k, b in self.nav_buttons.items():
            b.configure(bg=hover if k == key else self.accent)
        method_name = self.PANEL_MAP.get(key)
        if method_name:
            getattr(self, method_name)()

    # ── Shared widget builders ─────────────────────────────────
    def _page_title(self, parent, title, subtitle=""):
        h = tk.Frame(parent, bg=C_BG);
        h.pack(fill="x", padx=24, pady=(18, 4))
        label(h, title, font=FONT_H1, fg=C_TEXT, bg=C_BG).pack(anchor="w")
        if subtitle:
            label(h, subtitle, font=FONT_SMALL, fg=C_MUTED, bg=C_BG).pack(anchor="w")
        separator(parent)

    def _form_row(self, parent, fields):
        row = tk.Frame(parent, bg=C_CARD);
        row.pack(fill="x", padx=16, pady=4)
        for lt, build_fn in fields:
            col = tk.Frame(row, bg=C_CARD);
            col.pack(side="left", padx=(0, 18), anchor="n")
            tk.Label(col, text=lt, font=("Segoe UI", 8, "bold"),
                     fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            build_fn(col).pack(anchor="w", pady=(2, 0))
        return row

    def _admitted_ids(self):
        return [f"{v['patient_id']} — {v['full_name']}"
                for v in self.patients.values() if v["status"] == "Admitted"]

    def _all_ids(self):
        return [f"{v['patient_id']} — {v['full_name']}"
                for v in self.patients.values()]

    def _pid_from_combo(self, val):
        return val.split(" — ")[0] if " — " in val else val

    def _populate_tree(self, tree, rows):
        for item in tree.get_children(): tree.delete(item)
        for i, row in enumerate(rows):
            tree.insert("", "end", values=row, tags=("alt",) if i % 2 else ())

    def _kpi_row(self, parent, kpis):
        row = tk.Frame(parent, bg=C_BG);
        row.pack(fill="x", padx=24, pady=(4, 14))
        for lt, val, icon, col in kpis:
            kpi_card(row, lt, val, icon, col)

    def _disease_chart(self, parent, all_p):
        dc = {}
        for x in all_p: dc[x["disease"]] = dc.get(x["disease"], 0) + 1
        top5 = sorted(dc.items(), key=lambda x: -x[1])[:5]
        if not top5:
            tk.Label(parent, text="No data yet", font=FONT_SMALL,
                     fg=C_MUTED, bg=C_CARD, pady=14).pack();
            return
        max_v = top5[0][1]
        inner = tk.Frame(parent, bg=C_CARD);
        inner.pack(padx=12, pady=12, fill="x")
        colours = [self.accent, C_BLUE, C_PURPLE, C_DANGER, C_GOLD]
        for i, (dis, cnt) in enumerate(top5):
            row = tk.Frame(inner, bg=C_CARD);
            row.pack(fill="x", pady=3)
            nm = dis[:18] + "…" if len(dis) > 18 else dis
            tk.Label(row, text=nm, font=FONT_TINY, fg=C_TEXT,
                     bg=C_CARD, width=18, anchor="w").pack(side="left")
            c = tk.Canvas(row, width=130, height=16, bg=C_CARD, highlightthickness=0)
            c.pack(side="left")
            bw = max(int((cnt / max_v) * 120), 4)
            c.create_rectangle(0, 3, bw, 13, fill=colours[i % len(colours)], outline="")
            tk.Label(row, text=str(cnt), font=FONT_TINY, fg=C_MUTED, bg=C_CARD).pack(side="left", padx=4)

    def _activity_feed(self, parent, all_p, n=6):
        inner = tk.Frame(parent, bg=C_CARD);
        inner.pack(padx=10, pady=10, fill="both", expand=True)
        recent = sorted(all_p, key=lambda x: x.get("admission_date", ""), reverse=True)[:n]
        if not recent:
            tk.Label(inner, text="No activity yet", font=FONT_SMALL,
                     fg=C_MUTED, bg=C_CARD).pack(pady=10);
            return
        for pt in recent:
            row = tk.Frame(inner, bg=C_CARD);
            row.pack(fill="x", pady=3)
            dc = self.accent if pt["status"] == "Admitted" else C_MUTED
            tk.Label(row, text="●", font=("Segoe UI", 8), fg=dc, bg=C_CARD).pack(side="left", padx=(0, 6))
            inf = tk.Frame(row, bg=C_CARD);
            inf.pack(side="left", fill="x")
            tk.Label(inf, text=pt["full_name"], font=("Segoe UI", 9, "bold"),
                     fg=C_TEXT, bg=C_CARD, anchor="w").pack(anchor="w")
            ds = pt.get("admission_date", "")[:10]
            tk.Label(inf, text=f"{pt['status']}  ·  {ds}", font=FONT_TINY,
                     fg=dc, bg=C_CARD, anchor="w").pack(anchor="w")
            tk.Frame(inner, bg=C_BORDER, height=1).pack(fill="x", pady=2)

    # ── Common panels reused across roles ──────────────────────
    def _panel_search(self):
        p = self.content
        self._page_title(p, "Search Patient", "Look up by Patient ID")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pid_v = tk.StringVar()
        tk.Label(inner, text="Patient ID", font=("Segoe UI", 8, "bold"),
                 fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        row = tk.Frame(inner, bg=C_CARD);
        row.pack(fill="x", pady=(2, 0))
        entry(row, textvariable=pid_v, width=14).pack(side="left", padx=(0, 10))
        result_frame = card_frame(p)

        def do_search():
            for w in result_frame.winfo_children(): w.destroy()
            pid = pid_v.get().strip().upper()
            patient = self.patients.get(pid)
            if not patient: toast(self.root, f"No patient found for '{pid}'", "error"); return
            result_frame.pack(padx=24, pady=8, fill="x")
            fields = [
                ("── Patient ──", None),
                ("Patient ID", patient["patient_id"]), ("Full Name", patient["full_name"]),
                ("Age", patient["age"]), ("Gender", patient["gender"]),
                ("Disease", patient["disease"]),
                ("Doctor", patient.get("doctor_assigned") or "—"),
                ("Days Admitted", patient["days_admitted"]),
                ("Treatment Cost", fmt_kes(patient["treatment_cost"])),
                ("Status", patient["status"]),
                ("Admission Date", patient.get("admission_date", "—")),
                ("Discharge Date", patient.get("discharge_date") or "—"),
                ("Total Bill", fmt_kes(calc_bill(patient))),
                ("── Next of Kin ──", None),
                ("NOK Name", patient.get("nok_name") or "—"),
                ("Relationship", patient.get("nok_rel") or "—"),
                ("NOK Phone", patient.get("nok_phone") or "—"),
            ]
            inner2 = tk.Frame(result_frame, bg=C_CARD);
            inner2.pack(padx=16, pady=14, fill="x")
            label(inner2, "Patient Details", font=FONT_H2, fg=self.accent, bg=C_CARD).pack(anchor="w", pady=(0, 8))
            for k, v in fields:
                if v is None:
                    tk.Label(inner2, text=k, font=("Segoe UI", 8, "bold"), fg=self.accent, bg=C_CARD).pack(anchor="w",
                                                                                                           pady=(8, 2))
                    tk.Frame(inner2, bg=C_BORDER, height=1).pack(fill="x", pady=(0, 4));
                    continue
                r2 = tk.Frame(inner2, bg=C_CARD);
                r2.pack(fill="x", pady=2)
                tk.Label(r2, text=f"{k}:", font=("Segoe UI", 9, "bold"), fg=C_MUTED, bg=C_CARD, width=20,
                         anchor="w").pack(side="left")
                tk.Label(r2, text=str(v), font=FONT_BODY, fg=C_TEXT, bg=C_CARD, anchor="w").pack(side="left")

        btn(row, "Search", do_search).pack(side="left")

    def _panel_all_patients(self):
        p = self.content
        self._page_title(p, "All Patients", "Full patient registry")
        cols = ("ID", "Name", "Age", "Gender", "Disease", "Doctor", "Ward", "Status")
        widths = [60, 145, 42, 68, 135, 130, 120, 80]
        tf, tree = build_tree(p, cols, widths, height=18)
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        rows = [(x["patient_id"], x["full_name"], x["age"], x["gender"],
                 x["disease"], x.get("doctor_assigned") or "—",
                 x.get("ward") or "—", x["status"])
                for x in self.patients.values()]
        self._populate_tree(tree, rows)

    def _panel_ward_assignment(self):
        p = self.content
        self._page_title(p, "Ward Assignment", "Assign admitted patients to specific wards")

        adm_patients = [x for x in self.patients.values() if x["status"] == "Admitted"]
        wards = _default_wards()
        ward_names = [w["name"] for w in wards]

        card = card_frame(p)
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD)
        inner.pack(padx=16, pady=16, fill="x")

        pv = tk.StringVar()
        wv = tk.StringVar()

        tk.Label(inner, text="Select Admitted Patient", font=FONT_SMALL, bg=C_CARD, fg=C_MUTED).pack(anchor="w")
        cb_p = combobox(inner, pv, [f"{x['patient_id']} — {x['full_name']}" for x in adm_patients], width=40)
        cb_p.pack(anchor="w", pady=(2, 10))

        tk.Label(inner, text="Select Ward", font=FONT_SMALL, bg=C_CARD, fg=C_MUTED).pack(anchor="w")
        cb_w = combobox(inner, wv, ward_names, width=40)
        cb_w.pack(anchor="w", pady=(2, 14))

        def do_assign():
            sel_p = pv.get()
            sel_w = wv.get()
            if not sel_p or not sel_w:
                toast(self.root, "Select patient and ward", "error")
                return

            pid = sel_p.split(" — ")[0]
            if pid in self.patients:
                self.patients[pid]["ward"] = sel_w
                save_data(self.patients)
                toast(self.root, f"Patient assigned to {sel_w}")
                refresh_tree()
                pv.set("")
                wv.set("")

        btn(inner, "Assign to Ward", do_assign).pack(anchor="w")

        separator(p)
        label(p, "Current Ward Occupancy", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", padx=24, pady=(4, 6))

        cols = ("ID", "Patient Name", "Condition", "Assigned Ward", "Doctor")
        widths = [60, 150, 150, 150, 130]
        tf, tree = build_tree(p, cols, widths, height=10)
        tf.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        def refresh_tree():
            rows = [(x["patient_id"], x["full_name"], x["disease"], x.get("ward") or "Unassigned",
                     x.get("doctor_assigned") or "—")
                    for x in self.patients.values() if x["status"] == "Admitted"]
            self._populate_tree(tree, rows)

        refresh_tree()

    def _panel_morgue(self):
        p = self.content
        self._page_title(p, "Morgue Management", "Records for deceased patients")
        morgue_data = load_morgue()

        kpis = [
            ("Total Deceased", str(len(morgue_data)), "⚰️", C_DANGER),
            ("Recent Entries", str(sum(1 for m in morgue_data if m.get("dod", "").startswith(today_str()))), "📅",
             C_ACCENT),
        ]
        self._kpi_row(p, kpis)

        cols = ("ID", "Name", "D.O.D", "Cause of Death", "Morgue Slot", "Status")
        widths = [60, 150, 130, 200, 100, 100]
        tf, tree = build_tree(p, cols, widths, height=12)
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))

        def refresh():
            m_data = load_morgue()
            rows = [(m["patient_id"], m["name"], m["dod"], m["cause"], m["slot"], m["status"]) for m in m_data]
            self._populate_tree(tree, rows)

        refresh()

        if self.role in ["Administrator", "Morgue Attendant", "Doctor"]:
            btn_row = tk.Frame(p, bg=C_BG)
            btn_row.pack(fill="x", padx=24, pady=(0, 16))

            def register_death():
                win = tk.Toplevel(self.root)
                win.title("Register Death")
                win.geometry("400x450")
                win.configure(bg=C_BG)

                inner = tk.Frame(win, bg=C_BG, padx=20, pady=20)
                inner.pack(fill="both", expand=True)

                pv = tk.StringVar()
                causev = tk.StringVar()
                slotv = tk.StringVar()

                tk.Label(inner, text="Select Patient", font=FONT_SMALL, bg=C_BG).pack(anchor="w")
                cb = combobox(inner, pv, self._all_ids(), width=34)
                cb.pack(pady=(2, 10))

                tk.Label(inner, text="Cause of Death", font=FONT_SMALL, bg=C_BG).pack(anchor="w")
                entry(inner, textvariable=causev, width=34).pack(pady=(2, 10))

                tk.Label(inner, text="Morgue Slot / ID", font=FONT_SMALL, bg=C_BG).pack(anchor="w")
                entry(inner, textvariable=slotv, width=34).pack(pady=(2, 20))

                def save():
                    sel = pv.get()
                    if not sel: toast(win, "Select patient", "error"); return
                    pid = self._pid_from_combo(sel)
                    p_name = sel.split(" — ")[1]

                    m_data = load_morgue()
                    m_data.append({
                        "patient_id": pid,
                        "name": p_name,
                        "dod": now_str(),
                        "cause": causev.get() or "Unknown",
                        "slot": slotv.get() or "TBD",
                        "status": "In Morgue"
                    })
                    save_morgue(m_data)

                    # Update patient status
                    if pid in self.patients:
                        self.patients[pid]["status"] = "Deceased"
                        save_data(self.patients)

                    toast(self.root, f"Death registered for {p_name}")
                    win.destroy()
                    refresh()

                btn(inner, "Register Death", save, bg=C_DANGER).pack(fill="x")

            btn(btn_row, "＋ Register Death", register_death, bg=C_DANGER).pack(side="left", padx=(0, 10))
            btn(btn_row, "↻ Refresh", refresh, bg=C_MUTED).pack(side="left")

    def _on_close(self):
        save_data(self.patients);
        self.root.destroy()

    def _logout(self):
        save_data(self.patients)
        for w in self.root.winfo_children(): w.destroy()
        self.root.configure(bg=C_BG)
        self.root.title("MediCare HMS — Login")
        w, h = 440, 560
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")
        LoginWindow(self.root, _launch_app(self.root))


# ══════════════════════════════════════════════════════════════
#  1. ADMINISTRATOR
# ══════════════════════════════════════════════════════════════
class AdminApp(BaseApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  Dashboard")]),
        ("PATIENTS", [("register", "＋  Register Patient"),
                      ("all_patients", "☰  All Patients"),
                      ("edit_patient", "✎  Edit Patient"),
                      ("search", "⌕  Search Patient")]),
        ("CLINICAL", [("assign_doctor", "⚕  Assign Doctor"),
                      ("diagnosis", "✎  Diagnosis")]),
        ("FINANCE", [("billing", "₭  Billing"),
                     ("discharge", "→  Discharge")]),
        ("WARDS", [("ward_assign", "🏥  Ward Assignment")]),
        ("ADMIN", [("user_mgmt", "👥  User Management"),
                   ("report", "▤  Full Report")]),
    ]
    PANEL_MAP = {
        "dashboard": "_panel_dashboard",
        "register": "_panel_register",
        "all_patients": "_panel_all_patients",
        "edit_patient": "_panel_edit_patient",
        "search": "_panel_search",
        "assign_doctor": "_panel_assign_doctor",
        "diagnosis": "_panel_diagnosis",
        "billing": "_panel_billing",
        "discharge": "_panel_discharge",
        "user_mgmt": "_panel_user_mgmt",
        "report": "_panel_report",
    }

    def _panel_dashboard(self):
        p = self.content
        now = datetime.now().strftime("%A, %d %B %Y  ·  %H:%M")
        self._page_title(p, "Administrator Dashboard", now)
        all_p = list(self.patients.values())
        adm = sum(1 for x in all_p if x["status"] == "Admitted")
        rev = sum(calc_bill(x) for x in all_p)
        avg_d = (sum(x["days_admitted"] for x in all_p) / len(all_p)) if all_p else 0
        users = load_users()
        self._kpi_row(p, [
            ("Total Patients", str(len(all_p)), "👥", C_BLUE),
            ("Admitted", str(adm), "🏥", self.accent),
            ("Discharged", str(len(all_p) - adm), "✓", C_MUTED),
            ("Avg Stay", f"{avg_d:.1f}d", "📅", C_PURPLE),
            ("Revenue", fmt_kes(rev), "₭", C_DANGER),
            ("Staff Accounts", str(len(users)), "🔑", C_GOLD),
        ])
        two = tk.Frame(p, bg=C_BG);
        two.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        left = tk.Frame(two, bg=C_BG);
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        label(left, "Recent Patients", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        cols = ("ID", "Name", "Age", "Disease", "Doctor", "Days", "Status")
        widths = [60, 140, 42, 128, 128, 45, 78]
        tf, tree = build_tree(left, cols, widths, height=12)
        tf.pack(fill="both", expand=True)
        rows = [(x["patient_id"], x["full_name"], x["age"], x["disease"],
                 x.get("doctor_assigned") or "—", x["days_admitted"], x["status"])
                for x in reversed(all_p)]
        self._populate_tree(tree, rows)
        right = tk.Frame(two, bg=C_BG, width=300);
        right.pack(side="left", fill="y");
        right.pack_propagate(False)
        label(right, "Top Conditions", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        cc = card_frame(right);
        cc.pack(fill="x");
        self._disease_chart(cc, all_p)
        separator(right, pady=10)
        label(right, "Activity Feed", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        fc = card_frame(right);
        fc.pack(fill="both", expand=True);
        self._activity_feed(fc, all_p)

    def _panel_register(self):
        p = self.content
        self._page_title(p, "Register Patient", "Add a new patient")
        canvas = tk.Canvas(p, bg=C_BG, highlightthickness=0)
        vsb = ttk.Scrollbar(p, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y");
        canvas.pack(side="left", fill="both", expand=True)
        sf = tk.Frame(canvas, bg=C_BG)
        wid = canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(wid, width=e.width))
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        label(sf, "Patient Information", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", padx=24, pady=(8, 4))
        card = card_frame(sf);
        card.pack(padx=24, pady=(0, 10), fill="x")
        name_v = tk.StringVar();
        age_v = tk.StringVar();
        gender_v = tk.StringVar(value="Male");
        disease_v = tk.StringVar()
        self._form_row(card, [("Full Name", lambda f: entry(f, textvariable=name_v, width=30)),
                              ("Age", lambda f: entry(f, textvariable=age_v, width=8)),
                              ("Gender", lambda f: combobox(f, gender_v, ["Male", "Female", "Other"], width=12))])
        self._form_row(card, [("Disease / Condition", lambda f: entry(f, textvariable=disease_v, width=42))])
        tk.Frame(card, bg=C_CARD, height=6).pack()

        label(sf, "Next of Kin", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", padx=24, pady=(6, 4))
        nk = card_frame(sf);
        nk.pack(padx=24, pady=(0, 10), fill="x")
        nn_v = tk.StringVar();
        nr_v = tk.StringVar(value="Spouse");
        np_v = tk.StringVar();
        na_v = tk.StringVar()
        self._form_row(nk, [("Full Name", lambda f: entry(f, textvariable=nn_v, width=28)),
                            ("Relationship", lambda f: combobox(f, nr_v,
                                                                ["Spouse", "Parent", "Child", "Sibling", "Guardian",
                                                                 "Friend", "Other"], width=14))])
        self._form_row(nk, [("Phone", lambda f: entry(f, textvariable=np_v, width=18)),
                            ("Address", lambda f: entry(f, textvariable=na_v, width=30))])
        tk.Frame(nk, bg=C_CARD, height=6).pack()

        def do_reg():
            nm = name_v.get().strip();
            dis = disease_v.get().strip()
            try:
                age = int(age_v.get());
                assert age > 0
            except:
                toast(self.root, "Valid age required", "error");
                return
            if not nm: toast(self.root, "Name required", "error"); return
            if not dis: toast(self.root, "Condition required", "error"); return
            pid = next_pid(self.patients)
            self.patients[pid] = {"patient_id": pid, "full_name": nm, "age": age,
                                  "gender": gender_v.get(), "disease": dis, "doctor_assigned": None,
                                  "days_admitted": 0, "treatment_cost": 0.0, "status": "Admitted",
                                  "admission_date": now_str(), "discharge_date": None,
                                  "nok_name": nn_v.get().strip(), "nok_rel": nr_v.get(),
                                  "nok_phone": np_v.get().strip(), "nok_addr": na_v.get().strip()}
            save_data(self.patients)
            for v in (name_v, age_v, disease_v, nn_v, np_v, na_v): v.set("")
            toast(self.root, f"Patient {pid} registered")

        ar = tk.Frame(sf, bg=C_BG);
        ar.pack(fill="x", padx=24, pady=(0, 16))
        btn(ar, "  Register Patient", do_reg).pack(side="left")

    def _panel_edit_patient(self):
        p = self.content
        self._page_title(p, "Edit Patient", "Search, select, and update patient details")
        lookup = card_frame(p);
        lookup.pack(padx=24, pady=(4, 6), fill="x")
        li = tk.Frame(lookup, bg=C_CARD);
        li.pack(padx=16, pady=14, fill="x")
        tk.Label(li, text="Search (ID or name)", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        sr = tk.Frame(li, bg=C_CARD);
        sr.pack(fill="x", pady=(4, 0))
        sv = tk.StringVar()
        se = entry(sr, textvariable=sv, width=22);
        se.pack(side="left", padx=(0, 8))
        lf2 = tk.Frame(li, bg=C_CARD);
        lf2.pack(fill="x", pady=(8, 0))
        lb = tk.Listbox(lf2, font=FONT_BODY, height=5, bg="#EBF5F0", fg=C_TEXT,
                        selectbackground=self.accent, selectforeground="white",
                        relief="flat", highlightbackground=C_BORDER, highlightthickness=1, activestyle="none")
        lvsb = ttk.Scrollbar(lf2, orient="vertical", command=lb.yview)
        lb.configure(yscrollcommand=lvsb.set);
        lvsb.pack(side="right", fill="y");
        lb.pack(side="left", fill="x", expand=True)

        def _rl(*_):
            q = sv.get().strip().lower();
            lb.delete(0, "end")
            for pt in self.patients.values():
                if q in pt["patient_id"].lower() or q in pt["full_name"].lower() or q == "":
                    lb.insert("end", f"{pt['patient_id']}  ·  {pt['full_name']}  ({pt['age']}y)  —  {pt['status']}")

        sv.trace_add("write", _rl);
        _rl()
        edit_outer = tk.Frame(p, bg=C_BG)
        ev = {k: tk.StringVar() for k in
              ("name", "age", "gender", "disease", "status", "doctor", "days", "cost", "nn", "nr", "np", "na")}
        ev["gender"].set("Male");
        ev["status"].set("Admitted");
        ev["nr"].set("Spouse")
        sel_pid = [None]
        badge = tk.Label(p, text="", font=("Segoe UI", 9, "bold"), fg=self.accent, bg=C_BG)
        badge.pack(anchor="w", padx=24, pady=(4, 0))

        def _load(pid):
            sel_pid[0] = pid;
            pt = self.patients[pid]
            for k, fk in [("name", "full_name"), ("age", "age"), ("gender", "gender"), ("disease", "disease"),
                          ("status", "status"), ("doctor", "doctor_assigned"), ("days", "days_admitted"),
                          ("cost", "treatment_cost"), ("nn", "nok_name"), ("nr", "nok_rel"), ("np", "nok_phone"),
                          ("na", "nok_addr")]:
                ev[k].set(str(pt.get(fk) or ""))
            edit_outer.pack(fill="x", padx=24, pady=(0, 8))
            badge.configure(text=f"Editing  ›  {pid}  —  {pt['full_name']}")

        def _sel(event):
            s = lb.curselection()
            if not s: return
            pid = lb.get(s[0]).split("  ·  ")[0].strip()
            if pid in self.patients: _load(pid)

        lb.bind("<<ListboxSelect>>", _sel)
        btn(sr, "Load Selected", _sel, pady=5, padx=12).pack(side="left")
        lc = tk.Frame(edit_outer, bg=C_BG);
        rc = tk.Frame(edit_outer, bg=C_BG)
        lc.pack(side="left", fill="both", expand=True, padx=(0, 8));
        rc.pack(side="left", fill="both", expand=True)
        label(lc, "Patient Information", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 4))
        pic = card_frame(lc);
        pic.pack(fill="x")
        pii = tk.Frame(pic, bg=C_CARD);
        pii.pack(padx=14, pady=14, fill="x")
        for lt, k, w in [("Full Name", "name", 26), ("Age", "age", 8)]:
            tk.Label(pii, text=lt, font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            entry(pii, textvariable=ev[k], width=w).pack(anchor="w", pady=(2, 8))
        tk.Label(pii, text="Gender", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(pii, ev["gender"], ["Male", "Female", "Other"], width=14).pack(anchor="w", pady=(2, 8))
        tk.Label(pii, text="Disease", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        entry(pii, textvariable=ev["disease"], width=32).pack(anchor="w", pady=(2, 8))
        tk.Label(pii, text="Status", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(pii, ev["status"], ["Admitted", "Discharged"], width=14).pack(anchor="w", pady=(2, 8))
        tk.Label(pii, text="Doctor", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        entry(pii, textvariable=ev["doctor"], width=26).pack(anchor="w", pady=(2, 8))
        dr = tk.Frame(pii, bg=C_CARD);
        dr.pack(fill="x", pady=(0, 8))
        for lt, k, w in [("Days", ev["days"], 10), ("Cost (KES)", ev["cost"], 14)]:
            col = tk.Frame(dr, bg=C_CARD);
            col.pack(side="left", padx=(0, 14))
            tk.Label(col, text=lt, font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            entry(col, textvariable=k, width=w).pack(anchor="w", pady=(2, 0))
        label(rc, "Next of Kin", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 4))
        nc = card_frame(rc);
        nc.pack(fill="x")
        ni = tk.Frame(nc, bg=C_CARD);
        ni.pack(padx=14, pady=14, fill="x")
        for lt, k, w in [("Full Name", "nn", 26), ("Phone", "np", 20), ("Address", "na", 28)]:
            tk.Label(ni, text=lt, font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            entry(ni, textvariable=ev[k], width=w).pack(anchor="w", pady=(2, 8))
        tk.Label(ni, text="Relationship", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(ni, ev["nr"], ["Spouse", "Parent", "Child", "Sibling", "Guardian", "Friend", "Other"], width=16).pack(
            anchor="w", pady=(2, 8))

        def do_save():
            pid = sel_pid[0]
            if not pid: return
            nm = ev["name"].get().strip()
            if not nm: toast(self.root, "Name required", "error"); return
            try:
                age = int(ev["age"].get());
                assert age > 0
            except:
                toast(self.root, "Valid age required", "error");
                return
            try:
                days = int(ev["days"].get());
                assert days >= 0
            except:
                toast(self.root, "Valid days required", "error");
                return
            try:
                cost = float(ev["cost"].get());
                assert cost >= 0
            except:
                toast(self.root, "Valid cost required", "error");
                return
            pt = self.patients[pid]
            ns = ev["status"].get()
            if ns == "Discharged" and pt["status"] != "Discharged":
                pt["discharge_date"] = now_str()
            elif ns == "Admitted":
                pt["discharge_date"] = None
            pt.update({"full_name": nm, "age": age, "gender": ev["gender"].get(),
                       "disease": ev["disease"].get().strip(), "status": ns,
                       "doctor_assigned": ev["doctor"].get().strip() or None,
                       "days_admitted": days, "treatment_cost": cost,
                       "nok_name": ev["nn"].get().strip(), "nok_rel": ev["nr"].get(),
                       "nok_phone": ev["np"].get().strip(), "nok_addr": ev["na"].get().strip()})
            save_data(self.patients);
            _rl()
            toast(self.root, f"Patient {pid} updated");
            badge.configure(text=f"Editing  ›  {pid}  —  {nm}  ✔")

        def do_cancel():
            sel_pid[0] = None;
            edit_outer.pack_forget();
            badge.configure(text="");
            sv.set("");
            _rl()

        br = tk.Frame(edit_outer, bg=C_BG);
        br.pack(fill="x", pady=(10, 0))
        btn(br, "  Save Changes", do_save, pady=7).pack(side="left", padx=(0, 10))
        btn(br, "  Cancel", do_cancel, bg="#E5E7EB", fg=C_TEXT, pady=7).pack(side="left")

    def _panel_assign_doctor(self):
        p = self.content
        self._page_title(p, "Assign Doctor", "Link a doctor to an admitted patient")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar();
        dv = tk.StringVar()
        tk.Label(inner, text="Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, pv, self._admitted_ids(), width=34).pack(anchor="w", pady=(2, 10))
        tk.Label(inner, text="Doctor's Name", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        entry(inner, textvariable=dv, width=34).pack(anchor="w", pady=(2, 14))

        def do():
            sel = pv.get();
            doc = dv.get().strip()
            if not sel: toast(self.root, "Select a patient", "error"); return
            if not doc: toast(self.root, "Enter doctor name", "error"); return
            pid = self._pid_from_combo(sel)
            self.patients[pid]["doctor_assigned"] = doc;
            save_data(self.patients);
            dv.set("")
            toast(self.root, f"Dr. {doc} assigned")

        btn(inner, "  Assign Doctor", do).pack(anchor="w")

    def _panel_diagnosis(self):
        p = self.content
        self._page_title(p, "Record Diagnosis", "Update condition, days, treatment cost")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar();
        dv = tk.StringVar();
        daysv = tk.StringVar();
        costv = tk.StringVar()

        def prefill(*_):
            sel = pv.get()
            if not sel: return
            pt = self.patients.get(self._pid_from_combo(sel))
            if pt: dv.set(pt["disease"]); daysv.set(str(pt["days_admitted"])); costv.set(str(pt["treatment_cost"]))

        tk.Label(inner, text="Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        cb = combobox(inner, pv, self._admitted_ids(), width=34);
        cb.pack(anchor="w", pady=(2, 10));
        cb.bind("<<ComboboxSelected>>", prefill)
        tk.Label(inner, text="Disease / Condition", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(
            anchor="w")
        entry(inner, textvariable=dv, width=38).pack(anchor="w", pady=(2, 10))
        r2 = tk.Frame(inner, bg=C_CARD);
        r2.pack(fill="x")
        for lt, var, w in [("Days Admitted", daysv, 10), ("Treatment Cost (KES)", costv, 16)]:
            col = tk.Frame(r2, bg=C_CARD);
            col.pack(side="left", padx=(0, 18))
            tk.Label(col, text=lt, font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            entry(col, textvariable=var, width=w).pack(anchor="w", pady=(2, 0))
        tk.Frame(inner, bg=C_CARD, height=10).pack()

        def do():
            sel = pv.get()
            if not sel: toast(self.root, "Select patient", "error"); return
            pt = self.patients[self._pid_from_combo(sel)]
            if dv.get().strip(): pt["disease"] = dv.get().strip()
            try:
                d = int(daysv.get());
                assert d >= 0;
                pt["days_admitted"] = d
            except:
                toast(self.root, "Invalid days", "error");
                return
            try:
                c = float(costv.get());
                assert c >= 0;
                pt["treatment_cost"] = c
            except:
                toast(self.root, "Invalid cost", "error");
                return
            save_data(self.patients);
            toast(self.root, f"Record updated for {pt['full_name']}")

        btn(inner, "  Save Record", do).pack(anchor="w")

    def _panel_billing(self):
        p = self.content
        self._page_title(p, "Billing", "Itemised patient bill")
        top = tk.Frame(p, bg=C_BG);
        top.pack(fill="x", padx=24, pady=(8, 0))
        pv = tk.StringVar()
        tk.Label(top, text="Select Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_BG).pack(anchor="w")
        cb = combobox(top, pv, self._admitted_ids(), width=36);
        cb.pack(anchor="w", pady=(2, 10))
        bc = card_frame(p);
        bc.pack(padx=24, pady=8, fill="x")
        bi = tk.Frame(bc, bg=C_CARD);
        bi.pack(padx=20, pady=18, fill="x")
        lm = {}
        for txt, key in [("Admission Fee", "adm"), ("Daily Bed Charge", "bed"), ("Treatment Cost", "trt")]:
            r = tk.Frame(bi, bg=C_CARD);
            r.pack(fill="x", pady=4)
            tk.Label(r, text=txt, font=FONT_BODY, fg=C_MUTED, bg=C_CARD).pack(side="left")
            v = tk.StringVar(value="—");
            lm[key] = v
            tk.Label(r, textvariable=v, font=FONT_BODY, fg=C_TEXT, bg=C_CARD).pack(side="right")
        tk.Frame(bi, bg=C_BORDER, height=1).pack(fill="x", pady=8)
        tr = tk.Frame(bi, bg=C_CARD);
        tr.pack(fill="x")
        tk.Label(tr, text="TOTAL BILL", font=FONT_H2, fg=C_TEXT, bg=C_CARD).pack(side="left")
        tv = tk.StringVar(value="—")
        tk.Label(tr, textvariable=tv, font=("Georgia", 14, "bold"), fg=self.accent, bg=C_CARD).pack(side="right")

        def do_calc(*_):
            sel = pv.get()
            if not sel: return
            pt = self.patients.get(self._pid_from_combo(sel))
            if not pt: return
            bed = DAILY_BED_RATE * pt["days_admitted"];
            trt = pt["treatment_cost"]
            lm["adm"].set(fmt_kes(ADMISSION_FEE))
            lm["bed"].set(f"{fmt_kes(bed)}  ({pt['days_admitted']} days × KES {DAILY_BED_RATE:,})")
            lm["trt"].set(fmt_kes(trt));
            tv.set(fmt_kes(ADMISSION_FEE + bed + trt))

        cb.bind("<<ComboboxSelected>>", do_calc)
        btn(top, "  Calculate Bill", do_calc).pack(anchor="w", pady=(0, 4))

    def _panel_discharge(self):
        p = self.content
        self._page_title(p, "Discharge Patient", "Finalise and discharge")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar()
        tk.Label(inner, text="Select Admitted Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(
            anchor="w")
        combobox(inner, pv, self._admitted_ids(), width=34).pack(anchor="w", pady=(2, 14))

        def do():
            sel = pv.get()
            if not sel: toast(self.root, "Select a patient", "error"); return
            pid = self._pid_from_combo(sel);
            pt = self.patients[pid]
            if not messagebox.askyesno("Confirm",
                                       f"Discharge {pt['full_name']}?\nBill: {fmt_kes(calc_bill(pt))}"): return
            pt["status"] = "Discharged";
            pt["discharge_date"] = now_str()
            save_data(self.patients);
            toast(self.root, f"{pt['full_name']} discharged");
            pv.set("");
            refresh_dc()

        btn(inner, "  Discharge Patient", do, bg=C_DANGER).pack(anchor="w")
        separator(p)
        label(p, "Discharged Patients", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", padx=24, pady=(4, 6))
        cols = ("ID", "Name", "Discharge Date", "Days", "Total Bill");
        widths = [60, 150, 130, 50, 130]
        tf, tree = build_tree(p, cols, widths, height=10);
        tf.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        def refresh_dc():
            rows = [(x["patient_id"], x["full_name"], x.get("discharge_date") or "—",
                     x["days_admitted"], fmt_kes(calc_bill(x)))
                    for x in self.patients.values() if x["status"] == "Discharged"]
            self._populate_tree(tree, rows)

        refresh_dc()

    def _panel_user_mgmt(self):
        p = self.content
        self._page_title(p, "User Management", "View and remove staff accounts")
        users = load_users()
        cols = ("Username", "Full Name", "Role");
        widths = [120, 200, 150]
        tf, tree = build_tree(p, cols, widths, height=14);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 8))

        def refresh():
            users = load_users()
            rows = [(u, d.get("full_name", "—"), d["role"]) for u, d in users.items()]
            self._populate_tree(tree, rows)

        refresh()
        act = tk.Frame(p, bg=C_BG);
        act.pack(fill="x", padx=24, pady=(0, 12))

        def do_remove():
            sel = tree.selection()
            if not sel: toast(self.root, "Select a user", "warn"); return
            uname = tree.item(sel[0])["values"][0]
            if uname == self.username: toast(self.root, "Cannot remove yourself", "error"); return
            if messagebox.askyesno("Confirm", f"Remove account '{uname}'?"):
                users = load_users();
                users.pop(uname, None);
                save_users(users);
                refresh()
                toast(self.root, f"Account '{uname}' removed")

        btn(act, "  Remove Selected", do_remove, bg=C_DANGER).pack(side="left")
        btn(act, "  Refresh", refresh, bg=C_MUTED, pady=6, padx=14).pack(side="left", padx=(10, 0))

    def _panel_report(self):
        p = self.content
        self._page_title(p, "Full Report", f"Generated {datetime.now().strftime('%d %b %Y  %H:%M')}")
        all_p = list(self.patients.values())
        adm = sum(1 for x in all_p if x["status"] == "Admitted")
        rev = sum(calc_bill(x) for x in all_p)
        avg_d = (sum(x["days_admitted"] for x in all_p) / len(all_p)) if all_p else 0
        dc = {}
        for x in all_p: dc[x["disease"]] = dc.get(x["disease"], 0) + 1
        top = max(dc, key=dc.get) if dc else "—"
        self._kpi_row(p, [("Total", str(len(all_p)), "👥", C_BLUE), ("Admitted", str(adm), "🏥", self.accent),
                          ("Discharged", str(len(all_p) - adm), "✓", C_MUTED),
                          ("Revenue", fmt_kes(rev), "₭", C_DANGER), ("Avg Stay", f"{avg_d:.1f}d", "📅", C_PURPLE)])
        tk.Frame(p, bg=C_BG).pack(pady=2)
        label(p, f"Most common condition: {top}  ({dc.get(top, 0)} cases)",
              font=FONT_SMALL, fg=C_MUTED, bg=C_BG).pack(anchor="w", padx=24)
        label(p, "Patient Revenue Breakdown", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", padx=24, pady=(8, 6))
        cols = ("ID", "Name", "Days", "Treatment", "Total Bill", "Status");
        widths = [60, 150, 50, 120, 120, 80]
        tf, tree = build_tree(p, cols, widths, height=11);
        tf.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        rows = [(x["patient_id"], x["full_name"], x["days_admitted"],
                 fmt_kes(x["treatment_cost"]), fmt_kes(calc_bill(x)), x["status"]) for x in all_p]
        self._populate_tree(tree, rows)


# ══════════════════════════════════════════════════════════════
#  2. DOCTOR
# ══════════════════════════════════════════════════════════════
class DoctorApp(BaseApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  My Dashboard")]),
        ("PATIENTS", [("my_patients", "🏥  My Patients"),
                      ("all_patients", "☰  All Patients"),
                      ("search", "⌕  Search Patient")]),
        ("CLINICAL", [("diagnosis", "✎  Diagnosis & Notes"),
                      ("prescribe", "💊  Write Prescription"),
                      ("ward_rounds", "📋  Ward Rounds")]),
    ]
    PANEL_MAP = {
        "dashboard": "_panel_dashboard",
        "my_patients": "_panel_my_patients",
        "all_patients": "_panel_all_patients",
        "search": "_panel_search",
        "diagnosis": "_panel_diagnosis",
        "prescribe": "_panel_prescribe",
        "ward_rounds": "_panel_ward_rounds",
    }

    def _panel_dashboard(self):
        p = self.content
        self._page_title(p, "Doctor Dashboard", f"Dr. {self.username}  ·  {datetime.now().strftime('%d %b %Y')}")
        all_p = list(self.patients.values())
        mine = [x for x in all_p if
                (x.get("doctor_assigned") or "").lower() == self.username.lower() and x["status"] == "Admitted"]
        pending_rx = load_rx()
        pending = [r for r in pending_rx if r.get("status") == "Pending" and r.get("doctor") == self.username]
        self._kpi_row(p, [
            ("My Admitted Patients", str(len(mine)), "🏥", C_BLUE),
            ("Total Hospital Patients", str(len(all_p)), "👥", self.accent),
            ("Pending Prescriptions", str(len(pending)), "💊", C_DANGER),
        ])
        two = tk.Frame(p, bg=C_BG);
        two.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        left = tk.Frame(two, bg=C_BG);
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        label(left, "My Patients", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        cols = ("ID", "Name", "Age", "Disease", "Days", "Bill");
        widths = [60, 150, 42, 140, 45, 120]
        tf, tree = build_tree(left, cols, widths, height=13);
        tf.pack(fill="both", expand=True)
        rows = [(x["patient_id"], x["full_name"], x["age"], x["disease"],
                 x["days_admitted"], fmt_kes(calc_bill(x))) for x in mine]
        self._populate_tree(tree, rows)
        right = tk.Frame(two, bg=C_BG, width=300);
        right.pack(side="left", fill="y");
        right.pack_propagate(False)
        label(right, "Top Conditions", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        cc = card_frame(right);
        cc.pack(fill="x");
        self._disease_chart(cc, all_p)
        separator(right, pady=10)
        label(right, "Recent Activity", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        fc = card_frame(right);
        fc.pack(fill="both", expand=True);
        self._activity_feed(fc, mine)

    def _panel_my_patients(self):
        p = self.content
        self._page_title(p, "My Patients", "Patients assigned to you")
        mine = [x for x in self.patients.values()
                if (x.get("doctor_assigned") or "").lower() == self.username.lower()]
        cols = ("ID", "Name", "Age", "Disease", "Days", "Status", "Bill");
        widths = [60, 145, 42, 140, 45, 80, 120]
        tf, tree = build_tree(p, cols, widths, height=18);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        rows = [(x["patient_id"], x["full_name"], x["age"], x["disease"],
                 x["days_admitted"], x["status"], fmt_kes(calc_bill(x))) for x in mine]
        self._populate_tree(tree, rows)

    def _panel_diagnosis(self):
        p = self.content
        self._page_title(p, "Diagnosis & Clinical Notes", "Update condition, days, cost, add notes")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar();
        dv = tk.StringVar();
        daysv = tk.StringVar();
        costv = tk.StringVar();
        notesv = tk.StringVar()

        def prefill(*_):
            sel = pv.get()
            if not sel: return
            pt = self.patients.get(self._pid_from_combo(sel))
            if pt: dv.set(pt["disease"]); daysv.set(str(pt["days_admitted"])); costv.set(str(pt["treatment_cost"]))

        tk.Label(inner, text="Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        cb = combobox(inner, pv, self._admitted_ids(), width=34);
        cb.pack(anchor="w", pady=(2, 10));
        cb.bind("<<ComboboxSelected>>", prefill)
        r2 = tk.Frame(inner, bg=C_CARD);
        r2.pack(fill="x", pady=(0, 8))
        for lt, var, w in [("Disease", dv, 28), ("Days", daysv, 8), ("Cost (KES)", costv, 14)]:
            col = tk.Frame(r2, bg=C_CARD);
            col.pack(side="left", padx=(0, 14))
            tk.Label(col, text=lt, font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            entry(col, textvariable=var, width=w).pack(anchor="w", pady=(2, 0))
        tk.Label(inner, text="Clinical Notes", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w",
                                                                                                         pady=(6, 2))
        notes_box = tk.Text(inner, height=4, width=60, font=FONT_BODY, bg="#EBF5F0", fg=C_TEXT,
                            relief="flat", highlightbackground=C_BORDER, highlightthickness=1)
        notes_box.pack(anchor="w", pady=(0, 10))

        def do():
            sel = pv.get()
            if not sel: toast(self.root, "Select patient", "error"); return
            pt = self.patients[self._pid_from_combo(sel)]
            if dv.get().strip(): pt["disease"] = dv.get().strip()
            try:
                d = int(daysv.get());
                assert d >= 0;
                pt["days_admitted"] = d
            except:
                toast(self.root, "Invalid days", "error");
                return
            try:
                c = float(costv.get());
                assert c >= 0;
                pt["treatment_cost"] = c
            except:
                toast(self.root, "Invalid cost", "error");
                return
            notes = notes_box.get("1.0", "end").strip()
            if notes:
                existing = pt.get("clinical_notes", [])
                existing.append({"by": self.username, "at": now_str(), "note": notes})
                pt["clinical_notes"] = existing;
                notes_box.delete("1.0", "end")
            save_data(self.patients);
            toast(self.root, f"Record updated")

        btn(inner, "  Save & Add Notes", do).pack(anchor="w")

    def _panel_prescribe(self):
        p = self.content
        self._page_title(p, "Write Prescription", "Issue medication for an admitted patient")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar();
        drugv = tk.StringVar();
        dosev = tk.StringVar();
        freqv = tk.StringVar(value="Once daily");
        daysv = tk.StringVar()
        inv = [i["drug"] for i in load_inventory()]
        r1 = tk.Frame(inner, bg=C_CARD);
        r1.pack(fill="x", pady=(0, 8))
        tk.Label(r1, text="Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(r1, pv, self._admitted_ids(), width=34).pack(anchor="w", pady=(2, 0))
        r2 = tk.Frame(inner, bg=C_CARD);
        r2.pack(fill="x", pady=(0, 8))
        for lt, var, vals, w in [("Drug", drugv, inv, 28),
                                 ("Frequency", freqv,
                                  ["Once daily", "Twice daily", "Three times daily", "As needed", "Every 8 hrs",
                                   "Every 6 hrs"], 20)]:
            col = tk.Frame(r2, bg=C_CARD);
            col.pack(side="left", padx=(0, 16))
            tk.Label(col, text=lt, font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            combobox(col, var, vals, width=w).pack(anchor="w", pady=(2, 0))
        r3 = tk.Frame(inner, bg=C_CARD);
        r3.pack(fill="x", pady=(0, 8))
        for lt, var, w in [("Dose", dosev, 12), ("Duration (days)", daysv, 10)]:
            col = tk.Frame(r3, bg=C_CARD);
            col.pack(side="left", padx=(0, 16))
            tk.Label(col, text=lt, font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            entry(col, textvariable=var, width=w).pack(anchor="w", pady=(2, 0))

        def do():
            sel = pv.get()
            if not sel: toast(self.root, "Select patient", "error"); return
            if not drugv.get(): toast(self.root, "Select drug", "error"); return
            if not dosev.get().strip(): toast(self.root, "Enter dose", "error"); return
            rx = load_rx()
            rx.append({"id": f"RX{len(rx) + 1:04d}", "patient_id": self._pid_from_combo(sel),
                       "patient_name": sel.split(" — ")[1] if " — " in sel else sel,
                       "drug": drugv.get(), "dose": dosev.get().strip(),
                       "frequency": freqv.get(), "days": daysv.get().strip(),
                       "doctor": self.username, "issued_at": now_str(), "status": "Pending"})
            save_rx(rx);
            dosev.set("");
            daysv.set("")
            toast(self.root, "Prescription issued");
            refresh_rx()

        btn(inner, "  Issue Prescription", do).pack(anchor="w", pady=(4, 0))
        separator(p)
        label(p, "Prescriptions Issued Today", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", padx=24, pady=(4, 6))
        cols = ("RX ID", "Patient", "Drug", "Dose", "Freq", "Status");
        widths = [70, 140, 160, 80, 130, 80]
        tf, tree = build_tree(p, cols, widths, height=9);
        tf.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        def refresh_rx():
            rx = load_rx();
            today = today_str()
            rows = [(r["id"], r["patient_name"], r["drug"], r["dose"], r["frequency"], r["status"])
                    for r in rx if r.get("issued_at", "").startswith(today)]
            self._populate_tree(tree, rows)

        refresh_rx()

    def _panel_ward_rounds(self):
        p = self.content
        self._page_title(p, "Ward Rounds", "Review all admitted patients with vitals summary")
        all_adm = [x for x in self.patients.values() if x["status"] == "Admitted"]
        vitals = load_vitals()
        cols = ("ID", "Name", "Age", "Disease", "Days", "Last BP", "Last Temp", "Doctor");
        widths = [60, 140, 42, 140, 42, 90, 80, 120]
        tf, tree = build_tree(p, cols, widths, height=16);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        rows = []
        for x in all_adm:
            pid = x["patient_id"];
            pv = vitals.get(pid, [])
            last = pv[-1] if pv else {}
            rows.append((pid, x["full_name"], x["age"], x["disease"], x["days_admitted"],
                         last.get("bp", "—"), last.get("temp", "—"), x.get("doctor_assigned") or "—"))
        self._populate_tree(tree, rows)


# ══════════════════════════════════════════════════════════════
#  3. NURSE
# ══════════════════════════════════════════════════════════════
class NurseApp(BaseApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  My Dashboard")]),
        ("WARD CARE", [("vitals", "💓  Record Vitals"),
                       ("nursing_notes", "📝  Nursing Notes"),
                       ("tasks", "☑  Task Checklist")]),
        ("PATIENTS", [("all_patients", "☰  All Patients"),
                      ("search", "⌕  Search Patient")]),
        ("WARDS", [("ward_assign", "🏥  Ward Assignment")]),
    ]
    PANEL_MAP = {
        "dashboard": "_panel_dashboard",
        "vitals": "_panel_vitals",
        "nursing_notes": "_panel_nursing_notes",
        "tasks": "_panel_tasks",
        "all_patients": "_panel_all_patients",
        "search": "_panel_search",
        "ward_assign": "_panel_ward_assignment",
    }

    def _panel_dashboard(self):
        p = self.content
        self._page_title(p, "Nurse Dashboard", f"{self.username}  ·  {datetime.now().strftime('%d %b %Y  %H:%M')}")
        all_p = list(self.patients.values())
        adm = [x for x in all_p if x["status"] == "Admitted"]
        tasks = load_tasks();
        pending_t = [t for t in tasks if not t.get("done")]
        vitals = load_vitals()
        self._kpi_row(p, [
            ("Admitted Patients", str(len(adm)), "🏥", C_BLUE),
            ("Pending Tasks", str(len(pending_t)), "☑", C_DANGER),
            ("Vitals Recorded Today", str(sum(1 for v in vitals.values()
                                              if v and v[-1].get("date", "").startswith(today_str()))), "💓",
             self.accent),
        ])
        two = tk.Frame(p, bg=C_BG);
        two.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        left = tk.Frame(two, bg=C_BG);
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        label(left, "Admitted Patients", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        cols = ("ID", "Name", "Age", "Disease", "Doctor", "Days");
        widths = [60, 145, 42, 140, 130, 45]
        tf, tree = build_tree(left, cols, widths, height=13);
        tf.pack(fill="both", expand=True)
        rows = [(x["patient_id"], x["full_name"], x["age"], x["disease"],
                 x.get("doctor_assigned") or "—", x["days_admitted"]) for x in adm]
        self._populate_tree(tree, rows)
        right = tk.Frame(two, bg=C_BG, width=280);
        right.pack(side="left", fill="y");
        right.pack_propagate(False)
        label(right, "Pending Tasks", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        tc = card_frame(right);
        tc.pack(fill="x")
        ti = tk.Frame(tc, bg=C_CARD);
        ti.pack(padx=10, pady=10, fill="x")
        shown = pending_t[:8]
        if not shown:
            tk.Label(ti, text="All tasks done! ✓", font=FONT_SMALL, fg=C_SUCCESS, bg=C_CARD).pack(pady=8)
        for t in shown:
            r = tk.Frame(ti, bg=C_CARD);
            r.pack(fill="x", pady=2)
            tk.Label(r, text="•", font=FONT_BODY, fg=self.accent, bg=C_CARD).pack(side="left", padx=(0, 6))
            tk.Label(r, text=t["task"], font=FONT_SMALL, fg=C_TEXT, bg=C_CARD, anchor="w", wraplength=200).pack(
                side="left")
        separator(right, pady=8)
        label(right, "Activity Feed", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        fc = card_frame(right);
        fc.pack(fill="both", expand=True);
        self._activity_feed(fc, adm)

    def _panel_vitals(self):
        p = self.content
        self._page_title(p, "Record Vitals", "Log BP, temperature, pulse, O₂ for a patient")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar();
        bpv = tk.StringVar();
        tempv = tk.StringVar();
        pulsev = tk.StringVar();
        o2v = tk.StringVar();
        weightv = tk.StringVar()
        tk.Label(inner, text="Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, pv, self._admitted_ids(), width=34).pack(anchor="w", pady=(2, 10))
        r1 = tk.Frame(inner, bg=C_CARD);
        r1.pack(fill="x", pady=(0, 8))
        for lt, var, w, ph in [("Blood Pressure (mmHg)", bpv, 14, "120/80"),
                               ("Temperature (°C)", tempv, 8, "37.0"),
                               ("Pulse (bpm)", pulsev, 8, "72"),
                               ("O₂ Saturation (%)", o2v, 8, "98"),
                               ("Weight (kg)", weightv, 8, "")]:
            col = tk.Frame(r1, bg=C_CARD);
            col.pack(side="left", padx=(0, 12))
            tk.Label(col, text=lt, font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            e = entry(col, textvariable=var, width=w);
            e.pack(anchor="w", pady=(2, 0))

        def do():
            sel = pv.get()
            if not sel: toast(self.root, "Select patient", "error"); return
            pid = self._pid_from_combo(sel)
            vitals = load_vitals()
            entry_data = {"date": now_str(), "bp": bpv.get().strip(), "temp": tempv.get().strip(),
                          "pulse": pulsev.get().strip(), "o2": o2v.get().strip(),
                          "weight": weightv.get().strip(), "nurse": self.username}
            if pid not in vitals: vitals[pid] = []
            vitals[pid].append(entry_data);
            save_vitals(vitals)
            for v in (bpv, tempv, pulsev, o2v, weightv): v.set("")
            toast(self.root, "Vitals recorded");
            refresh_vt()

        btn(inner, "  Record Vitals", do).pack(anchor="w", pady=(6, 0))
        separator(p)
        label(p, "Recent Vitals Log", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", padx=24, pady=(4, 6))
        cols = ("Patient ID", "Name", "Date", "BP", "Temp", "Pulse", "O₂", "Nurse");
        widths = [70, 130, 130, 90, 70, 70, 60, 100]
        tf, tree = build_tree(p, cols, widths, height=9);
        tf.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        def refresh_vt():
            vitals = load_vitals();
            rows = []
            for pid, entries in vitals.items():
                pt = self.patients.get(pid)
                nm = pt["full_name"] if pt else "—"
                for e in reversed(entries[-3:]):
                    rows.append((pid, nm, e.get("date", ""), e.get("bp", ""), e.get("temp", ""),
                                 e.get("pulse", ""), e.get("o2", ""), e.get("nurse", "")))
            self._populate_tree(tree, rows)

        refresh_vt()

    def _panel_nursing_notes(self):
        p = self.content
        self._page_title(p, "Nursing Notes", "Add and view nursing observations")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar()
        tk.Label(inner, text="Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, pv, self._admitted_ids(), width=34).pack(anchor="w", pady=(2, 10))
        tk.Label(inner, text="Note", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        nb = tk.Text(inner, height=4, width=60, font=FONT_BODY, bg="#EBF5F0", fg=C_TEXT,
                     relief="flat", highlightbackground=C_BORDER, highlightthickness=1)
        nb.pack(anchor="w", pady=(2, 10))

        def do():
            sel = pv.get()
            if not sel: toast(self.root, "Select patient", "error"); return
            note = nb.get("1.0", "end").strip()
            if not note: toast(self.root, "Enter a note", "error"); return
            pid = self._pid_from_combo(sel);
            pt = self.patients[pid]
            nn = pt.get("nursing_notes", [])
            nn.append({"by": self.username, "at": now_str(), "note": note})
            pt["nursing_notes"] = nn;
            save_data(self.patients);
            nb.delete("1.0", "end")
            toast(self.root, "Note saved");
            refresh_notes()

        btn(inner, "  Save Note", do).pack(anchor="w")
        separator(p)
        label(p, "Notes Log", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", padx=24, pady=(4, 6))
        cols = ("Patient", "Date", "Note", "By");
        widths = [130, 130, 360, 100]
        tf, tree = build_tree(p, cols, widths, height=10);
        tf.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        def refresh_notes():
            rows = []
            for pt in self.patients.values():
                for n in pt.get("nursing_notes", []):
                    rows.append((pt["full_name"], n["at"], n["note"][:60], n["by"]))
            rows.sort(key=lambda x: x[1], reverse=True)
            self._populate_tree(tree, rows)

        refresh_notes()

    def _panel_tasks(self):
        p = self.content
        self._page_title(p, "Task Checklist", "Manage ward tasks and nursing duties")
        top = tk.Frame(p, bg=C_BG);
        top.pack(fill="x", padx=24, pady=(4, 6))
        taskv = tk.StringVar()
        tk.Label(top, text="New Task", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_BG).pack(anchor="w")
        row = tk.Frame(top, bg=C_BG);
        row.pack(fill="x", pady=(2, 0))
        entry(row, textvariable=taskv, width=50).pack(side="left", padx=(0, 10))
        tasks = [];
        check_vars = {}
        cols = ("", "Task", "Added By", "Time", "Done");
        widths = [30, 280, 120, 130, 60]
        tf, tree = build_tree(p, cols, widths, height=16);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))

        def refresh():
            ts = load_tasks()
            rows = [("✓" if t.get("done") else "○", t["task"], t.get("by", ""), t.get("at", ""),
                     "Done" if t.get("done") else "Pending") for t in ts]
            self._populate_tree(tree, rows)

        def add_task():
            t = taskv.get().strip()
            if not t: toast(self.root, "Enter task text", "error"); return
            ts = load_tasks();
            ts.append({"task": t, "by": self.username, "at": now_str(), "done": False})
            save_tasks(ts);
            taskv.set("");
            toast(self.root, "Task added");
            refresh()

        def mark_done():
            sel = tree.selection()
            if not sel: toast(self.root, "Select a task", "warn"); return
            idx = tree.index(sel[0]);
            ts = load_tasks()
            if idx < len(ts): ts[idx]["done"] = True; save_tasks(ts); toast(self.root, "Marked done"); refresh()

        def delete_task():
            sel = tree.selection()
            if not sel: toast(self.root, "Select a task", "warn"); return
            idx = tree.index(sel[0]);
            ts = load_tasks()
            if idx < len(ts): ts.pop(idx); save_tasks(ts); toast(self.root, "Task removed"); refresh()

        btn(row, "  Add Task", add_task, pady=5, padx=12).pack(side="left")
        act = tk.Frame(p, bg=C_BG);
        act.pack(fill="x", padx=24, pady=(0, 8))
        btn(act, "  Mark Done ✓", mark_done, bg=C_SUCCESS, pady=5, padx=12).pack(side="left", padx=(0, 10))
        btn(act, "  Delete", delete_task, bg=C_DANGER, pady=5, padx=12).pack(side="left")
        refresh()


# ══════════════════════════════════════════════════════════════
#  4. HRIO (Health Records & Information Officer)
# ══════════════════════════════════════════════════════════════
class HRIOApp(BaseApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  Dashboard")]),
        ("PATIENTS", [("register", "＋  Register Patient"),
                      ("all_patients", "☰  All Patients"),
                      ("search", "⌕  Search Patient")]),
        ("WARDS", [("ward_assign", "🏥  Ward Assignment")]),
        ("APPOINTMENTS", [("appointments", "📅  Appointments"),
                          ("walk_ins", "🚶  Walk-ins Today")]),
    ]
    PANEL_MAP = {
        "dashboard": "_panel_dashboard",
        "register": "_panel_register",
        "all_patients": "_panel_all_patients",
        "search": "_panel_search",
        "ward_assign": "_panel_ward_assignment",
        "appointments": "_panel_appointments",
        "walk_ins": "_panel_walk_ins",
    }

    def _panel_dashboard(self):
        p = self.content
        self._page_title(p, "HRIO Dashboard", f"{datetime.now().strftime('%A, %d %B %Y  ·  %H:%M')}")
        all_p = list(self.patients.values())
        adm = sum(1 for x in all_p if x["status"] == "Admitted")
        appts = load_appointments();
        today_appts = [a for a in appts if a.get("date", "").startswith(today_str())]
        self._kpi_row(p, [
            ("Total Patients", str(len(all_p)), "👥", C_BLUE),
            ("Admitted", str(adm), "🏥", self.accent),
            ("Today's Appointments", str(len(today_appts)), "📅", C_PURPLE),
            ("New Today", str(sum(1 for x in all_p if x.get("admission_date", "").startswith(today_str()))), "🆕",
             C_GOLD),
        ])
        two = tk.Frame(p, bg=C_BG);
        two.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        left = tk.Frame(two, bg=C_BG);
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        label(left, "Today's Appointments", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        cols = ("Time", "Patient", "Doctor", "Reason", "Status");
        widths = [80, 150, 130, 160, 90]
        tf, tree = build_tree(left, cols, widths, height=13);
        tf.pack(fill="both", expand=True)
        rows = [(a["time"], a["patient"], a["doctor"], a.get("reason", "—"), a.get("status", "Scheduled"))
                for a in today_appts]
        self._populate_tree(tree, rows)
        right = tk.Frame(two, bg=C_BG, width=280);
        right.pack(side="left", fill="y");
        right.pack_propagate(False)
        label(right, "Recently Registered", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        fc = card_frame(right);
        fc.pack(fill="both", expand=True);
        self._activity_feed(fc, all_p)

    def _panel_register(self):
        p = self.content
        self._page_title(p, "Register Patient", "Add a new patient")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        name_v = tk.StringVar();
        age_v = tk.StringVar();
        gender_v = tk.StringVar(value="Male")
        disease_v = tk.StringVar();
        nn_v = tk.StringVar();
        nr_v = tk.StringVar(value="Spouse");
        np_v = tk.StringVar()
        self._form_row(inner, [("Full Name", lambda f: entry(f, textvariable=name_v, width=28)),
                               ("Age", lambda f: entry(f, textvariable=age_v, width=8)),
                               ("Gender", lambda f: combobox(f, gender_v, ["Male", "Female", "Other"], width=12))])
        self._form_row(inner, [("Disease / Condition", lambda f: entry(f, textvariable=disease_v, width=40))])
        separator(inner)
        label(inner, "Next of Kin", font=FONT_H3, fg=self.accent, bg=C_CARD).pack(anchor="w", pady=(4, 4))
        self._form_row(inner, [("Name", lambda f: entry(f, textvariable=nn_v, width=26)),
                               ("Relationship", lambda f: combobox(f, nr_v,
                                                                   ["Spouse", "Parent", "Child", "Sibling", "Guardian",
                                                                    "Friend", "Other"], width=14)),
                               ("Phone", lambda f: entry(f, textvariable=np_v, width=16))])
        tk.Frame(inner, bg=C_CARD, height=6).pack()

        def do():
            nm = name_v.get().strip();
            dis = disease_v.get().strip()
            try:
                age = int(age_v.get());
                assert age > 0
            except:
                toast(self.root, "Valid age required", "error");
                return
            if not nm: toast(self.root, "Name required", "error"); return
            if not dis: toast(self.root, "Condition required", "error"); return
            pid = next_pid(self.patients)
            self.patients[pid] = {"patient_id": pid, "full_name": nm, "age": age,
                                  "gender": gender_v.get(), "disease": dis, "doctor_assigned": None,
                                  "days_admitted": 0, "treatment_cost": 0.0, "status": "Admitted",
                                  "admission_date": now_str(), "discharge_date": None,
                                  "nok_name": nn_v.get().strip(), "nok_rel": nr_v.get(),
                                  "nok_phone": np_v.get().strip(), "nok_addr": ""}
            save_data(self.patients)
            for v in (name_v, age_v, disease_v, nn_v, np_v): v.set("")
            toast(self.root, f"Patient {pid} registered");
            refresh_tbl()

        btn(inner, "  Register Patient", do).pack(anchor="w", pady=(0, 12))
        separator(p)
        label(p, "Registered Today", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", padx=24, pady=(4, 6))
        cols = ("ID", "Name", "Age", "Gender", "Disease", "NOK Phone", "Status");
        widths = [60, 140, 42, 68, 150, 110, 80]
        tf, tree = build_tree(p, cols, widths, height=9);
        tf.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        def refresh_tbl():
            rows = [(x["patient_id"], x["full_name"], x["age"], x["gender"],
                     x["disease"], x.get("nok_phone") or "—", x["status"])
                    for x in self.patients.values() if x.get("admission_date", "").startswith(today_str())]
            self._populate_tree(tree, rows)

        refresh_tbl()

    def _panel_appointments(self):
        p = self.content
        self._page_title(p, "Appointments", "Schedule and manage appointments")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pname_v = tk.StringVar();
        doc_v = tk.StringVar();
        date_v = tk.StringVar(value=today_str())
        time_v = tk.StringVar(value="09:00");
        reason_v = tk.StringVar()
        r1 = tk.Frame(inner, bg=C_CARD);
        r1.pack(fill="x", pady=(0, 8))
        for lt, var, w in [("Patient Name", pname_v, 26), ("Doctor", doc_v, 22), ("Date (YYYY-MM-DD)", date_v, 16),
                           ("Time", time_v, 8)]:
            col = tk.Frame(r1, bg=C_CARD);
            col.pack(side="left", padx=(0, 14))
            tk.Label(col, text=lt, font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            entry(col, textvariable=var, width=w).pack(anchor="w", pady=(2, 0))
        tk.Label(inner, text="Reason", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w",
                                                                                                 pady=(6, 2))
        entry(inner, textvariable=reason_v, width=50).pack(anchor="w")

        def do():
            if not pname_v.get().strip(): toast(self.root, "Patient name required", "error"); return
            if not doc_v.get().strip(): toast(self.root, "Doctor required", "error"); return
            appts = load_appointments()
            appts.append({"patient": pname_v.get().strip(), "doctor": doc_v.get().strip(),
                          "date": date_v.get().strip(), "time": time_v.get().strip(),
                          "reason": reason_v.get().strip(), "status": "Scheduled",
                          "booked_by": self.username, "booked_at": now_str()})
            save_appointments(appts)
            for v in (pname_v, doc_v, reason_v): v.set("")
            toast(self.root, "Appointment scheduled");
            refresh_appts()

        btn(inner, "  Schedule Appointment", do, pady=7).pack(anchor="w", pady=(8, 0))
        separator(p)
        label(p, "All Appointments", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", padx=24, pady=(4, 6))
        cols = ("Date", "Time", "Patient", "Doctor", "Reason", "Status");
        widths = [100, 70, 140, 130, 180, 90]
        tf, tree = build_tree(p, cols, widths, height=11);
        tf.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        def refresh_appts():
            appts = load_appointments()
            rows = [
                (a["date"], a["time"], a["patient"], a["doctor"], a.get("reason", "—"), a.get("status", "Scheduled"))
                for a in sorted(appts, key=lambda x: x.get("date", ""), reverse=True)]
            self._populate_tree(tree, rows)

        refresh_appts()

    def _panel_walk_ins(self):
        p = self.content
        self._page_title(p, "Walk-ins Today", "Patients who arrived today without an appointment")
        today = today_str()
        walk_ins = [x for x in self.patients.values() if x.get("admission_date", "").startswith(today)]
        cols = ("ID", "Name", "Age", "Disease", "Admission Time", "Status");
        widths = [60, 150, 42, 150, 130, 80]
        tf, tree = build_tree(p, cols, widths, height=16);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        rows = [(x["patient_id"], x["full_name"], x["age"], x["disease"],
                 x.get("admission_date", ""), x["status"]) for x in walk_ins]
        self._populate_tree(tree, rows)
        label(p, f"Total walk-ins today: {len(walk_ins)}", font=FONT_SMALL, fg=C_MUTED, bg=C_BG).pack(anchor="w",
                                                                                                      padx=24)


# ══════════════════════════════════════════════════════════════
#  5. PHARMACIST
# ══════════════════════════════════════════════════════════════
class PharmacistApp(BaseApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  Dashboard")]),
        ("DISPENSING", [("rx_queue", "💊  Prescription Queue"),
                        ("dispense", "✓  Dispense Medication")]),
        ("INVENTORY", [("inventory", "📦  Drug Inventory"),
                       ("restock", "＋  Restock Drug")]),
        ("LOGS", [("dispense_log", "📋  Dispensing Log"),
                  ("search", "⌕  Search Patient")]),
    ]
    PANEL_MAP = {
        "dashboard": "_panel_dashboard",
        "rx_queue": "_panel_rx_queue",
        "dispense": "_panel_dispense",
        "inventory": "_panel_inventory",
        "restock": "_panel_restock",
        "dispense_log": "_panel_dispense_log",
        "search": "_panel_search",
    }

    def _panel_dashboard(self):
        p = self.content
        self._page_title(p, "Pharmacy Dashboard", f"{datetime.now().strftime('%d %b %Y  ·  %H:%M')}")
        rx = load_rx();
        inv = load_inventory()
        pending = [r for r in rx if r.get("status") == "Pending"]
        dispensed_today = [r for r in rx if
                           r.get("status") == "Dispensed" and r.get("dispensed_at", "").startswith(today_str())]
        low = [i for i in inv if i["stock"] <= i["reorder"]]
        self._kpi_row(p, [
            ("Pending Prescriptions", str(len(pending)), "💊", C_DANGER),
            ("Dispensed Today", str(len(dispensed_today)), "✓", self.accent),
            ("Low Stock Alerts", str(len(low)), "⚠", C_GOLD),
            ("Drug Lines", str(len(inv)), "📦", C_BLUE),
        ])
        two = tk.Frame(p, bg=C_BG);
        two.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        left = tk.Frame(two, bg=C_BG);
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        label(left, "Pending Prescriptions", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        cols = ("RX ID", "Patient", "Drug", "Dose", "Freq", "Doctor", "Issued");
        widths = [70, 130, 150, 70, 120, 110, 120]
        tf, tree = build_tree(left, cols, widths, height=10);
        tf.pack(fill="both", expand=True)
        rows = [(r["id"], r["patient_name"], r["drug"], r["dose"], r["frequency"], r["doctor"], r["issued_at"][:16])
                for r in pending]
        self._populate_tree(tree, rows)
        right = tk.Frame(two, bg=C_BG, width=280);
        right.pack(side="left", fill="y");
        right.pack_propagate(False)
        label(right, "⚠ Low Stock", font=FONT_H2, fg=C_DANGER, bg=C_BG).pack(anchor="w", pady=(0, 6))
        lc = card_frame(right);
        lc.pack(fill="x")
        li = tk.Frame(lc, bg=C_CARD);
        li.pack(padx=10, pady=10, fill="x")
        if not low:
            tk.Label(li, text="All stock levels OK ✓", font=FONT_SMALL, fg=C_SUCCESS, bg=C_CARD).pack(pady=8)
        for item in low[:8]:
            r = tk.Frame(li, bg=C_CARD);
            r.pack(fill="x", pady=3)
            tk.Label(r, text="⚠", font=FONT_SMALL, fg=C_DANGER, bg=C_CARD).pack(side="left", padx=(0, 6))
            tk.Label(r, text=f"{item['drug']}", font=("Segoe UI", 9, "bold"), fg=C_TEXT, bg=C_CARD).pack(side="left")
            tk.Label(r, text=f"  {item['stock']} {item['unit']}", font=FONT_TINY, fg=C_DANGER, bg=C_CARD).pack(
                side="left")
        separator(right, pady=8)
        label(right, "Inventory Status", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        ic = card_frame(right);
        ic.pack(fill="x")
        ii = tk.Frame(ic, bg=C_CARD);
        ii.pack(padx=10, pady=10, fill="x")
        CHART_H = 100
        canvas = tk.Canvas(ii, width=240, height=CHART_H, bg=C_CARD, highlightthickness=0)
        canvas.pack()
        top5_inv = sorted(inv, key=lambda x: -x["stock"])[:5]
        if top5_inv:
            max_s = top5_inv[0]["stock"];
            bar_w = 36;
            gap = 8;
            x0 = 10
            colours_bar = ["#0C5C47", "#1565C0", "#6A1B9A", "#B71C1C", "#B8860B"]
            for i2, item in enumerate(top5_inv):
                bh = max(int((item["stock"] / max_s) * (CHART_H - 20)), 4)
                x1 = x0 + i2 * (bar_w + gap);
                y1 = CHART_H - bh - 10;
                y2 = CHART_H - 10
                canvas.create_rectangle(x1, y1, x1 + bar_w, y2, fill=colours_bar[i2 % 5], outline="")
                nm = item["drug"][:6];
                canvas.create_text(x1 + bar_w // 2, y2 + 2, text=nm, font=("Segoe UI", 7), fill=C_MUTED, anchor="n")

    def _panel_rx_queue(self):
        p = self.content
        self._page_title(p, "Prescription Queue", "All pending prescriptions")
        rx = load_rx();
        pending = [r for r in rx if r.get("status") == "Pending"]
        cols = ("RX ID", "Patient ID", "Patient", "Drug", "Dose", "Frequency", "Days", "Doctor", "Issued At");
        widths = [70, 70, 120, 150, 70, 120, 45, 110, 130]
        tf, tree = build_tree(p, cols, widths, height=18);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        rows = [(r["id"], r["patient_id"], r["patient_name"], r["drug"], r["dose"],
                 r["frequency"], r.get("days", "—"), r["doctor"], r["issued_at"][:16]) for r in pending]
        self._populate_tree(tree, rows)
        label(p, f"Pending: {len(pending)}", font=FONT_SMALL, fg=C_MUTED, bg=C_BG).pack(anchor="w", padx=24)

    def _panel_dispense(self):
        p = self.content
        self._page_title(p, "Dispense Medication", "Mark a prescription as dispensed and deduct stock")
        rx = load_rx();
        pending = [r for r in rx if r.get("status") == "Pending"]
        rx_labels = [f"{r['id']}  —  {r['patient_name']}  —  {r['drug']}" for r in pending]
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        rxv = tk.StringVar();
        qtyv = tk.StringVar(value="1")
        tk.Label(inner, text="Prescription", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, rxv, rx_labels, width=54).pack(anchor="w", pady=(2, 10))
        tk.Label(inner, text="Quantity to Dispense", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(
            anchor="w")
        entry(inner, textvariable=qtyv, width=8).pack(anchor="w", pady=(2, 14))
        info_var = tk.StringVar(value="")
        tk.Label(inner, textvariable=info_var, font=FONT_SMALL, fg=C_MUTED, bg=C_CARD).pack(anchor="w")

        def do():
            sel = rxv.get()
            if not sel: toast(self.root, "Select prescription", "error"); return
            rxid = sel.split("  —  ")[0].strip()
            try:
                qty = int(qtyv.get());
                assert qty > 0
            except:
                toast(self.root, "Valid quantity required", "error");
                return
            rx = load_rx();
            inv = load_inventory()
            target = next((r for r in rx if r["id"] == rxid), None)
            if not target: toast(self.root, "Prescription not found", "error"); return
            drug_item = next((i for i in inv if i["drug"] == target["drug"]), None)
            if drug_item:
                if drug_item["stock"] < qty: toast(self.root, f"Insufficient stock ({drug_item['stock']} left)",
                                                   "error"); return
                drug_item["stock"] -= qty;
                save_inventory(inv)
            target["status"] = "Dispensed";
            target["dispensed_by"] = self.username
            target["dispensed_at"] = now_str();
            target["qty_dispensed"] = qty
            save_rx(rx)
            stock_left = drug_item["stock"] if drug_item else "—"
            info_var.set(f"✓ Dispensed {qty}× {target['drug']}  |  Remaining stock: {stock_left}")
            toast(self.root, "Medication dispensed")
            # refresh the combobox
            rx2 = load_rx();
            pending2 = [r for r in rx2 if r.get("status") == "Pending"]
            rl2 = [f"{r['id']}  —  {r['patient_name']}  —  {r['drug']}" for r in pending2]
            rxv.set("");
            cb["values"] = rl2

        btn(inner, "  Dispense", do, bg=C_SUCCESS).pack(anchor="w")
        # grab combobox widget reference
        for w in inner.winfo_children():
            if isinstance(w, ttk.Combobox): cb = w; break

    def _panel_inventory(self):
        p = self.content
        self._page_title(p, "Drug Inventory", "Current stock levels")
        inv = load_inventory()
        cols = ("Drug", "Category", "Stock", "Unit", "Reorder Level", "Status");
        widths = [190, 120, 70, 80, 110, 90]
        tf, tree = build_tree(p, cols, widths, height=18);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))

        def refresh():
            inv = load_inventory()
            rows = []
            for item in sorted(inv, key=lambda x: x["drug"]):
                status = "⚠ Low" if item["stock"] <= item["reorder"] else "OK"
                rows.append((item["drug"], item["category"], item["stock"], item["unit"], item["reorder"], status))
            self._populate_tree(tree, rows)

        refresh()
        act = tk.Frame(p, bg=C_BG);
        act.pack(fill="x", padx=24, pady=(0, 8))
        btn(act, "  Refresh", refresh, bg=C_MUTED, pady=5, padx=12).pack(side="left")

    def _panel_restock(self):
        p = self.content
        self._page_title(p, "Restock Drug", "Add stock to an existing drug or add a new drug line")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        inv = load_inventory();
        drug_names = [i["drug"] for i in inv]
        drugv = tk.StringVar();
        qtyv = tk.StringVar();
        catv = tk.StringVar();
        unitv = tk.StringVar();
        reorderv = tk.StringVar()
        tk.Label(inner, text="Drug (select existing or type new name)", font=("Segoe UI", 8, "bold"), fg=C_MUTED,
                 bg=C_CARD).pack(anchor="w")
        drug_cb = ttk.Combobox(inner, textvariable=drugv, values=drug_names, width=36, font=FONT_BODY)
        drug_cb.pack(anchor="w", pady=(2, 10))
        r1 = tk.Frame(inner, bg=C_CARD);
        r1.pack(fill="x", pady=(0, 8))
        for lt, var, w in [("Quantity to Add", qtyv, 10), ("Category", catv, 18), ("Unit", unitv, 14),
                           ("Reorder Level", reorderv, 10)]:
            col = tk.Frame(r1, bg=C_CARD);
            col.pack(side="left", padx=(0, 14))
            tk.Label(col, text=lt, font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            entry(col, textvariable=var, width=w).pack(anchor="w", pady=(2, 0))

        def do():
            drug = drugv.get().strip()
            if not drug: toast(self.root, "Drug name required", "error"); return
            try:
                qty = int(qtyv.get());
                assert qty > 0
            except:
                toast(self.root, "Valid quantity required", "error");
                return
            inv = load_inventory()
            existing = next((i for i in inv if i["drug"].lower() == drug.lower()), None)
            if existing:
                existing["stock"] += qty
                if reorderv.get().strip():
                    try:
                        existing["reorder"] = int(reorderv.get())
                    except:
                        pass
            else:
                if not catv.get().strip(): toast(self.root, "Category required for new drug", "error"); return
                if not unitv.get().strip(): toast(self.root, "Unit required for new drug", "error"); return
                try:
                    ro = int(reorderv.get());
                    assert ro >= 0
                except:
                    ro = 20
                inv.append({"drug": drug, "category": catv.get().strip(), "stock": qty, "unit": unitv.get().strip(),
                            "reorder": ro})
            save_inventory(inv)
            for v in (drugv, qtyv, catv, unitv, reorderv): v.set("")
            toast(self.root, f"Stock updated for {drug}")

        btn(inner, "  Update Stock", do, pady=7).pack(anchor="w")

    def _panel_dispense_log(self):
        p = self.content
        self._page_title(p, "Dispensing Log", "All dispensed medications")
        rx = load_rx();
        dispensed = [r for r in rx if r.get("status") == "Dispensed"]
        cols = ("RX ID", "Patient", "Drug", "Qty", "Dispensed By", "Dispensed At");
        widths = [70, 140, 170, 50, 120, 130]
        tf, tree = build_tree(p, cols, widths, height=18);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        rows = [(r["id"], r["patient_name"], r["drug"], r.get("qty_dispensed", "—"),
                 r.get("dispensed_by", "—"), r.get("dispensed_at", "")[:16])
                for r in sorted(dispensed, key=lambda x: x.get("dispensed_at", ""), reverse=True)]
        self._populate_tree(tree, rows)
        label(p, f"Total dispensed: {len(dispensed)}", font=FONT_SMALL, fg=C_MUTED, bg=C_BG).pack(anchor="w", padx=24)


# ══════════════════════════════════════════════════════════════
#  6. RESIDENT / INTERN
# ══════════════════════════════════════════════════════════════
class ResidentApp(DoctorApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  My Dashboard")]),
        ("PATIENTS", [("all_patients", "☰  All Patients"),
                      ("search", "⌕  Search Patient")]),
        ("WARDS", [("ward_assign", "🏥  Ward Assignment")]),
        ("CLINICAL", [("diagnosis", "✎  Diagnosis & Notes"),
                      ("prescribe", "💊  Write Prescription"),
                      ("ward_rounds", "📋  Ward Rounds")]),
    ]


# ══════════════════════════════════════════════════════════════
#  7. LAB TECHNICIAN
# ══════════════════════════════════════════════════════════════
class LabApp(BaseApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  Lab Dashboard")]),
        ("LAB WORK", [("enter_results", "🔬  Enter Results"),
                      ("history", "📜  Lab History")]),
        ("PATIENTS", [("all_patients", "☰  All Patients")]),
    ]
    PANEL_MAP = {
        "dashboard": "_panel_dashboard",
        "enter_results": "_panel_enter_results",
        "history": "_panel_history",
        "all_patients": "_panel_all_patients",
    }

    def _panel_dashboard(self):
        p = self.content;
        self._page_title(p, "Laboratory Dashboard", now_str())
        lab = load_lab();
        pending = [l for l in lab if l.get("status") == "Pending"]
        self._kpi_row(p, [
            ("Pending Tests", str(len(pending)), "🔬", C_DANGER),
            ("Completed Today", str(sum(1 for l in lab if l.get("date", "").startswith(today_str()))), "✓", C_SUCCESS),
        ])

    def _panel_enter_results(self):
        p = self.content;
        self._page_title(p, "Enter Lab Results", "Record diagnostic findings")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar();
        testv = tk.StringVar();
        resv = tk.StringVar();
        unitv = tk.StringVar()
        tk.Label(inner, text="Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, pv, self._admitted_ids(), width=34).pack(anchor="w", pady=(2, 10))
        r1 = tk.Frame(inner, bg=C_CARD);
        r1.pack(fill="x", pady=(0, 8))
        for lt, var, w in [("Test Name", testv, 24), ("Result", resv, 14), ("Unit", unitv, 10)]:
            col = tk.Frame(r1, bg=C_CARD);
            col.pack(side="left", padx=(0, 14))
            tk.Label(col, text=lt, font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
            entry(col, textvariable=var, width=w).pack(anchor="w", pady=(2, 0))

        def do():
            if not pv.get(): toast(self.root, "Select patient", "error"); return
            lab = load_lab()
            lab.append({"patient_id": self._pid_from_combo(pv.get()), "patient_name": pv.get().split(" — ")[1],
                        "test": testv.get(), "result": resv.get(), "unit": unitv.get(), "date": now_str(),
                        "tech": self.username})
            save_lab(lab);
            toast(self.root, "Results saved")

        btn(inner, "  Save Results", do).pack(anchor="w", pady=(10, 0))

    def _panel_history(self):
        p = self.content;
        self._page_title(p, "Lab History", "All recorded tests")
        lab = load_lab();
        cols = ("Date", "Patient", "Test", "Result", "Unit", "Tech");
        widths = [130, 140, 150, 80, 70, 100]
        tf, tree = build_tree(p, cols, widths, height=18);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        rows = [(l["date"], l["patient_name"], l["test"], l["result"], l["unit"], l["tech"]) for l in reversed(lab)]
        self._populate_tree(tree, rows)


# ══════════════════════════════════════════════════════════════
#  8. RADIOLOGIC TECHNOLOGIST
# ══════════════════════════════════════════════════════════════
class RadiologyApp(BaseApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  Radiology Dashboard")]),
        ("IMAGING", [("upload", "📸  Upload Study"),
                     ("studies", "📂  All Studies")]),
        ("PATIENTS", [("all_patients", "☰  All Patients")]),
    ]
    PANEL_MAP = {
        "dashboard": "_panel_dashboard",
        "upload": "_panel_upload",
        "studies": "_panel_studies",
        "all_patients": "_panel_all_patients",
    }

    def _panel_dashboard(self):
        p = self.content;
        self._page_title(p, "Radiology Dashboard", now_str())
        img = load_imaging()
        self._kpi_row(p, [("Studies Today", str(sum(1 for i in img if i.get("date", "").startswith(today_str()))), "📸",
                           self.accent)])

    def _panel_upload(self):
        p = self.content;
        self._page_title(p, "Upload Study", "Record imaging procedure details")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar();
        studyv = tk.StringVar();
        modalityv = tk.StringVar(value="X-Ray")
        tk.Label(inner, text="Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, pv, self._admitted_ids(), width=34).pack(anchor="w", pady=(2, 10))
        tk.Label(inner, text="Modality", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, modalityv, ["X-Ray", "CT Scan", "MRI", "Ultrasound", "PET Scan"], width=20).pack(anchor="w",
                                                                                                         pady=(2, 10))
        tk.Label(inner, text="Study Description", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        entry(inner, textvariable=studyv, width=40).pack(anchor="w", pady=(2, 14))

        def do():
            if not pv.get(): toast(self.root, "Select patient", "error"); return
            img = load_imaging()
            img.append({"patient_id": self._pid_from_combo(pv.get()), "patient_name": pv.get().split(" — ")[1],
                        "modality": modalityv.get(), "study": studyv.get(), "date": now_str(), "tech": self.username})
            save_imaging(img);
            toast(self.root, "Study recorded")

        btn(inner, "  Save Study", do).pack(anchor="w")

    def _panel_studies(self):
        p = self.content;
        self._page_title(p, "All Studies", "Imaging study log")
        img = load_imaging();
        cols = ("Date", "Patient", "Modality", "Study", "Technician");
        widths = [130, 140, 100, 200, 120]
        tf, tree = build_tree(p, cols, widths, height=18);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        rows = [(i["date"], i["patient_name"], i["modality"], i["study"], i["tech"]) for i in reversed(img)]
        self._populate_tree(tree, rows)


# ══════════════════════════════════════════════════════════════
#  9. RESPIRATORY THERAPIST
# ══════════════════════════════════════════════════════════════
class RespiratoryApp(BaseApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  RT Dashboard")]),
        ("THERAPY", [("log", "🫁  RT Log"),
                     ("history", "📜  History")]),
    ]
    PANEL_MAP = {"dashboard": "_panel_dashboard", "log": "_panel_log", "history": "_panel_history"}

    def _panel_dashboard(self):
        p = self.content;
        self._page_title(p, "Respiratory Therapy Dashboard", now_str())
        t = load_therapy();
        rt = [i for i in t if i["type"] == "Respiratory"]
        self._kpi_row(p, [
            ("Total Sessions", str(len(rt)), "🫁", self.accent),
            ("Patients Today", str(sum(1 for i in rt if i.get("date", "").startswith(today_str()))), "👥", C_BLUE),
        ])
        two = tk.Frame(p, bg=C_BG);
        two.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        left = tk.Frame(two, bg=C_BG);
        left.pack(side="left", fill="both", expand=True)
        label(left, "Recent Interventions", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        cols = ("Date", "Patient", "Mode", "By");
        widths = [130, 140, 200, 100]
        tf, tree = build_tree(left, cols, widths, height=12);
        tf.pack(fill="both", expand=True)
        rows = [(i["date"], i["patient"], i["mode"], i["by"]) for i in reversed(rt[-10:])]
        self._populate_tree(tree, rows)

    def _panel_log(self):
        p = self.content;
        self._page_title(p, "RT Log", "Record respiratory care")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar();
        modev = tk.StringVar();
        o2v = tk.StringVar()
        tk.Label(inner, text="Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, pv, self._admitted_ids(), width=34).pack(anchor="w", pady=(2, 10))
        tk.Label(inner, text="O2 Delivery / Mode", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        entry(inner, textvariable=modev, width=30).pack(anchor="w", pady=(2, 10))
        tk.Label(inner, text="O2 Saturation (%)", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        entry(inner, textvariable=o2v, width=10).pack(anchor="w", pady=(2, 14))

        def do():
            if not pv.get(): toast(self.root, "Select patient", "error"); return
            t = load_therapy();
            t.append(
                {"patient": pv.get(), "type": "Respiratory", "mode": modev.get(), "o2": o2v.get(), "date": now_str(),
                 "by": self.username})
            save_therapy(t);
            toast(self.root, "RT log saved")

        btn(inner, "  Save Log", do).pack(anchor="w")

    def _panel_history(self):
        p = self.content;
        self._page_title(p, "RT History", "Past respiratory interventions")
        t = load_therapy();
        rt = [i for i in t if i["type"] == "Respiratory"]
        cols = ("Date", "Patient", "Mode", "O2 %", "By");
        widths = [130, 140, 180, 70, 100]
        tf, tree = build_tree(p, cols, widths, height=18);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        rows = [(i["date"], i["patient"], i["mode"], i["o2"], i["by"]) for i in reversed(rt)]
        self._populate_tree(tree, rows)


# ══════════════════════════════════════════════════════════════
#  10. PHYSICAL THERAPIST
# ══════════════════════════════════════════════════════════════
class PhysicalApp(BaseApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  PT Dashboard")]),
        ("REHAB", [("session", "🏃  PT Session"),
                   ("history", "📜  History")]),
    ]
    PANEL_MAP = {"dashboard": "_panel_dashboard", "session": "_panel_session", "history": "_panel_history"}

    def _panel_dashboard(self):
        p = self.content;
        self._page_title(p, "Physical Therapy Dashboard", now_str())
        t = load_therapy();
        pt = [i for i in t if i["type"] == "Physical"]
        self._kpi_row(p, [
            ("Total Rehab", str(len(pt)), "🏃", self.accent),
            ("Sessions Today", str(sum(1 for i in pt if i.get("date", "").startswith(today_str()))), "📅", C_PURPLE),
        ])
        two = tk.Frame(p, bg=C_BG);
        two.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        left = tk.Frame(two, bg=C_BG);
        left.pack(side="left", fill="both", expand=True)
        label(left, "Rehab History", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        cols = ("Date", "Patient", "Note", "By");
        widths = [130, 140, 250, 100]
        tf, tree = build_tree(left, cols, widths, height=12);
        tf.pack(fill="both", expand=True)
        rows = [(i["date"], i["patient"], i["note"][:40], i["by"]) for i in reversed(pt[-10:])]
        self._populate_tree(tree, rows)

    def _panel_session(self):
        p = self.content;
        self._page_title(p, "PT Session", "Record rehabilitation session")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar();
        note_v = tk.StringVar()
        tk.Label(inner, text="Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, pv, self._admitted_ids(), width=34).pack(anchor="w", pady=(2, 10))
        tk.Label(inner, text="Session Notes / Progress", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(
            anchor="w")
        entry(inner, textvariable=note_v, width=50).pack(anchor="w", pady=(2, 14))

        def do():
            if not pv.get(): toast(self.root, "Select patient", "error"); return
            t = load_therapy();
            t.append(
                {"patient": pv.get(), "type": "Physical", "note": note_v.get(), "date": now_str(), "by": self.username})
            save_therapy(t);
            toast(self.root, "PT session saved")

        btn(inner, "  Save Session", do).pack(anchor="w")

    def _panel_history(self):
        p = self.content;
        self._page_title(p, "PT History", "Past physical therapy")
        t = load_therapy();
        pt = [i for i in t if i["type"] == "Physical"]
        cols = ("Date", "Patient", "Progress Note", "By");
        widths = [130, 140, 350, 100]
        tf, tree = build_tree(p, cols, widths, height=18);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        rows = [(i["date"], i["patient"], i["note"], i["by"]) for i in reversed(pt)]
        self._populate_tree(tree, rows)


# ══════════════════════════════════════════════════════════════
#  11. DIETITIAN
# ══════════════════════════════════════════════════════════════
class DietApp(BaseApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  Nutrition Dashboard")]),
        ("DIET", [("plan", "🥗  Diet Plan"),
                  ("history", "📜  Plan History")]),
    ]
    PANEL_MAP = {"dashboard": "_panel_dashboard", "plan": "_panel_plan", "history": "_panel_history"}

    def _panel_dashboard(self):
        p = self.content;
        self._page_title(p, "Dietitian Dashboard", now_str())
        d = load_diet()
        self._kpi_row(p, [
            ("Diet Plans", str(len(d)), "🥗", self.accent),
            ("Updated Today", str(sum(1 for i in d if i.get("date", "").startswith(today_str()))), "✓", C_SUCCESS),
        ])
        two = tk.Frame(p, bg=C_BG);
        two.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        left = tk.Frame(two, bg=C_BG);
        left.pack(side="left", fill="both", expand=True)
        label(left, "Current Nutritional Plans", font=FONT_H2, fg=C_TEXT, bg=C_BG).pack(anchor="w", pady=(0, 6))
        cols = ("Date", "Patient", "Diet", "By");
        widths = [130, 140, 150, 100]
        tf, tree = build_tree(left, cols, widths, height=12);
        tf.pack(fill="both", expand=True)
        rows = [(i["date"], i["patient"], i["diet"], i["by"]) for i in reversed(d[-10:])]
        self._populate_tree(tree, rows)

    def _panel_plan(self):
        p = self.content;
        self._page_title(p, "Diet Plan", "Set patient nutritional plan")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar();
        dietv = tk.StringVar();
        notesv = tk.StringVar()
        tk.Label(inner, text="Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, pv, self._admitted_ids(), width=34).pack(anchor="w", pady=(2, 10))
        tk.Label(inner, text="Diet Type", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, dietv, ["Regular", "Low Sodium", "Diabetic", "Liquid", "Soft", "High Protein"], width=20).pack(
            anchor="w", pady=(2, 10))
        tk.Label(inner, text="Special Instructions", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(
            anchor="w")
        entry(inner, textvariable=notesv, width=40).pack(anchor="w", pady=(2, 14))

        def do():
            if not pv.get(): toast(self.root, "Select patient", "error"); return
            d = load_diet();
            d.append({"patient": pv.get(), "diet": dietv.get(), "notes": notesv.get(), "date": now_str(),
                      "by": self.username})
            save_diet(d);
            toast(self.root, "Diet plan saved")

        btn(inner, "  Save Plan", do).pack(anchor="w")

    def _panel_history(self):
        p = self.content;
        self._page_title(p, "Diet History", "Past nutrition plans")
        d = load_diet();
        cols = ("Date", "Patient", "Diet Type", "Instructions", "By");
        widths = [130, 140, 100, 250, 100]
        tf, tree = build_tree(p, cols, widths, height=18);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        rows = [(i["date"], i["patient"], i["diet"], i["notes"], i["by"]) for i in reversed(d)]
        self._populate_tree(tree, rows)


# ══════════════════════════════════════════════════════════════
#  12. SOCIAL WORKER
# ══════════════════════════════════════════════════════════════
class SocialApp(BaseApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  Social Dashboard")]),
        ("CASES", [("notes", "🏠  Social Notes"),
                   ("history", "📜  Case History")]),
    ]
    PANEL_MAP = {"dashboard": "_panel_dashboard", "notes": "_panel_notes", "history": "_panel_history"}

    def _panel_dashboard(self):
        p = self.content;
        self._page_title(p, "Social Worker Dashboard", now_str())

    def _panel_notes(self):
        p = self.content;
        self._page_title(p, "Social Notes", "Record psychosocial assessment")
        card = card_frame(p);
        card.pack(padx=24, pady=8, fill="x")
        inner = tk.Frame(card, bg=C_CARD);
        inner.pack(padx=16, pady=16, fill="x")
        pv = tk.StringVar();
        note_v = tk.StringVar()
        tk.Label(inner, text="Patient", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        combobox(inner, pv, self._admitted_ids(), width=34).pack(anchor="w", pady=(2, 10))
        tk.Label(inner, text="Assessment / Notes", font=("Segoe UI", 8, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
        entry(inner, textvariable=note_v, width=50).pack(anchor="w", pady=(2, 14))

        def do():
            if not pv.get(): toast(self.root, "Select patient", "error"); return
            s = load_social();
            s.append({"patient": pv.get(), "note": note_v.get(), "date": now_str(), "by": self.username})
            save_social(s);
            toast(self.root, "Social notes saved")

        btn(inner, "  Save Notes", do).pack(anchor="w")

    def _panel_history(self):
        p = self.content;
        self._page_title(p, "Case History", "Past social assessments")
        s = load_social();
        cols = ("Date", "Patient", "Social Note", "By");
        widths = [130, 140, 350, 100]
        tf, tree = build_tree(p, cols, widths, height=18);
        tf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        rows = [(i["date"], i["patient"], i["note"], i["by"]) for i in reversed(s)]
        self._populate_tree(tree, rows)


# ══════════════════════════════════════════════════════════════
#  13. CASE MANAGER
# ══════════════════════════════════════════════════════════════
class CaseManagerApp(AdminApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  Case Dashboard")]),
        ("PATIENTS", [("all_patients", "☰  All Patients"),
                      ("search", "⌕  Search Patient")]),
        ("DISCHARGE", [("discharge", "→  Discharge Planning")]),
    ]
    PANEL_MAP = {
        "dashboard": "_panel_dashboard",
        "all_patients": "_panel_all_patients",
        "search": "_panel_search",
        "discharge": "_panel_discharge",
    }


# ══════════════════════════════════════════════════════════════
#  13. MORGUE ATTENDANT
# ══════════════════════════════════════════════════════════════
class MorgueAttendantApp(BaseApp):
    SIDEBAR_SECTIONS = [
        ("OVERVIEW", [("dashboard", "▦  Morgue Dashboard")]),
        ("MORGUE", [("morgue", "⚰️  Records"),
                    ("search", "⌕  Search Patient")]),
    ]
    PANEL_MAP = {
        "dashboard": "_panel_morgue",
        "morgue": "_panel_morgue",
        "search": "_panel_search",
    }


# ══════════════════════════════════════════════════════════════
#  DISPATCHER  — routes role → app class
# ══════════════════════════════════════════════════════════════
ROLE_APP_MAP = {
    "Administrator": AdminApp,
    "Doctor": DoctorApp,
    "Nurse": NurseApp,
    "HRIO": HRIOApp,
    "Pharmacist": PharmacistApp,
    "Resident/Intern": ResidentApp,
    "Lab Technician": LabApp,
    "Radiologic Technologist": RadiologyApp,
    "Respiratory Therapist": RespiratoryApp,
    "Physical Therapist": PhysicalApp,
    "Dietitian": DietApp,
    "Social Worker": SocialApp,
    "Case Manager": CaseManagerApp,
    "Morgue Attendant": MorgueAttendantApp,
}


def _launch_app(root):
    def launch(username, role):
        for w in root.winfo_children(): w.destroy()
        root.configure(bg=C_BG)
        app_class = ROLE_APP_MAP.get(role, AdminApp)
        app_class(root, username, role)

    return launch


def main():
    root = tk.Tk()
    root.configure(bg=C_BG)
    try:
        root.tk.call("tk", "scaling", 1.2)
    except Exception:
        pass
    LoginWindow(root, _launch_app(root))
    root.mainloop()


if __name__ == "__main__":
    main()