import tkinter as tk

from src.THEME import BORDER_THICKNESS, FONT_MAIN


class HoverButton(tk.Label):
    """Кнопка на основе Label с ховер-эффектом и опциональной обводкой."""

    def __init__(self, parent, text, command, bg, hover_bg, fg="#ffffff",
                 font=FONT_MAIN, padx=16, pady=8, border=None):
        kwargs = {}
        if border is not None:
            kwargs.update(
                highlightthickness=BORDER_THICKNESS,
                highlightbackground=border,
                highlightcolor=border,
                bd=0,
            )
        super().__init__(
            parent, text=text, bg=bg, fg=fg, font=font,
            padx=padx, pady=pady, cursor="hand2", **kwargs
        )
        self._bg = bg
        self._hover_bg = hover_bg
        self._command = command
        self.bind("<Button-1>", lambda e: self._command())
        self.bind("<Enter>", lambda e: self.config(bg=self._hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self._bg))