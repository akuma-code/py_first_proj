import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys


GRID_TYPES = {
    "skf":    (-45, -47),
    "simple": (30, 40),
    "hooks":  (40, 30),
}

def get_history_path():
    if getattr(sys, "frozen", False):
        # .exe — кладём рядом с exe-файлом
        base = os.path.dirname(sys.executable)
    else:
        # обычный .py
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "netcalculator_history.json")

HISTORY_FILE = get_history_path()

# --- Палитра ---
BG_COLOR        = "#1e1f26"
PANEL_COLOR     = "#282a36"
CARD_COLOR      = "#2f3141"
SUBBLOCK_COLOR  = "#2b2d3a"     # фон подблоков ввода
ACCENT_COLOR    = "#7aa2f7"
ACCENT_HOVER    = "#5c86e0"
TEXT_COLOR      = "#e6e6e6"
MUTED_COLOR     = "#9aa0b4"
ENTRY_BG        = "#1b1c22"
DANGER_COLOR    = "#f7768e"
DANGER_HOVER    = "#e05a72"
BORDER_COLOR    = "#3a3d4d"
BORDER_ACCENT   = "#4a4d60"

# --- Шрифты ---
FONT_MAIN   = ("Segoe UI", 11)
FONT_LABEL  = ("Segoe UI", 9)
FONT_ENTRY  = ("Segoe UI", 22, "bold")
FONT_TITLE  = ("Segoe UI", 16, "bold")
FONT_RESULT = ("Segoe UI", 15, "bold")

# --- Размеры ---
ENTRY_WIDTH_CHARS = 6
SELECTOR_ITEM_PADX = 22
SELECTOR_ITEM_PADY = 8

BORDER_THICKNESS = 1


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except (json.JSONDecodeError, OSError):
        pass
    return []


