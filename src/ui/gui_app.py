import tkinter as tk
from tkinter import ttk, messagebox

from src.storage.json_storage import load_bank_data, save_bank_data
from src.core.bank_service import BankService

from src.ui.screens_start import StartFrame
from src.ui.screens_auth import RegisterFrame, LoginFrame
from src.ui.screens_dashboard import DashboardFrame


DATA_FILE_PATH = "data/bank_data.json"


class MiniBankApplication(tk.Tk):
    """Ứng dụng Tkinter chính."""

    def __init__(self):
        super().__init__()
        self.title("Mini Bank - Tkinter GUI (V2)")
        self.geometry("760x560")
        self.resizable(False, False)

        self.setup_style()
        self.setup_menu()

        bank_data = load_bank_data(DATA_FILE_PATH)
        self.bank_service = BankService(bank_data)

        self.logged_account_id = None

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.create_frames()

        self.status_text = tk.StringVar(value="Sẵn sàng.")
        self.status_bar = ttk.Label(self, textvariable=self.status_text, anchor="w")
        self.status_bar.pack(fill="x", side="bottom")

        self.show_frame("StartFrame")

        self.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def setup_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TFrame", padding=8)
        style.configure("TButton", padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))

    def setup_menu(self) -> None:
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Lưu dữ liệu", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.on_window_close)
        menu_bar.add_cascade(label="Tệp", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Hướng dẫn", command=self.show_help)
        help_menu.add_command(label="Giới thiệu", command=self.show_about)
        menu_bar.add_cascade(label="Trợ giúp", menu=help_menu)

        self.config(menu=menu_bar)

    def show_help(self) -> None:
        text = (
            "1) Tạo tài khoản: nhập Tên + PIN (4-6 số) + Số dư ban đầu.\n"
            "2) Đăng nhập: nhập Số tài khoản + PIN.\n"
            "3) Sau khi đăng nhập: Nạp/Rút/Chuyển khoản, xem Lịch sử.\n"
            "4) Dữ liệu lưu tự động khi bạn thao tác hoặc khi thoát."
        )
        messagebox.showinfo("Hướng dẫn nhanh", text)

    def show_about(self) -> None:
        messagebox.showinfo("Giới thiệu", "Mini Bank - Tkinter GUI (V2)\nDự án học Git + Python theo nhóm (3 bạn).")

    def set_status(self, text: str) -> None:
        self.status_text.set(str(text))

    def create_frames(self) -> None:
        self.frames["StartFrame"] = StartFrame(self.container, self)
        self.frames["RegisterFrame"] = RegisterFrame(self.container, self)
        self.frames["LoginFrame"] = LoginFrame(self.container, self)
        self.frames["DashboardFrame"] = DashboardFrame(self.container, self)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_name: str) -> None:
        frame = self.frames.get(frame_name)
        if frame is None:
            return

        if frame_name == "DashboardFrame":
            frame.refresh_information()

        self.set_status(f"Đang ở màn hình: {frame_name}")
        frame.tkraise()

    def save_data(self) -> None:
        save_bank_data(DATA_FILE_PATH, self.bank_service.build_snapshot_data())
        self.set_status("Đã lưu dữ liệu.")

    def on_window_close(self) -> None:
        self.save_data()
        self.destroy()


def run_application() -> None:
    app = MiniBankApplication()
    app.mainloop()
