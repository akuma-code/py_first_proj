from src.THEME import ACCENT_COLOR, BORDER_COLOR, ENTRY_BG, FONT_MAIN, GRID_TYPES, MUTED_COLOR, NET_NAME, SELECTOR_ITEM_PADX, SELECTOR_ITEM_PADY, SUBBLOCK_COLOR
from src.Frames.MainFrame import BorderedFrame
import tkinter as tk


class GridTypeSelector(BorderedFrame):
    """Переключатель типа сетки в виде группы кнопок (segmented control)."""

    def __init__(self, parent, variable, command=None, stretch=False):
        super().__init__(parent, bg=SUBBLOCK_COLOR, border=BORDER_COLOR)
        self.var = variable
        self.command = command
        self.buttons = {}

        self.columnconfigure(tuple(range(len(GRID_TYPES))), weight=1)

        for i, gt in enumerate(GRID_TYPES):
            btn = tk.Label(
                self,
                text=NET_NAME[gt],
                font=FONT_MAIN,
                bg=SUBBLOCK_COLOR,
                fg=MUTED_COLOR,
                padx=SELECTOR_ITEM_PADX,
                pady=SELECTOR_ITEM_PADY,
                cursor="hand2",
            )
            if stretch:
                btn.grid(row=0, column=i, sticky="ew", padx=1, pady=1)
            else:
                btn.pack(side="left", padx=2, pady=2)
            btn.bind("<Button-1>", lambda e, g=gt: self.select(g))
            btn.bind("<Enter>", lambda e, g=gt: self._hover(g, True))
            btn.bind("<Leave>", lambda e, g=gt: self._hover(g, False))
            self.buttons[gt] = btn

        self.var.trace_add("write", lambda *_: self._refresh())
        self._refresh()

    def _hover(self, gt, entering):
        if self.var.get() == gt:
            return
        self.buttons[gt].config(bg=ENTRY_BG if entering else SUBBLOCK_COLOR)

    def select(self, gt):
        self.var.set(gt)
        if self.command:
            self.command()

    def _refresh(self):
        for gt, btn in self.buttons.items():
            if self.var.get() == gt:
                btn.config(bg=ACCENT_COLOR, fg="#ffffff")
            else:
                btn.config(bg=SUBBLOCK_COLOR, fg=MUTED_COLOR)