def save_history(cards_data):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(cards_data, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


# ---------- Базовый виджет с обводкой ----------

class BorderedFrame(tk.Frame):
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


# ---------- Пользовательские виджеты ----------

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
                text=gt,
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


class BigEntry(tk.Frame):
    """Поле ввода с крупным шрифтом и подписью снизу (без собственной обводки)."""

    def __init__(self, parent, label_text, width=ENTRY_WIDTH_CHARS):
        super().__init__(parent, bg=SUBBLOCK_COLOR)

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
            bg=SUBBLOCK_COLOR,
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


# ---------- Карточка результата ----------

class ResultCard(BorderedFrame):
    def __init__(self, parent, source_w, source_h, grid_type, on_delete, on_change):
        super().__init__(parent, bg=CARD_COLOR, border=BORDER_COLOR,
                         padx=16, pady=14)

        self.source_w = source_w
        self.source_h = source_h
        self.grid_type_var = tk.StringVar(value=grid_type)
        self.on_delete = on_delete
        self.on_change = on_change

        left = tk.Frame(self, bg=CARD_COLOR)
        left.pack(side="left", fill="both", expand=True)

        self.result_label = tk.Label(
            left, font=FONT_RESULT, bg=CARD_COLOR, fg=ACCENT_COLOR
        )
        self.result_label.pack(anchor="w")

        tk.Label(
            left,
            text=f"Источник: {source_w} × {source_h}",
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


# ---------- Приложение ----------

class NetCalculatorApp:
    def __init__(self, root):
        self.root = root
        root.title("netCalculator")
        root.geometry("560x640")
        root.configure(bg=BG_COLOR)
        root.minsize(500, 560)

        # === Верхняя панель ===
        top = BorderedFrame(root, bg=PANEL_COLOR, border=BORDER_COLOR,
                            padx=20, pady=20)
        top.pack(fill="x", padx=14, pady=(14, 8))

        tk.Label(
            top, text="netCalculator", font=FONT_TITLE,
            bg=PANEL_COLOR, fg=TEXT_COLOR
        ).grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(0, 16))

        # --- Подблок 1: поля ввода ---
        sub_inputs = BorderedFrame(top, bg=SUBBLOCK_COLOR, border=BORDER_COLOR,
                                   padx=16, pady=12)
        sub_inputs.grid(row=1, column=0, sticky="nsew")

        self.entry_w = BigEntry(sub_inputs, "ШИРИНА (sourceW)")
        self.entry_w.pack(side="left")

        tk.Label(
            sub_inputs, text="×", font=("Segoe UI", 22, "bold"),
            bg=SUBBLOCK_COLOR, fg=MUTED_COLOR
        ).pack(side="left", padx=16)

        self.entry_h = BigEntry(sub_inputs, "ВЫСОТА (sourceH)")
        self.entry_h.pack(side="left")

        # --- Подблок 2: кнопки действий ---
        sub_actions = BorderedFrame(top, bg=SUBBLOCK_COLOR, border=BORDER_COLOR,
                                    padx=16, pady=12)
        sub_actions.grid(row=1, column=1, sticky="nsew", padx=(12, 0))

        # Кнопки центрируем по вертикали
        inner_actions = tk.Frame(sub_actions, bg=SUBBLOCK_COLOR)
        inner_actions.pack(expand=True)

        HoverButton(
            inner_actions, text="Посчитать", command=self.calculate,
            bg=ACCENT_COLOR, hover_bg=ACCENT_HOVER, pady=12,
            border=BORDER_COLOR,
        ).pack(pady=(0, 8))

        HoverButton(
            inner_actions, text="Удалить все", command=self.clear_all,
            bg=ENTRY_BG, hover_bg=DANGER_COLOR, fg=MUTED_COLOR, pady=12,
            border=BORDER_COLOR,
        ).pack()

        # --- Подблок 3: переключатель типа сетки ---
        sub_grid = BorderedFrame(top, bg=SUBBLOCK_COLOR, border=BORDER_COLOR,
                                 padx=16, pady=12)
        sub_grid.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(12, 0))

        self.grid_type_var = tk.StringVar(value="skf")
        self.selector = GridTypeSelector(sub_grid, self.grid_type_var, stretch=True)
        self.selector.pack(fill="x")

        tk.Label(
            sub_grid, text="ТИП СЕТКИ", font=FONT_LABEL,
            bg=SUBBLOCK_COLOR, fg=MUTED_COLOR
        ).pack(pady=(6, 0))

        # Растягиваем подблоки по ширине
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=0)

        # === Список карточек ===
        list_wrap = BorderedFrame(root, bg=BG_COLOR, border=BORDER_COLOR,
                                  padx=6, pady=6)
        list_wrap.pack(fill="both", expand=True, padx=14, pady=(6, 14))

        self.canvas = tk.Canvas(list_wrap, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_wrap, orient="vertical",
                                  command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y", padx=(0, 4), pady=4)
        self.canvas.pack(side="left", fill="both", expand=True,
                         padx=(4, 0), pady=4)

        self.cards_frame = tk.Frame(self.canvas, bg=BG_COLOR)
        self.cards_window = self.canvas.create_window(
            (0, 0), window=self.cards_frame, anchor="nw"
        )

        self.cards_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(self.cards_window, width=e.width),
        )

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        self.entry_w.bind_enter(self._on_enter)
        self.entry_h.bind_enter(self._on_enter)

        self._load_cards()

    # ---------- Прокрутка ----------
    def _on_mousewheel(self, event):
        if self.cards_frame.winfo_height() > self.canvas.winfo_height():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ---------- Enter ----------
    def _on_enter(self, event):
        self.calculate()
        self.entry_w.clear()
        self.entry_h.clear()
        self.entry_w.focus()
        return "break"

    # ---------- Логика ----------
    def calculate(self):
        try:
            w = int(self.entry_w.get())
            h = int(self.entry_h.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Ширина и высота должны быть целыми числами!")
            return

        if w <= 0 or h <= 0:
            messagebox.showerror("Ошибка", "Ширина и высота должны быть больше нуля!")
            return

        grid_type = self.grid_type_var.get()
        dw, dh = GRID_TYPES[grid_type]
        result_w = w + dw
        result_h = h + dh

        if result_w <= 0 or result_h <= 0:
            messagebox.showerror(
                "Ошибка",
                f"Результат получился недопустимым: {result_w} × {result_h}.\n"
                f"Для типа '{grid_type}' минимальные размеры источника: "
                f"{abs(dw) + 1} × {abs(dh) + 1}.",
            )
            return

        self._add_card(w, h, grid_type)
        self._save_cards()

    def _add_card(self, w, h, grid_type):
        card = ResultCard(
            self.cards_frame,
            source_w=w,
            source_h=h,
            grid_type=grid_type,
            on_delete=self.delete_card,
            on_change=self._save_cards,
        )
        card.pack(fill="x", pady=6, padx=2)
        return card

    def delete_card(self, card):
        card.destroy()
        self._save_cards()

    def clear_all(self):
        if not self.cards_frame.winfo_children():
            return
        if not messagebox.askyesno("Подтверждение", "Удалить все карточки?"):
            return
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        self._save_cards()

    # ---------- История ----------
    def _save_cards(self):
        data = [
            card.to_dict()
            for card in self.cards_frame.winfo_children()
            if isinstance(card, ResultCard)
        ]
        save_history(data)

    def _load_cards(self):
        for item in load_history():
            try:
                w = int(item["sourceW"])
                h = int(item["sourceH"])
                gt = item["gridType"]
                if gt not in GRID_TYPES:
                    gt = "skf"
            except (KeyError, TypeError, ValueError):
                continue
            self._add_card(w, h, gt)


if __name__ == "__main__":
    root = tk.Tk()
    app = NetCalculatorApp(root)
    root.mainloop()