import tkinter as tk
from tkinter import ttk, messagebox

from src.ui.ui_helpers import read_positive_integer, format_money_vnd


class TransferDialog(tk.Toplevel):
    """Cửa sổ chuyển khoản (V2).

    - Hiển thị số dư người gửi
    - Tự hiển thị tên người nhận (nếu tìm thấy)
    - Xác nhận trước khi chuyển
    """

    def __init__(self, parent, bank_service, from_account_id: str, success_callback):
        super().__init__(parent)
        self.title("Chuyển khoản")
        self.geometry("520x330")
        self.resizable(False, False)

        self.bank_service = bank_service
        self.from_account_id = str(from_account_id)
        self.success_callback = success_callback

        from_account = self.bank_service.get_account(self.from_account_id)
        from_balance = 0
        from_name = ""
        if from_account is not None:
            from_balance = int(from_account.balance)
            from_name = str(from_account.owner_name)

        ttk.Label(self, text="Chuyển khoản", font=("Segoe UI", 12, "bold")).pack(pady=10)

        ttk.Label(self, text=f"Tài khoản gửi: {self.from_account_id} ({from_name})").pack(pady=2)
        ttk.Label(self, text=f"Số dư hiện tại: {format_money_vnd(from_balance)}").pack(pady=2)

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

    def on_to_account_change(self, event=None) -> None:
        to_account_id = self.to_account_entry.get().strip()
        if to_account_id == "":
            self.to_name_label.configure(text="Tên người nhận: (chưa nhập)", foreground="gray")
            return

        to_account = self.bank_service.get_account(to_account_id)
        if to_account is None:
            self.to_name_label.configure(text="Tên người nhận: (không tìm thấy)", foreground="red")
        else:
            self.to_name_label.configure(text=f"Tên người nhận: {to_account.owner_name}", foreground="green")

    def on_amount_change(self, event=None) -> None:
        amount = read_positive_integer(self.amount_entry.get())
        if amount == -1:
            self.hint_label.configure(text="Gợi ý: nhập số nguyên dương, ví dụ 100000.")
            return
        self.hint_label.configure(text="")

    def on_submit(self) -> None:
        to_account_id = self.to_account_entry.get().strip()
        amount = read_positive_integer(self.amount_entry.get())
        note = self.note_entry.get().strip()

        if to_account_id == "":
            messagebox.showwarning("Lỗi nhập liệu", "Số tài khoản nhận không được để trống.")
            return

        if amount == -1:
            messagebox.showwarning("Lỗi nhập liệu", "Số tiền phải là số nguyên dương.")
            return

        confirm = messagebox.askyesno("Xác nhận", f"Chuyển {format_money_vnd(amount)} đến {to_account_id} ?")
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