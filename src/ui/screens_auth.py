from tkinter import ttk, messagebox
from src.ui.ui_helpers import read_non_negative_integer, is_pin_format_valid


class RegisterFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        title_label = ttk.Label(self, text="Tạo tài khoản", style="Header.TLabel")
        title_label.pack(pady=12)

        form = ttk.Frame(self)
        form.pack(pady=8)

        ttk.Label(form, text="Tên chủ tài khoản:").grid(row=0, column=0, sticky="w", pady=8)
        self.owner_name_entry = ttk.Entry(form, width=38)
        self.owner_name_entry.grid(row=0, column=1, pady=8)

        ttk.Label(form, text="PIN (4–6 chữ số):").grid(row=1, column=0, sticky="w", pady=8)
        self.pin_code_entry = ttk.Entry(form, width=38, show="*")
        self.pin_code_entry.grid(row=1, column=1, pady=8)

        self.show_pin_register = ttk.Checkbutton(form, text="Hiện PIN", command=self.toggle_register_pin)
        self.show_pin_register.grid(row=1, column=2, padx=6)

        ttk.Label(form, text="Số dư ban đầu (VNĐ):").grid(row=2, column=0, sticky="w", pady=8)
        self.initial_balance_entry = ttk.Entry(form, width=38)
        self.initial_balance_entry.grid(row=2, column=1, pady=8)
        self.initial_balance_entry.insert(0, "0")

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=14)

        ttk.Button(button_frame, text="Tạo tài khoản", command=self.create_account, width=18).grid(row=0, column=0, padx=8)
        ttk.Button(button_frame, text="Quay lại", command=self.go_back, width=18).grid(row=0, column=1, padx=8)

    def toggle_register_pin(self) -> None:
        current_show = self.pin_code_entry.cget("show")
        if current_show == "":
            self.pin_code_entry.configure(show="*")
        else:
            self.pin_code_entry.configure(show="")

    def go_back(self) -> None:
        self.clear_inputs()
        self.app.show_frame("StartFrame")

    def clear_inputs(self) -> None:
        self.owner_name_entry.delete(0, "end")
        self.pin_code_entry.delete(0, "end")
        self.initial_balance_entry.delete(0, "end")
        self.initial_balance_entry.insert(0, "0")

    def create_account(self) -> None:
        owner_name = self.owner_name_entry.get().strip()
        pin_code = self.pin_code_entry.get().strip()
        initial_balance_text = self.initial_balance_entry.get().strip()

        if not is_pin_format_valid(pin_code):
            messagebox.showwarning("Lỗi nhập liệu", "PIN phải gồm 4 đến 6 chữ số.")
            return

        initial_balance = read_non_negative_integer(initial_balance_text)
        if initial_balance == -1:
            messagebox.showwarning("Lỗi nhập liệu", "Số dư ban đầu phải là số nguyên không âm.")
            return

        ok, message, account_id = self.app.bank_service.create_account(owner_name, pin_code, initial_balance)
        if ok:
            self.app.save_data()
            messagebox.showinfo("Thành công", message)
            self.clear_inputs()
            self.app.show_frame("LoginFrame")
        else:
            messagebox.showwarning("Không thành công", message)


class LoginFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        title_label = ttk.Label(self, text="Đăng nhập", style="Header.TLabel")
        title_label.pack(pady=12)

        form = ttk.Frame(self)
        form.pack(pady=8)

        ttk.Label(form, text="Số tài khoản:").grid(row=0, column=0, sticky="w", pady=8)
        self.account_id_entry = ttk.Entry(form, width=38)
        self.account_id_entry.grid(row=0, column=1, pady=8)

        ttk.Label(form, text="PIN:").grid(row=1, column=0, sticky="w", pady=8)
        self.pin_code_entry = ttk.Entry(form, width=38, show="*")
        self.pin_code_entry.grid(row=1, column=1, pady=8)

        self.show_pin_login = ttk.Checkbutton(form, text="Hiện PIN", command=self.toggle_login_pin)
        self.show_pin_login.grid(row=1, column=2, padx=6)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=14)

        ttk.Button(button_frame, text="Đăng nhập", command=self.login, width=18).grid(row=0, column=0, padx=8)
        ttk.Button(button_frame, text="Quay lại", command=self.go_back, width=18).grid(row=0, column=1, padx=8)

    def toggle_login_pin(self) -> None:
        current_show = self.pin_code_entry.cget("show")
        if current_show == "":
            self.pin_code_entry.configure(show="*")
        else:
            self.pin_code_entry.configure(show="")

    def go_back(self) -> None:
        self.clear_inputs()
        self.app.show_frame("StartFrame")

    def clear_inputs(self) -> None:
        self.account_id_entry.delete(0, "end")
        self.pin_code_entry.delete(0, "end")

    def login(self) -> None:
        account_id = self.account_id_entry.get().strip()
        pin_code = self.pin_code_entry.get().strip()

        ok, message = self.app.bank_service.authenticate_login(account_id, pin_code)
        if ok:
            self.app.logged_account_id = account_id
            self.clear_inputs()
            self.app.show_frame("DashboardFrame")
        else:
            messagebox.showwarning("Không thành công", message)
<<<<<<< HEAD
    
    self.preview_label = ttk.Label(self, text = "Bo sung sau", style= "Strong.Tlabel")
    self.preview_label.pack(pady=(0,8))

    display_name = owner_name if owner_name != "" else "(Chưa nhập tên)"
    display_pin = "*" * len(pin_code) if pin_code != "" else "(Chưa nhập PIN)"
    display_balance = "Không hợp lệ" if balance == -1 else format_money_vnd(balance)
    self.preview_label.configure(
        text = f"Thông tin xem trước: {display_name} | {display_pin} | {display_balance}"
    )

    
=======

    self.preview_label = ttk.Label(self, text = "Bo sung sau", style = "Strong.TLabel")
    self.preview_label.pack(pady=(0,0))

    display_name = owner_name if owner_name != "" else "(Chua nhap ten)"
    display_pin = "*" * len(pin_code) if pin_code != "" else "(Chua nhap PIN)"
    display_balance = "Khong hop le" if balance == -1 else format_money_vnd(balance)
    self.preview_label.configure(
        text = f"Thong tin xem truoc: {display_name} | {display_pin} | {display_balance}"
    )
>>>>>>> f7a368f13a77b143aa588a320b7113c2fe37bc65
