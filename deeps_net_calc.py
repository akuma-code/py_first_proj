import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
from src.THEME import *
from src.Frames.HoverButton import HoverButton
from src.Frames.ResultCard import ResultCard
from src.Frames.TypeSelector import GridTypeSelector
from src.Frames.MainFrame import BorderedFrame
from src.Frames.BigEntry import BigEntry


def get_history_path():
    """Возвращает путь к JSON-файлу истории.
    Windows: %APPDATA%\\netCalculator\\netcalculator_history.json
    Linux/macOS: ~/.netCalculator/netcalculator_history.json    """
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    else:
        base = os.path.expanduser("~")

    folder = os.path.join(base, "netCalculator")
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError:
        # Если по какой-то причине не удалось создать папку —
        # падаем обратно в текущую директорию
        folder = os.path.abspath(".")

    return os.path.join(folder, "netcalculator_history.json")




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

# ---------- Файл сохранения ----------

HISTORY_FILE = get_history_path()

# ---------- Приложение ----------

class NetCalculatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Калькулятор москиток")
        # root.geometry("700x800")
        root.configure(bg=BG_COLOR)
        root.minsize(650, 800)
        root.resizable(True, True)
        root.update_idletasks()
        root.geometry(f"650x{root.winfo_reqheight()}")
        # === Верхняя панель ===
        top = BorderedFrame(root, bg=PANEL_COLOR, border=BORDER_COLOR,
                            padx=20, pady=20)
        top.pack(fill="x", padx=14, pady=(14, 8))

        tk.Label(
            top, text="Расчет сеток по световому проему", font=FONT_TITLE,
            bg=PANEL_COLOR, fg=TEXT_COLOR
        ).grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(0, 16))

        # --- Подблок 1: поля ввода ---
        sub_inputs = BorderedFrame(top, bg=PANEL_COLOR, border=BORDER_COLOR, thickness=0,
                                   padx=16, pady=12)
        sub_inputs.grid(row=1, column=0, sticky="nsew")

        self.entry_w = BigEntry(sub_inputs, "ШИРИНА")
        self.entry_w.pack(side="left",expand=True)

        tk.Label(
            sub_inputs, text="×", font=("Segoe UI", 22, "bold"),
            bg=PANEL_COLOR, fg=MUTED_COLOR
        ).pack(side="left", padx=16, anchor="n", pady=10)

        self.entry_h = BigEntry(sub_inputs, "ВЫСОТА")
        self.entry_h.pack(side="left", expand=True)

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
        sub_grid = BorderedFrame(top, bg=SUBBLOCK_COLOR, border=BORDER_COLOR, thickness=0,
                                 padx=16, pady=12 )
        sub_grid.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(12, 0))

        self.grid_type_var = tk.StringVar(value="skf")
        self.selector = GridTypeSelector(sub_grid, self.grid_type_var, stretch=True)
        self.selector.pack(fill="x")

        
        # Растягиваем подблоки по ширине
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=0)

        # === Список карточек ===
        self.list_wrap = BorderedFrame(root, bg=BG_COLOR, border=BORDER_COLOR,
                                       padx=6, pady=6)
        # ВАЖНО: пока не пакуем. Управление видимостью — через _update_list_visibility().

        self.canvas = tk.Canvas(self.list_wrap, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.list_wrap, orient="vertical",
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
        self._update_list_visibility()

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
        self.entry_w.clear()
        self.entry_h.clear()
        self.entry_w.focus()

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
        next_index = len(self.cards_frame.winfo_children()) + 1
        card = ResultCard(
            self.cards_frame,
            index=next_index,
            source_w=w,
            source_h=h,
            grid_type=grid_type,
            on_delete=self.delete_card,
            on_change=self._save_cards,
        )
        card.pack(fill="x", pady=6, padx=2)
        self._update_list_visibility()
        return card

    def delete_card(self, card):
        card.destroy()
        self._renumber_cards()   # внутри вызывает _update_list_visibility()
        self._save_cards()



    def clear_all(self):
        if not self.cards_frame.winfo_children():
            return
        if not messagebox.askyesno("Подтверждение", "Удалить все карточки?"):
            return
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        self._save_cards()
        self._update_list_visibility()

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
    def _update_list_visibility(self):
        """Показывает контейнер карточек только если есть хотя бы одна карточка."""
        has_cards = any(
            isinstance(w, ResultCard)
            for w in self.cards_frame.winfo_children()
        )
        if has_cards and not self.list_wrap.winfo_ismapped():
            self.list_wrap.pack(fill="both", expand=True,
                                padx=14, pady=(6, 14))
        elif not has_cards and self.list_wrap.winfo_ismapped():
            self.list_wrap.pack_forget()
            self.root.update_idletasks()
            self.root.geometry(f"650x{min(self.root.winfo_reqheight(), 800)}")

    def _renumber_cards(self):
        """Перенумеровывает карточки и обновляет видимость списка."""
        for i, widget in enumerate(self.cards_frame.winfo_children(), start=1):
            if isinstance(widget, ResultCard):
                widget.set_index(i)
        self._update_list_visibility()


if __name__ == "__main__":
    root = tk.Tk()
    app = NetCalculatorApp(root)
    root.mainloop()