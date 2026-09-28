import tkinter as Tk
from tkinter import ttk, messagebox

from src.THEME import BORDER_COLOR, BORDER_THICKNESS, PANEL_COLOR



# ---------- Базовый виджет с обводкой ----------




class BorderedFrame(Tk.Frame):
    """Фрейм с настраиваемой обводкой и фоном."""

    def __init__(self, parent, bg=PANEL_COLOR, border=BORDER_COLOR,
                 thickness=BORDER_THICKNESS, **kwargs):
        super().__init__(
            parent,
            bg=bg,
            highlightthickness=thickness,
            highlightbackground=border,
            highlightcolor=border,
            bd=0,
            **kwargs,
        )