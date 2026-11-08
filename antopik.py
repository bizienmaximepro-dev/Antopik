import json
import random
import tkinter as tk
from pathlib import Path

LESSONS_DIR = Path(__file__).parent / "lessons"
REFRESH_INTERVAL_MS = 60 * 60 * 1000  # 1 hour
BG = "#1c1c1e"
ACCENT = "#4cc9f0"

# NEW: one color per category
CATEGORY_COLORS = {
    "Vocabulary": "#4cc9f0",
    "Key expressions": "#f72585",
    "Grammar": "#f9c74f",
    "Culture": "#90be6d",
}
DEFAULT_CATEGORY_COLOR = "#a0a0a0"


def load_cards():
    all_cards = []
    for file in sorted(LESSONS_DIR.glob("*.json")):
        category = file.stem.replace("_", " ").capitalize()  # key_expressions -> Key expressions
        for card in json.loads(file.read_text(encoding="utf-8")):
            card.setdefault("category", category)
            all_cards.append(card)
    return all_cards


cards = load_cards()
current = None

root = tk.Tk()
root.title("Korean Widget")
root.overrideredirect(True)          # no title bar
root.attributes("-topmost", True)    # always on top
root.configure(bg=BG)
root.geometry("+40+40")              # screen position

# NEW: category label, packed BEFORE the other labels so it sits on top
category_label = tk.Label(root, font=("Helvetica", 10, "bold"), bg=BG)
category_label.pack(padx=20, pady=(10, 0))

korean_label = tk.Label(root, font=("Apple SD Gothic Neo", 32, "bold"), fg="white", bg=BG)
romanization_label = tk.Label(root, font=("Helvetica", 14, "italic"), fg="gray", bg=BG)
meaning_label = tk.Label(root, font=("Helvetica", 16), fg=ACCENT, bg=BG)
for label in (korean_label, romanization_label, meaning_label):
    label.pack(padx=20, pady=4)


def next_word():
    global current
    current = random.choice(cards)
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

    # NEW: category badge at the top of the card
    category = card.get("category", "")
    if category:
        color = CATEGORY_COLORS.get(category, DEFAULT_CATEGORY_COLOR)
        tk.Label(win, text=category.upper(), font=("Helvetica", 11, "bold"),
                 fg=BG, bg=color, padx=12, pady=3).pack(pady=(20, 0))

    # Header (pady changed from (20, 0) to (10, 0))
    tk.Label(win, text=card["korean"], font=("Apple SD Gothic Neo", 40, "bold"),
             fg="white", bg=BG).pack(padx=30, pady=(10, 0))
    tk.Label(win, text=f'{card["romanization"]}  ·  {card["meaning"]}',
             font=("Helvetica", 16), fg=ACCENT, bg=BG).pack(pady=(0, 5))

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
            tk.Label(win, text=example["english"], font=("Helvetica", 12, "italic"),
                     fg="gray", bg=BG).pack(padx=30, anchor="w")

    # Tip section (optional)
    if card.get("tip"):
        section_title(win, "Memory tip")
        tk.Label(win, text=card["tip"], font=("Helvetica", 14), fg="white",
                 bg=BG, wraplength=420, justify="left").pack(padx=30, pady=(8, 0), anchor="w")

    tk.Button(win, text="Close (Esc)", command=win.destroy).pack(pady=20)


menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Next word", command=next_word)
menu.add_command(label="Quit", command=root.destroy)


def show_menu(event):
    menu.tk_popup(event.x_root, event.y_root)


root.bind("<Button-1>", open_lesson)              # left click = open lesson
root.bind("<Button-2>", show_menu)                # right click (macOS)
root.bind("<Button-3>", show_menu)                # right click (other OS)
root.bind("<Control-Button-1>", show_menu)        # ctrl + click (macOS)

schedule_refresh()
root.mainloop()