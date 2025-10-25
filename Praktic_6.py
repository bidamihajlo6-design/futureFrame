# -*- coding: utf-8 -*-
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, List, Optional

DATA_FILES = {
    "Математика": "questions_math.json",
    "Українська мова": "questions_ukr.json",
    "Історія": "questions_hist.json",
}



class Question:
    def __init__(self, text: str, options: List[str], answer: int) -> None:
        self.text = text
        self.options = options
        self.answer = answer


class TestData:
    def __init__(self, title: str, time_seconds: int, questions: List[Question]) -> None:
        self.title = title
        self.time_seconds = time_seconds
        self.questions = questions


def _read_text_with_fallback(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read()
    except Exception:
        pass

    try:
        from charset_normalizer import from_bytes  # type: ignore
    except Exception:
        from_charset = None
    else:
        try:
            with open(path, "rb") as f:
                raw = f.read()
            match = from_bytes(raw).best()
            if match and match.encoding:
                try:
                    return raw.decode(match.encoding, errors="replace")
                except Exception:
                    pass
        except Exception:
            pass

    try:
        with open(path, "r", encoding="cp1251", errors="replace") as f:
            return f.read()
    except Exception:
        pass

    try:
        with open(path, "r", encoding="latin-1", errors="replace") as f:
            return f.read()
    except Exception:
        pass

    return None


def load_test_from_file(path: str) -> Optional[TestData]:
    if not path or not os.path.exists(path):
        return None
    txt = _read_text_with_fallback(path)
    if txt is None:
        return None
    try:
        data = json.loads(txt)
    except Exception:
        return None
    questions = [
        Question(q["text"], q["options"], int(q.get("answer", 0)))
        for q in data.get("questions", [])
    ]
    return TestData(data.get("title", "Тест"), int(data.get("time_seconds", 300)), questions)


class QuizFrame(ttk.Frame):
    def __init__(self, parent, test_data: TestData, on_back) -> None:
        super().__init__(parent)
        self.parent = parent
        self.test_data = test_data
        self.on_back = on_back
        self.total_questions = len(test_data.questions)
        self.current_index = 0
        self.answers: Dict[int, Optional[int]] = {i: None for i in range(self.total_questions)}
        self.remaining = test_data.time_seconds
        self.timer_id = None
        self.selected_var = tk.IntVar(value=-1)
        self._build_ui()
        self._display_question()
        self._start_timer()

    def _build_ui(self) -> None:
        title_label = ttk.Label(self, text=self.test_data.title, font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(10, 5))
        self.timer_label = ttk.Label(self, text="", font=("Arial", 12))
        self.timer_label.grid(row=0, column=3, sticky="e", padx=10)
        self.q_label = ttk.Label(self, text="", wraplength=700, font=("Arial", 12))
        self.q_label.grid(row=1, column=0, columnspan=4, pady=(10, 10), padx=10)
        self.options_frame = ttk.Frame(self)
        self.options_frame.grid(row=2, column=0, columnspan=4, padx=10, sticky="w")
        nav_frame = ttk.Frame(self)
        nav_frame.grid(row=3, column=0, columnspan=4, pady=10)
        self.prev_btn = ttk.Button(nav_frame, text="Попереднє", command=self._previous)
        self.prev_btn.grid(row=0, column=0, padx=5)
        self.next_btn = ttk.Button(nav_frame, text="Наступне", command=self._next)
        self.next_btn.grid(row=0, column=1, padx=5)
        self.submit_btn = ttk.Button(nav_frame, text="Здати", command=self._submit)
        self.submit_btn.grid(row=0, column=2, padx=5)
        self.back_btn = ttk.Button(nav_frame, text="Меню", command=self._back_to_menu)
        self.back_btn.grid(row=0, column=3, padx=5)
        self.counter_label = ttk.Label(self, text="")
        self.counter_label.grid(row=4, column=0, columnspan=4, pady=(5, 10))

    def _display_question(self) -> None:
        q = self.test_data.questions[self.current_index]
        self.q_label.config(text=f"Питання {self.current_index + 1}: {q.text}")
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        prev = self.answers.get(self.current_index)
        self.selected_var.set(prev if prev is not None else -1)
        for idx, opt in enumerate(q.options):
            rb = ttk.Radiobutton(
                self.options_frame,
                text=opt,
                variable=self.selected_var,
                value=idx,
                command=self._store_answer,
            )
            rb.pack(anchor="w", pady=2)
        self._update_nav_buttons()
        self._update_counter()

    def _store_answer(self) -> None:
        val = self.selected_var.get()
        if val >= 0:
            self.answers[self.current_index] = int(val)

    def _update_nav_buttons(self) -> None:
        self.prev_btn.config(state="normal" if self.current_index > 0 else "disabled")
        self.next_btn.config(state="normal" if self.current_index < self.total_questions - 1 else "disabled")

    def _update_counter(self) -> None:
        self.counter_label.config(text=f"Питання {self.current_index + 1} з {self.total_questions}")

    def _previous(self) -> None:
        self._store_answer()
        if self.current_index > 0:
            self.current_index -= 1
            self._display_question()

    def _next(self) -> None:
        self._store_answer()
        if self.current_index < self.total_questions - 1:
            self.current_index += 1
            self._display_question()

    def _submit(self) -> None:
        self._store_answer()
        correct = 0
        for i, q in enumerate(self.test_data.questions):
            if self.answers.get(i) is not None and int(self.answers[i]) == int(q.answer):
                correct += 1
        total = self.total_questions
        percent = int(correct / total * 100) if total > 0 else 0
        messagebox.showinfo("Результат", f"Правильних: {correct} з {total}\nОцінка: {percent}%")
        self._stop_timer()
        self.on_back()

    def _back_to_menu(self) -> None:
        if messagebox.askyesno("Підтвердження", "Повернутися в меню? Прогрес не буде збережено"):
            self._stop_timer()
            self.on_back()

    def _start_timer(self) -> None:
        self._tick()

    def _tick(self) -> None:
        mins, secs = divmod(self.remaining, 60)
        self.timer_label.config(text=f"Час залишилось {mins:02d}:{secs:02d}")
        if self.remaining <= 0:
            messagebox.showinfo("Час вичерпано", "Час тесту вичерпано. Тест буде відправлено автоматично.")
            self._submit()
            return
        self.remaining -= 1
        self.timer_id = self.after(1000, self._tick)

    def _stop_timer(self) -> None:
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None


class MainApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("NMT Prep Tests")
        self.geometry("800x500")
        self.resizable(False, False)
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self._show_main_menu()

    def _show_main_menu(self) -> None:
        for widget in self.container.winfo_children():
            widget.destroy()
        frame = ttk.Frame(self.container)
        frame.pack(expand=True)
        label = ttk.Label(frame, text="Виберіть тест", font=("Arial", 18))
        label.pack(pady=20)
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        for key in ("Математика", "Українська мова", "Історія"):
            b = ttk.Button(
                btn_frame,
                text=key,
                command=lambda k=key: self._start_test(k),
                width=24,
            )
            b.pack(pady=8)
        quit_btn = ttk.Button(frame, text="Вийти", command=self.destroy)
        quit_btn.pack(pady=20)

    def _start_test(self, key: str) -> None:
        filename = DATA_FILES.get(key)
        test = load_test_from_file(filename) if filename else None
        if test is None or not test.questions:
            messagebox.showerror("Помилка", f"Не знайдено або порожній файл для тесту {key}")
            return
        for widget in self.container.winfo_children():
            widget.destroy()
        quiz = QuizFrame(self.container, test, on_back=self._show_main_menu)
        quiz.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
