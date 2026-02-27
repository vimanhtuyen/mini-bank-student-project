import tkinter as tk
from tkinter import ttk, messagebox

from src.ui.ui_helpers import read_positive_integer, format_money_vnd


class MoneyDialog(tk.Toplevel):
    """Cửa sổ nạp/rút tiền (V2).

    - Hiển thị số dư hiện tại
    - Xác nhận trước khi thực hiện
    """

    def __init__(self, parent, title_text: str, current_balance: int, submit_callback):
        super().__init__(parent)
        self.title(title_text)
        self.geometry("460x270")
        self.resizable(False, False)

        self.title_text = title_text
        self.current_balance = int(current_balance)
        self.submit_callback = submit_callback

        ttk.Label(self, text=title_text, font=("Segoe UI", 12, "bold")).pack(pady=10)

        balance_text = f"Số dư hiện tại: {format_money_vnd(self.current_balance)}"
        ttk.Label(self, text=balance_text).pack(pady=2)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Số tiền (VNĐ):").grid(row=0, column=0, sticky="w", pady=6)
        self.amount_entry = ttk.Entry(form, width=30)
        self.amount_entry.grid(row=0, column=1, pady=6)

        ttk.Label(form, text="Ghi chú:").grid(row=1, column=0, sticky="w", pady=6)
        self.note_entry = ttk.Entry(form, width=30)
        self.note_entry.grid(row=1, column=1, pady=6)
        self.note_entry.insert(0, "")

        self.hint_label = ttk.Label(self, text="", foreground="gray")
        self.hint_label.pack(pady=4)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Xác nhận", command=self.on_submit, width=16).grid(row=0, column=0, padx=8)
        ttk.Button(button_frame, text="Đóng", command=self.destroy, width=16).grid(row=0, column=1, padx=8)

        self.amount_entry.bind("<KeyRelease>", self.on_amount_change)

    def on_amount_change(self, event=None) -> None:
        amount = read_positive_integer(self.amount_entry.get())
        if amount == -1:
            self.hint_label.configure(text="Gợi ý: nhập số nguyên dương, ví dụ 50000.")
            return

        if "Rút" in self.title_text and amount > self.current_balance:
            self.hint_label.configure(text="Cảnh báo: số tiền rút lớn hơn số dư.")
            return

        self.hint_label.configure(text="")

    def on_submit(self) -> None:
        amount = read_positive_integer(self.amount_entry.get())
        note = self.note_entry.get().strip()

        if amount == -1:
            messagebox.showwarning("Lỗi nhập liệu", "Số tiền phải là số nguyên dương.")
            return

        if "Rút" in self.title_text and amount > self.current_balance:
            messagebox.showwarning("Không đủ số dư", "Số tiền rút lớn hơn số dư hiện tại.")
            return

        confirm = messagebox.askyesno("Xác nhận", f"{self.title_text} {format_money_vnd(amount)} ?")
        if not confirm:
            return

        ok, message = self.submit_callback(amount, note)
        if ok:
            messagebox.showinfo("Thành công", message)
            self.destroy()
        else:
            messagebox.showwarning("Không thành công", message)
