import json
import random
import tkinter as tk
from pathlib import Path

LESSONS_FILE = Path(__file__).parent / "lessons.json"
REFRESH_INTERVAL_MS = 60 * 60 * 1000  # 1 hour
BG = "#1c1c1e"
ACCENT = "#4cc9f0"

cards = json.loads(LESSONS_FILE.read_text(encoding="utf-8"))
current = None

root = tk.Tk()
root.title("Korean Widget")
root.overrideredirect(True)          # no title bar
root.attributes("-topmost", True)    # always on top
root.configure(bg=BG)
root.geometry("+40+40")              # screen position

korean_label = tk.Label(root, font=("Apple SD Gothic Neo", 32, "bold"), fg="white", bg=BG)
romanization_label = tk.Label(root, font=("Helvetica", 14, "italic"), fg="gray", bg=BG)
meaning_label = tk.Label(root, font=("Helvetica", 16), fg=ACCENT, bg=BG)
for label in (korean_label, romanization_label, meaning_label):
    label.pack(padx=20, pady=4)


def next_word():
    global current
    current = random.choice(cards)
    korean_label.config(text=current["korean"])
    romanization_label.config(text=current["romanization"])
    meaning_label.config(text=current["meaning"])


def schedule_refresh():
    next_word()
    root.after(REFRESH_INTERVAL_MS, schedule_refresh)


def open_lesson(_event=None):
    card = current
    win = tk.Toplevel(root)
    win.title(card["korean"])
    win.configure(bg=BG)
    win.attributes("-topmost", True)
    win.bind("<Escape>", lambda e: win.destroy())

    tk.Label(win, text=card["korean"], font=("Apple SD Gothic Neo", 40, "bold"),
             fg="white", bg=BG).pack(padx=30, pady=(20, 0))
    tk.Label(win, text=f'{card["romanization"]}  ·  {card["meaning"]}',
             font=("Helvetica", 16), fg=ACCENT, bg=BG).pack(pady=(0, 10))
    tk.Label(win, text=card.get("lesson", ""), font=("Helvetica", 14), fg="white",
             bg=BG, wraplength=420, justify="left").pack(padx=30, pady=10)

    for example in card.get("examples", []):
        tk.Label(win, text=example["korean"], font=("Apple SD Gothic Neo", 18),
                 fg="white", bg=BG).pack(padx=30, anchor="w")
        tk.Label(win, text=example["english"], font=("Helvetica", 12, "italic"),
                 fg="gray", bg=BG).pack(padx=30, pady=(0, 8), anchor="w")

    tk.Button(win, text="Close (Esc)", command=win.destroy).pack(pady=15)


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