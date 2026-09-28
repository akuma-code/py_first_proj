import tkinter as tk
from src.Frames.HoverButton import HoverButton
from src.Frames.MainFrame import BorderedFrame
from src.Frames.TypeSelector import GridTypeSelector
from src.THEME import ACCENT_COLOR, BORDER_COLOR, CARD_COLOR, DANGER_COLOR, FONT_LABEL, FONT_RESULT, GRID_TYPES, MUTED_COLOR

class ResultCard(BorderedFrame):
    def __init__(self, parent, index, source_w, source_h, grid_type,
                 on_delete, on_change):
        super().__init__(parent, bg=CARD_COLOR, border=BORDER_COLOR,
                         padx=16, pady=14)

        self.source_w = source_w
        self.source_h = source_h
        self.grid_type_var = tk.StringVar(value=grid_type)
        self.on_delete = on_delete
        self.on_change = on_change

        # --- Номер карточки ---
        self.index_label = tk.Label(
            self,
            text=f"#{index}",
            font=("Segoe UI", 18, "bold"),
            bg=CARD_COLOR,
            fg=MUTED_COLOR,
        )
        self.index_label.pack(side="left", padx=(0, 16))

        left = tk.Frame(self, bg=CARD_COLOR)
        left.pack(side="left", fill="both", expand=True)

        self.result_label = tk.Label(
            left, font=FONT_RESULT, bg=CARD_COLOR, fg=ACCENT_COLOR
        )
        self.result_label.pack(anchor="w")

        tk.Label(
            left,
            text=f"{source_w} × {source_h}",
            font=FONT_LABEL,
            bg=CARD_COLOR,
            fg=MUTED_COLOR,
        ).pack(anchor="w", pady=(4, 0))

        right = tk.Frame(self, bg=CARD_COLOR)
        right.pack(side="right")

        selector = GridTypeSelector(right, self.grid_type_var,
                                    command=self._on_grid_change)
        selector.pack(side="left", padx=(0, 12))

        HoverButton(
            right, text="✕", command=lambda: self.on_delete(self),
            bg=CARD_COLOR, hover_bg=DANGER_COLOR, fg=DANGER_COLOR,
            font=("Segoe UI", 12, "bold"), padx=10, pady=6,
            border=BORDER_COLOR,
        ).pack(side="left")

        self.update_result()

    def set_index(self, index):
        """Обновляет отображаемый номер карточки."""
        self.index_label.config(text=f"#{index}")

    def _on_grid_change(self):
        self.update_result()
        self.on_change()

    def update_result(self):
        dw, dh = GRID_TYPES[self.grid_type_var.get()]
        w = self.source_w + dw
        h = self.source_h + dh
        self.result_label.config(text=f"{w} × {h}")

    def to_dict(self):
        return {
            "sourceW": self.source_w,
            "sourceH": self.source_h,
            "gridType": self.grid_type_var.get(),
        }