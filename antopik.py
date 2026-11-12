import json
import random
import tkinter as tk
from pathlib import Path

LESSONS_DIR = Path(__file__).parent / "lessons"
PROGRESS_FILE = Path(__file__).parent / "progress.json"  
REFRESH_INTERVAL_MS = 10 * 60 * 1000  # 10min 
BG = "#1c1c1e"
ACCENT = "#4cc9f0"

CATEGORY_COLORS = {
    "Vocabulary": "#4cc9f0",
    "Key expressions": "#f72585",
    "Grammar": "#f9c74f",
    "Culture": "#90be6d",
}
DEFAULT_CATEGORY_COLOR = "#a0a0a0"

# How likely a card is to be drawn, depending on its status
STATUS_WEIGHTS = {"review": 5, "new": 3, "known": 1}
STATUS_LABELS = {"review": "To review", "new": "New", "known": "Known", "hidden": "Hidden"}

def load_cards():
    all_cards = []
    for file in sorted(LESSONS_DIR.glob("*.json")):
        category = file.stem.replace("_", " ").capitalize()  # key_expressions -> Key expressions
        for card in json.loads(file.read_text(encoding="utf-8")):
            card.setdefault("category", category)
            all_cards.append(card)
    return all_cards


# Progress helpers
def load_progress():
    try:
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_progress():
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2),
                             encoding="utf-8")


def card_id(card):
    return f'{card["category"]}:{card["korean"]}'


def get_status(card):
    return progress.get(card_id(card), "new")


def set_status(card, status):
    progress[card_id(card)] = status
    save_progress()


cards = load_cards()
progress = load_progress()  
current = None

root = tk.Tk()
root.title("Korean Widget")
root.overrideredirect(True)          # no title bar
root.attributes("-topmost", True)    # always on top
root.configure(bg=BG)
root.geometry("+40+40")              # screen position

category_label = tk.Label(root, font=("Helvetica", 10, "bold"), bg=BG)
category_label.pack(padx=20, pady=(10, 0))

korean_label = tk.Label(root, font=("Apple SD Gothic Neo", 32, "bold"), fg="white", bg=BG)
romanization_label = tk.Label(root, font=("Helvetica", 14, "italic"), fg="gray", bg=BG)
meaning_label = tk.Label(root, font=("Helvetica", 16), fg=ACCENT, bg=BG)
for label in (korean_label, romanization_label, meaning_label):
    label.pack(padx=20, pady=4)


def next_word():
    global current
    visible = [c for c in cards if get_status(c) != "hidden"]
    if not visible:
        category_label.config(text="")
        korean_label.config(text="No cards left")
        romanization_label.config(text="")
        meaning_label.config(text="Right-click → Restore hidden cards")
        return

    # Weighted draw, avoiding the same card twice in a row
    pool = [c for c in visible if c is not current] or visible
    weights = [STATUS_WEIGHTS[get_status(c)] for c in pool]
    current = random.choices(pool, weights=weights, k=1)[0]

    category = current.get("category", "")
    category_label.config(text=category.upper(),
                          fg=CATEGORY_COLORS.get(category, DEFAULT_CATEGORY_COLOR))
    korean_label.config(text=current["korean"])
    romanization_label.config(text=current["romanization"])
    meaning_label.config(text=current["meaning"])


def schedule_refresh():
    next_word()
    root.after(REFRESH_INTERVAL_MS, schedule_refresh)


def section_title(parent, text):
    tk.Label(parent, text=text.upper(), font=("Helvetica", 11, "bold"),
             fg=ACCENT, bg=BG).pack(padx=30, pady=(18, 2), anchor="w")
    tk.Frame(parent, bg=ACCENT, height=1).pack(padx=30, fill="x")


def open_lesson(_event=None):
    card = current
    win = tk.Toplevel(root)
    win.title(card["korean"])
    win.configure(bg=BG)
    win.attributes("-topmost", True)
    win.bind("<Escape>", lambda e: win.destroy())

    category = card.get("category", "")
    if category:
        color = CATEGORY_COLORS.get(category, DEFAULT_CATEGORY_COLOR)
        tk.Label(win, text=category.upper(), font=("Helvetica", 11, "bold"),
                 fg=BG, bg=color, padx=12, pady=3).pack(pady=(20, 0))

    # Header
    tk.Label(win, text=card["korean"], font=("Apple SD Gothic Neo", 40, "bold"),
             fg="white", bg=BG).pack(padx=30, pady=(10, 0))
    tk.Label(win, text=f'{card["romanization"]}  ·  {card["meaning"]}',
             font=("Helvetica", 16), fg=ACCENT, bg=BG).pack(pady=(0, 5))

    # Current status
    tk.Label(win, text=f"Status: {STATUS_LABELS[get_status(card)]}",
             font=("Helvetica", 11), fg="gray", bg=BG).pack()

    # Explanation section
    if card.get("explanation"):
        section_title(win, "Explanation")
        tk.Label(win, text=card["explanation"], font=("Helvetica", 14), fg="white",
                 bg=BG, wraplength=420, justify="left").pack(padx=30, pady=(8, 0), anchor="w")

    # Examples section
    if card.get("examples"):
        section_title(win, "Examples")
        for example in card["examples"]:
            tk.Label(win, text=example["korean"], font=("Apple SD Gothic Neo", 18),
                     fg="white", bg=BG).pack(padx=30, pady=(8, 0), anchor="w")
            if example.get("pronunciation"):
                tk.Label(win, text=example["pronunciation"], font=("Helvetica", 12),
                         fg=ACCENT, bg=BG).pack(padx=30, anchor="w")
            if example.get("english"):
                tk.Label(win, text=example["english"], font=("Helvetica", 12, "italic"),
                         fg="gray", bg=BG).pack(padx=30, anchor="w")

    # Tip section (optional)
    if card.get("tip"):
        section_title(win, "Memory tip")
        tk.Label(win, text=card["tip"], font=("Helvetica", 14), fg="white",
                 bg=BG, wraplength=420, justify="left").pack(padx=30, pady=(8, 0), anchor="w")

    # Known / To review / Hide buttons
    def mark(status):
        set_status(card, status)
        win.destroy()
        if status == "hidden":
            next_word()

    buttons = tk.Frame(win, bg=BG)
    buttons.pack(pady=20)
    tk.Button(buttons, text="✓ Known", command=lambda: mark("known")).pack(side="left", padx=5)
    tk.Button(buttons, text="↻ To review", command=lambda: mark("review")).pack(side="left", padx=5)
    tk.Button(buttons, text="✗ Hide", command=lambda: mark("hidden")).pack(side="left", padx=5)
    tk.Button(buttons, text="Close (Esc)", command=win.destroy).pack(side="left", padx=5)

def restore_hidden():
    for key in [k for k, v in progress.items() if v == "hidden"]:
        del progress[key]  # back to "new"
    save_progress()
    next_word()

menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Next word", command=next_word)
menu.add_command(label="Restore hidden cards", command=restore_hidden)
menu.add_command(label="Quit", command=root.destroy)


def show_menu(event):
    menu.tk_popup(event.x_root, event.y_root)


root.bind("<Button-1>", open_lesson)              # left click = open lesson
root.bind("<Button-2>", show_menu)                # right click (macOS)
root.bind("<Button-3>", show_menu)                # right click (other OS)
root.bind("<Control-Button-1>", show_menu)        # ctrl + click (macOS)

schedule_refresh()
root.mainloop()