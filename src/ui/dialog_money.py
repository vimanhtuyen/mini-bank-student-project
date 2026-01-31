import tkinter as tk
from tkinter import ttk, messagebox

from src.ui.ui_helpers import read_positive_integer


class MoneyDialog(tk.Toplevel):

    def __init__(self, parent, title_text: str, submit_callback):
        super().__init__(parent)
        self.title(title_text)
        self.geometry("400x200")
        self.resizable(False, False)

        self.submit_callback = submit_callback

        ttk.Label(self, text=title_text, font=("Segoe UI", 12, "bold")).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=8)

        ttk.Label(form, text="So tien (VND):").grid(row=0, column=0, sticky="w", pady=6)
        self.amount_entry = ttk.Entry(form, width=28)
        self.amount_entry.grid(row=0, column=1, pady=6)

        ttk.Label(form, text="Ghi chu").grid(row=1, column=0, sticky="w", pady=6)
        self.note_entry = ttk.Entry(form, width=28)
        self.note_entry.grid(row=1, column=1, pady=6)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Xac nhan", command=self.on_submit, width=16).grid(row=0, column=0, padx=8)
        ttk.Button(button_frame, text="Huy bo", command=self.destroy, width=16).grid(row=0, column=1, padx=8)

    def on_submit(self) -> None:
        amount = read_positive_integer(self.amount_entry.get())
        note = self.note_entry.get().strip()

        if amount == -1:
            messagebox.showwarning("So tien khong hop le")
            return

        ok, message = self.submit_callback(amount, note)
        if ok:
            messagebox.showinfo("Thanh cong", message)
            self.destroy()
        else:
            messagebox.showwarning("Khong thanh cong", message)