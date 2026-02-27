from tkinter import ttk, messagebox

from src.ui.ui_helpers import format_money_vnd
from src.ui.dialog_money import MoneyDialog
from src.ui.dialog_transfer import TransferDialog
from src.ui.window_history import HistoryWindow


class DashboardFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        title_label = ttk.Label(self, text="Bảng điều khiển", style="Header.TLabel")
        title_label.pack(pady=10)

        self.info_label = ttk.Label(self, text="", font=("Segoe UI", 11))
        self.info_label.pack(pady=4)

        self.balance_label = ttk.Label(self, text="", font=("Segoe UI", 12, "bold"))
        self.balance_label.pack(pady=4)

        info_frame = ttk.Frame(self)
        info_frame.pack(pady=4)

        ttk.Button(info_frame, text="Copy số tài khoản", command=self.copy_account_id, width=20).grid(row=0, column=0, padx=6)
        ttk.Button(info_frame, text="Làm mới", command=self.refresh_information, width=14).grid(row=0, column=1, padx=6)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=18)

        ttk.Button(button_frame, text="Nạp tiền", command=self.open_deposit, width=22).grid(row=0, column=0, padx=10, pady=8)
        ttk.Button(button_frame, text="Rút tiền", command=self.open_withdraw, width=22).grid(row=0, column=1, padx=10, pady=8)
        ttk.Button(button_frame, text="Chuyển khoản", command=self.open_transfer, width=22).grid(row=1, column=0, padx=10, pady=8)
        ttk.Button(button_frame, text="Lịch sử giao dịch", command=self.open_history, width=22).grid(row=1, column=1, padx=10, pady=8)

        ttk.Button(self, text="Đăng xuất", command=self.logout, width=22).pack(pady=12)

    def get_logged_account_id(self) -> str:
        if self.app.logged_account_id is None:
            return ""
        return str(self.app.logged_account_id)

    def get_logged_account(self):
        account_id = self.get_logged_account_id()
        return self.app.bank_service.get_account(account_id)

    def refresh_information(self) -> None:
        account = self.get_logged_account()
        if account is None:
            self.info_label.configure(text="Không tìm thấy tài khoản.")
            self.balance_label.configure(text="")
            return

        self.info_label.configure(text=f"Số tài khoản: {account.account_id} | Chủ tài khoản: {account.owner_name}")
        self.balance_label.configure(text=f"Số dư: {format_money_vnd(account.balance)}")

        self.app.set_status("Đã làm mới thông tin tài khoản.")

    def copy_account_id(self) -> None:
        account = self.get_logged_account()
        if account is None:
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(str(account.account_id))
            self.app.set_status("Đã copy số tài khoản vào clipboard.")
            messagebox.showinfo("Copy", "Đã copy số tài khoản.")
        except Exception:
            messagebox.showwarning("Lỗi", "Không thể copy vào clipboard.")

    def logout(self) -> None:
        confirm = messagebox.askyesno("Xác nhận", "Bạn muốn đăng xuất?")
        if not confirm:
            return
        self.app.logged_account_id = None
        self.app.show_frame("StartFrame")

    def open_deposit(self) -> None:
        account = self.get_logged_account()
        if account is None:
            return

        def submit(amount: int, note: str):
            ok, message = self.app.bank_service.deposit_money(account.account_id, amount, note)
            if ok:
                self.app.save_data()
                self.refresh_information()
            return ok, message

        MoneyDialog(self, "Nạp tiền", account.balance, submit)

    def open_withdraw(self) -> None:
        account = self.get_logged_account()
        if account is None:
            return

        def submit(amount: int, note: str):
            ok, message = self.app.bank_service.withdraw_money(account.account_id, amount, note)
            if ok:
                self.app.save_data()
                self.refresh_information()
            return ok, message

        MoneyDialog(self, "Rút tiền", account.balance, submit)

    def open_transfer(self) -> None:
        account = self.get_logged_account()
        if account is None:
            return

        def on_success():
            self.app.save_data()
            self.refresh_information()

        TransferDialog(self, self.app.bank_service, account.account_id, on_success)

    def open_history(self) -> None:
        account = self.get_logged_account()
        if account is None:
            return
        HistoryWindow(self, self.app.bank_service, account.account_id)
