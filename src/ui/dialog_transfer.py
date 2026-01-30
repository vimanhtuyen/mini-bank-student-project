import tkinter as tk
from tkinter import tkk, messagebox

from src.ui.ui_helpers import read_positive_integer

class TransferDialog(tk.Toplevel):

    def __init__(self, parent, bank_service, from_account_id: str, success_callback):
        super().__init__(parent)
        self.title("chuyen khoan")
        self.geometry("400 x200")
        self.resizable(False, False)

        self.bank_service = bank_service
        self.from_account_id = str(from_account_id)
        self.success_callback = success_callback

        ttk.Label(self, text = "Chuyen Khoan", font=("Segoe UI", 12, "bold")).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=8)

        ttk.Label(form, text = "So tai khoan nhan:").grid(row=0, column=0, sticky="w", pady=6)
        self.to_account_entry = ttk.Entry(form, width=28)
        self.to_account_entry.grid(row=0, column=1, pady=6)

        ttk.Label(form, text = "So tien (VND):").grid(row=1, column=0, sticky="w", pady=6)
        self.amount_entry = ttk.Entry(form, width=28)
        self.amount_entry.grid(row=1, column=1, pady=6)

        ttk.Label(form, text = "Ghi chu:").grid(row=2, column=0, sticky="w", pady=6)
        self.note_entry = ttk.Entry(form, width=28)
        self.note_entry.grid(row=2, column=1, pady=6)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=12)

        ttk.Button(button_frame, text = "Xac nhan", command=self.on_submit, width=16).grid(row=0, column=0, padx=8)
        ttk.Button(button_frame, text = "Huy bo", command=self.destroy, width=16).grid(row=0, column=1, padx=8)

    def on_submit(self) -> None:
        to_account_id = self.to_account_entry.get().strip()
        amount = read_positive_integer(self.amount_entry.get())
        note = self.note_entry.get().strip()

        if to_account_id == "":
            messagebox.showwarning("Vui long nhap so tai khoan nhan")
            return

        if amount == -1:
            messagebox.showwarning("So tien khong hop le")
            return

        ok, message = self.bank_service.transfer_money(self.from_account_id, to_account_id, amount, note)
        if ok:
            if self.success_callback is not None:
                self.success_callback()
            messagebox.showinfo("Thanh Cong", message)
            self.destroy()
        else:
            messagebox.showwarning("Khong Thanh Cong", message)