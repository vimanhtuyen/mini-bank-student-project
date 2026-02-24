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
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Hướng dẫn", command=self.show_help)
        help_menu.add_command(label="Giới thiệu", command=self.show_about)
        menu_bar.add_cascade(label="Trợ giúp", menu=help_menu)

        self.config(menu=menu_bar)


    def show_about(self) -> None:
        messagebox.showinfo("Giới thiệu") # Có thể sửa sau
        
    def show_help(self) -> None:
        text = (
            "1. Tạo tài khoản. \n"
            "2. Đăng nhập. \n"
            "3. Chuyển khoản. \n"
            "4. Nạp tiền. \n"
            "5. Rút tiền. \n"
            "6. Xem lịch sử giao dịch. \n"
            "7. Đăng xuất. \n"
            "8. Thoát. \n"
        )
        messagebox.showinfo("Hướng dẫn") # Có thể sửa sau

def run_application() -> None:
    app = MiniBankApplication()
    app.mainloop()