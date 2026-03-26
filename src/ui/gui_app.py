import os  
import tkinter as tk
from tkinter import ttk, messagebox

from src.storage.json_storage import load_bank_data, save_bank_data
from src.core.bank_service import BankService

from src.ui.screens_start import StartFrame
from src.ui.screens_auth import RegisterFrame, LoginFrame
from src.ui.screens_dashboard import DashboardFrame


DATA_FILE_PATH = "data/bank_data.json"


class MiniBankApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini Bank - Student GUI")  
        self.geometry("960x680")  
        self.resizable(False, False)

        self.last_created_account_id = ""  
        self.last_login_account_id = ""  

        self.setup_style()
        self.setup_menu()

        bank_data = load_bank_data(DATA_FILE_PATH)
        self.bank_service = BankService(bank_data)

        self.logged_account_id = None

        self.build_shell_layout()  

        self.frames = {}
        self.create_frames()

        self.build_status_bar()  
        self.update_quick_summary()  

        self.show_frame("StartFrame")
        self.center_window()  

        self.bind_all("<Control-s>", lambda event: self.save_data())  
        self.bind_all("<F5>", lambda event: self.refresh_current_frame())  

        self.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def setup_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TFrame", padding=8)
        style.configure("App.TFrame", padding=12)  
        style.configure("Card.TFrame", padding=14)  
        style.configure("TButton", padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"))  
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))  
        style.configure("Status.TLabel", font=("Segoe UI", 9))  
        style.configure("Strong.TLabel", font=("Segoe UI", 11, "bold"))  

    def setup_menu(self) -> None:
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Lưu dữ liệu", command=self.save_data)
        file_menu.add_command(label="Làm mới màn hình", command=self.refresh_current_frame)  
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.on_window_close)
        menu_bar.add_cascade(label="Tệp", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Hướng dẫn", command=self.show_help)
        help_menu.add_command(label="Giới thiệu", command=self.show_about)
        menu_bar.add_cascade(label="Trợ giúp", menu=help_menu)

        self.config(menu=menu_bar)

    def build_shell_layout(self) -> None:  
        self.main_shell = ttk.Frame(self, style="App.TFrame")  
        self.main_shell.pack(fill="both", expand=True)  

        header_frame = ttk.Frame(self.main_shell, style="Card.TFrame")  
        header_frame.pack(fill="x", pady=(0, 8))  

        ttk.Label(header_frame, text="MINI BANK", style="Title.TLabel").pack(anchor="center")  
        ttk.Label(  
            header_frame,  
            text="Ứng dụng quản lý tài khoản ngân hàng mini dành cho học sinh thực hành Tkinter.",  
            style="Subtitle.TLabel",  
            justify="center",  
        ).pack(anchor="center", pady=(2, 0))  

        self.container = ttk.Frame(self.main_shell, style="Card.TFrame")  
        self.container.pack(fill="both", expand=True)  

    def build_status_bar(self) -> None:  
        status_frame = ttk.Frame(self.main_shell)  
        status_frame.pack(fill="x", side="bottom", pady=(8, 0))  

        self.status_text = tk.StringVar(value="Sẵn sàng.")
        self.quick_summary_text = tk.StringVar(value="")  

        self.status_bar = ttk.Label(status_frame, textvariable=self.status_text, anchor="w", style="Status.TLabel")  
        self.status_bar.pack(side="left", fill="x", expand=True)  

        self.summary_bar = ttk.Label(status_frame, textvariable=self.quick_summary_text, anchor="e", style="Status.TLabel")  
        self.summary_bar.pack(side="right")  

    def show_help(self) -> None:
        text = (
            "1) Tạo tài khoản: nhập Tên + PIN (4-6 số) + Số dư ban đầu.\n"
            "2) Đăng nhập: nhập Số tài khoản + PIN.\n"
            "3) Sau khi đăng nhập: Nạp/Rút/Chuyển khoản, xem Lịch sử.\n"
            "4) Dữ liệu lưu tự động khi bạn thao tác hoặc khi thoát.\n"  
            "5) Phím tắt: Ctrl+S để lưu, F5 để làm mới màn hình hiện tại."  
        )
        messagebox.showinfo("Hướng dẫn nhanh", text)

    def show_about(self) -> None:
        messagebox.showinfo(  
            "Mini Bank",  
            "Mini Bank - Student GUI\n"  
            "Phiên bản nâng cấp giao diện cho dự án nhóm học sinh.\n"  
            f"Tệp dữ liệu: {os.path.abspath(DATA_FILE_PATH)}",  
        )  

    def set_status(self, text: str) -> None:
        self.status_text.set(str(text))

    def update_quick_summary(self) -> None:  
        account_count = len(self.bank_service.accounts_by_id)  
        transaction_count = len(self.bank_service.transaction_list)  
        self.quick_summary_text.set(f"Tài khoản: {account_count} | Giao dịch: {transaction_count}")  

    def center_window(self) -> None:  
        self.update_idletasks()  
        width = self.winfo_width()  
        height = self.winfo_height()  
        screen_width = self.winfo_screenwidth()  
        screen_height = self.winfo_screenheight()  
        pos_x = max((screen_width - width) // 2, 0)  
        pos_y = max((screen_height - height) // 2 - 20, 0)  
        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")  

    def create_frames(self) -> None:
        self.frames["StartFrame"] = StartFrame(self.container, self)
        self.frames["RegisterFrame"] = RegisterFrame(self.container, self)
        self.frames["LoginFrame"] = LoginFrame(self.container, self)
        self.frames["DashboardFrame"] = DashboardFrame(self.container, self)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def refresh_current_frame(self) -> None:  
        current_frame = None  
        for frame in self.frames.values():  
            if str(frame.winfo_viewable()) == "1":  
                current_frame = frame  
                break  
        if current_frame is not None and hasattr(current_frame, "refresh_information"):  
            current_frame.refresh_information()  
        if current_frame is not None and hasattr(current_frame, "on_show"):  
            current_frame.on_show()  
        self.update_quick_summary()  
        self.set_status("Đã làm mới màn hình hiện tại.")  

    def show_frame(self, frame_name: str) -> None:
        frame = self.frames.get(frame_name)
        if frame is None:
            return

        if hasattr(frame, "on_show"):  
            frame.on_show()  

        if frame_name == "DashboardFrame":
            frame.refresh_information()

        self.update_quick_summary()  
        self.set_status(f"Đang ở màn hình: {frame_name}")
        frame.tkraise()

    def save_data(self) -> None:
        save_bank_data(DATA_FILE_PATH, self.bank_service.build_snapshot_data())
        self.update_quick_summary()  
        self.set_status("Đã lưu dữ liệu.")

    def on_window_close(self) -> None:
        self.save_data()
        self.destroy()


def run_application() -> None:
    app = MiniBankApplication()
    app.mainloop()