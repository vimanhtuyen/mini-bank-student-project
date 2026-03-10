import tkinter as tk
from tkinter import ttk, messagebox

from src.ui.ui_helpers import read_positive_integer, format_money_vnd
import re  # new


class TransferDialog(tk.Toplevel):
    def __init__(self, parent, bank_service, from_account_id: str, success_callback):
        super().__init__(parent)
        self.title("Chuyển khoản")
        self.geometry("520x330")
        self.resizable(False, False)

        self.bank_service = bank_service
        self.from_account_id = str(from_account_id)
        self.success_callback = success_callback

        from_account = self.bank_service.get_account(self.from_account_id)
        self.from_balance = 0  # new
        from_name = ""
        if from_account is not None:
            self.from_balance = int(from_account.balance)  # new
            from_name = str(from_account.owner_name)

        ttk.Label(self, text="Chuyển khoản", font=("Segoe UI", 12, "bold")).pack(pady=10)

        ttk.Label(self, text=f"Tài khoản gửi: {self.from_account_id} ({from_name})").pack(pady=2)
        ttk.Label(self, text=f"Số dư hiện tại: {format_money_vnd(self.from_balance)}").pack(pady=2)

        form = ttk.Frame(self)
        form.pack(pady=12)

        ttk.Label(form, text="Số tài khoản nhận:").grid(row=0, column=0, sticky="w", pady=6)
        self.to_account_entry = ttk.Entry(form, width=30)
        self.to_account_entry.grid(row=0, column=1, pady=6)

        self.to_name_label = ttk.Label(form, text="Tên người nhận: (chưa nhập)", foreground="gray")
        self.to_name_label.grid(row=1, column=1, sticky="w", pady=2)

        ttk.Label(form, text="Số tiền (VNĐ):").grid(row=2, column=0, sticky="w", pady=6)
        self.amount_entry = ttk.Entry(form, width=30)
        self.amount_entry.grid(row=2, column=1, pady=6)

        ttk.Label(form, text="Ghi chú:").grid(row=3, column=0, sticky="w", pady=6)
        self.note_entry = ttk.Entry(form, width=30)
        self.note_entry.grid(row=3, column=1, pady=6)

        self.hint_label = ttk.Label(self, text="", foreground="gray")
        self.hint_label.pack(pady=4)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=12)

        ttk.Button(button_frame, text="Xác nhận", command=self.on_submit, width=16).grid(row=0, column=0, padx=8)
        ttk.Button(button_frame, text="Đóng", command=self.destroy, width=16).grid(row=0, column=1, padx=8)

        self.to_account_entry.bind("<KeyRelease>", self.on_to_account_change)
        self.amount_entry.bind("<KeyRelease>", self.on_amount_change)

        self.to_account_entry.bind("<Return>", lambda e: self.on_submit())  # new
        self.amount_entry.bind("<Return>", lambda e: self.on_submit())  # new
        self.bind("<Escape>", lambda e: self.destroy())  # new
        self.amount_entry.bind("<FocusOut>", self.on_amount_focus_out)  # new
        self.to_account_entry.focus_set()  # new

    def on_submit(self) -> None:
        to_account_id = self.to_account_entry.get().strip()
        amount = self._parse_amount_relaxed(self.amount_entry.get())  # new
        note = self.note_entry.get().strip()

        if to_account_id == "":
            messagebox.showwarning("Lỗi nhập liệu", "Số tài khoản nhận không được để trống.")
            return

        if str(to_account_id) == str(self.from_account_id):  # new
            messagebox.showwarning("Lỗi nhập liệu", "Không thể chuyển khoản cho chính mình.")
            return

        to_account = self.bank_service.get_account(to_account_id)  # new
        if to_account is None:  # new
            messagebox.showwarning("Không tìm thấy", "Tài khoản nhận không tồn tại.")  # new
            return  # new

        if amount == -1:
            messagebox.showwarning("Lỗi nhập liệu", "Số tiền phải là số nguyên dương.")
            return

        if amount > self.from_balance:  # new
            messagebox.showwarning("Không đủ số dư", "Số tiền chuyển lớn hơn số dư hiện tại.")  # new
            return  # new

        confirm = messagebox.askyesno(
            "Xác nhận",
            f"Chuyển {format_money_vnd(amount)} đến {to_account_id} ({to_account.owner_name}) ?",
        )  # new
        if not confirm:
            return

        ok, message = self.bank_service.transfer_money(self.from_account_id, to_account_id, amount, note)
        if ok:
            if self.success_callback is not None:
                self.success_callback()
            messagebox.showinfo("Thành công", message)
            self.destroy()
        else:
            messagebox.showwarning("Không thành công", message)
    def _parse_amount_relaxed(self, text: str) -> int:
        raw= str(text).strip() 
        if raw == "":
            return -1
        raw = re.sub(r"[\s\.,_]","",raw)
        return read_positive_integer(raw)
    def on_amount_focus_out(self, event=None) -> None:
        amount = self._parse_amount_relaxed(self.amount_entry.get()) 
        if amount != -1:
            self.amount_entry.delete(0, tk. END)
            self.amount_entry.insert(0, f"{amount:,}".replace(",", ".")) 
    def on_to_account_change(self, event=None) -> None:
        to_account_id = self.to_account_entry.get().strip()
        if to_account_id == "":
            self.to_name_label.configure(text="Tên người nhận: (chưa nhập)", foreground="gray")
            return
    def on_amount_change(self, event=None) -> None:
        amount = self._parse_amount_relaxed(self.amount_entry.get())
        if amount == -1:
            self.hint_label.configure(text="Gợi ý: nhập số nguyên dương, ví dụ 100.000.")
            return
        if amount > self.from_balance:
            self.hint_label.configure(text="Cảnh báo: số tiền chuyển lớn hơn số dư.", foreground="red")
            return
        self.hint_label.configure(text=f"Bạn nhập: {format_money_vnd (amount)}", foreground="gray")