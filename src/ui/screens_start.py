from tkinter import ttk


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
