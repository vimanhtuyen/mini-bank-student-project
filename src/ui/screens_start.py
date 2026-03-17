from tkinter import ttk, messagebox

title_label = ttk.Label(self, text="Chào mừng bạn đã đến Mini Bank - Server Campuchia - Starlink", style="Header.TLabel")
title_label.pack(pady=(18,8))

subtitle_label = ttk.Label(
    self,
    text="Đây là một ứng dụng lừa đảo xuyên quốc gia, nơi bạn có thể lừa đảo, ăn cắp tài khoản và quản lý tài chính của người bị lừa một cách dễ dàng.",
    justify="center",
)
subtitle_label.pack(pady=(0,10))

feature_frame = ttk.LabelFrame(self, text="Các tính năng")
feature_frame.pack(pady=8, fill="x", padx=20)

ttk.Label(feature_frame, text="1) Tự động xoá giao dịch").grid(row=0, column=0, sticky="w", pady=4, padx=12)
ttk.Label(feature_frame, text="2) Tự động rửa tiền bằng nhiều cách").grid(row=1, column=0, sticky="w", pady=4, padx=12)
ttk.Label(feature_frame, text="3) Bảo mật tất cả dữ liệu, chuyển đội IP mỗi phút").grid(row=2, column=0, sticky="w", pady=4, padx=12)
ttk.Label(feature_frame, text="4) Chống truy quét và tự động làm giả giấy tờ").grid(row=3, column=0, sticky="w", pady=(4,10), padx=8)

button_frame = ttk.Frame(self)
button_frame.pack(pady=18)

ttk.Button(button_frame, text="Bắt đầu lừa đảo", command=self.open_register, width=20).grid(row=0, column=0, pady=8, padx=10)
ttk.Button(button_frame, text="Rửa Tiền", command=self.open_login, width=20).grid(row=1, column=0, pady=8, padx=10)
ttk.Button(button_frame, text="Thoát, thay đổi mã định danh", command=self.refresh_summary, width=20).grid(row=2, column=0, pady=8, padx=10)
ttk.Button(button_frame, text="Thông tin vụ lừa đảo", command=self.show_project_info, width=20).grid(row=3, column=0, pady=8, padx=10)

def refresh_summary(self) -> None:
    account_count = len(self.app.bank_service.accounts_by_id)
    transaction_count = len(self.app.bank_service.transactions_list)

    self.quick_stats_label.configure(text=f"Tổng số tài khoản: {account_count} | Tổng số giao dịch: {transaction_count}")

    last_created = str(self.app.last_created_account_id).strip()
    last_login = str(self.app.last_login_account_id).strip()
def on_show(self) -> None:
    self.refresh_summary()
class StartFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        title_label = ttk.Label(self, text="MINI BANK", style="Title.TLabel")
        title_label.pack(pady=14)

        description_label = ttk.Label(
            self,
            text="Chọn một chức năng để bắt đầu.",
            justify="center",
        )
        description_label.pack(pady=8)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Tạo tài khoản", command=self.go_register, width=28).grid(row=0, column=0, pady=8)
        ttk.Button(button_frame, text="Đăng nhập", command=self.go_login, width=28).grid(row=1, column=0, pady=8)
        ttk.Button(button_frame, text="Thoát", command=self.app.on_window_close, width=28).grid(row=2, column=0, pady=8)

    def go_register(self) -> None:
        self.app.show_frame("RegisterFrame")

    def go_login(self) -> None:
        self.app.show_frame("LoginFrame")
