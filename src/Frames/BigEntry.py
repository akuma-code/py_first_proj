import tkinter as tk

from src.THEME import ACCENT_COLOR, ENTRY_BG, ENTRY_WIDTH_CHARS, FONT_ENTRY, FONT_LABEL, MUTED_COLOR, PANEL_COLOR, TEXT_COLOR

class BigEntry(tk.Frame):
    """Поле ввода с крупным шрифтом и подписью снизу (без собственной обводки)."""

    def __init__(self, parent, label_text, width=ENTRY_WIDTH_CHARS):
        super().__init__(parent, bg=PANEL_COLOR)

        self.entry = tk.Entry(
            self,
            font=FONT_ENTRY,
            width=width,
            justify="center",
            bg=ENTRY_BG,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            highlightthickness=2,
            highlightbackground=ENTRY_BG,
            highlightcolor=ACCENT_COLOR,
            bd=0,
        )
        self.entry.pack(ipady=10, fill="x")

        tk.Label(
            self,
            text=label_text,
            font=FONT_LABEL,
            bg=PANEL_COLOR,
            fg=MUTED_COLOR,
        ).pack(pady=(4, 0), anchor="center")

    def get(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, tk.END)

    def focus(self):
        self.entry.focus_set()

    def bind_enter(self, callback):
        self.entry.bind("<Return>", callback)