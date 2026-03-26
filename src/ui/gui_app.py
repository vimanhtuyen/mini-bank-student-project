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
        self.title("Not A Bank - B-E1-22")
        self.geometry(f"{int(1600*3/4)}x{int(900*3/4)}")
        self.resizable(False, False)

        self.last_created_account_id = ""
        self.last_logged_account_id = ""
        self.setup_style()
        self.setup_menu()
        self.build_shell_layout()
        style.configure("App.TFrame", padding = 12)
        style.configure("Card.TFrame", padding = 12)
        style.configure("Title.TLabel", font=("Bitcount Grid Single Ink", 22, "bold"))
        style.configure("Subtitle.TLabel", font=("Lobster Two", 14, "italic"))
        style.configure("Status.TLabel", font=("Great Vibes", 10))
        style.configure("Strong.TLabel", font=("Yellowtail", 12, "bold"))

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
        messagebox.showinfo("Mini Bank")

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

        guide_label = ttk.Label(
            self,
<<<<<<< HEAD
            text = "Bo sung sau",
            justify = "center"
        )
        guide_label.pack(pady = (0,8))
=======
            text= "Bo sung sau",
            justify= "center"
        )
        guide_label.pack(pady= (0,0))
>>>>>>> f7a368f13a77b143aa588a320b7113c2fe37bc65

    def save_data(self) -> None:
        save_bank_data(DATA_FILE_PATH, self.bank_service.build_snapshot_data())
        self.set_status("Đã lưu dữ liệu.")

    def on_window_close(self) -> None:
        self.save_data()
        self.destroy()

    def build_shell_layout(self) -> None:
<<<<<<< HEAD
        self.main_shell = ttk.Frame(self, style="App.TFrame")
        self.main_shell.pack(fill="both", expand=True)

        header_frame = ttk.Frame(self.main_shell, style="Card.TFrame")
        header_frame.pack(fill="x", pady = (0, 8))

        ttk.Label(header_frame, text= " Bổ sung sau ", style="Title.TLabel").pack(anchor="center")
        ttk.Label(
            header_frame,
            text = " Bổ sung sau ",
            style = "Subtitle.TLabel",
            justify = "center",
        ).pack(anchor="center", pady=(2,0))
=======
        self.main_shell = ttk.Frame(self, system="App.TFrame")
        self.main_shell.pack(fill="both", expand=True)

        header_frame = ttk.Frame(self.main_shell, style="Card.TFrame")
        header_frame = pack(fill="x", pady = (0,0))

        ttk.Label(header_frame, text= "Bo sung sau", style="Title.TLabel").pack(anchor="center")
        ttk.Label(
            header_frame,
            text = "Bo sung sau ",
            style= "Subtitle.TLabel",
            justify= "center"
        ).pack(anchor="center", pady = (2,0))
>>>>>>> f7a368f13a77b143aa588a320b7113c2fe37bc65

        self.container = ttk.Frame(self.main_shell, style="Card.TFrame")
        self.container.pack(fill="both", expand=True)

<<<<<<< HEAD

    self.center_window()
    self.bind_all("<Control-s>", lambda event: self.save_data())
    self.bind_all("<F5>", lambda event: self.refresh_current_frame())
=======
    self.center_window()
    self.bind_all("<Control-s>", lambda event: self.save_data())
    self.bind_all("<F5>", lambda event: expand=self.refresh_current_frame())
>>>>>>> f7a368f13a77b143aa588a320b7113c2fe37bc65

    def center_window(self) -> None:
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
<<<<<<< HEAD
        pos_x = max((screen_width - width)//2, 0)
        pos_y = max((screen_height - height)//2 - 30, 0)
        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")







=======
        pos_x = max((screen_width - width)// 2, 0)
        pos_y = max((screen_height - height)//2 - 30, 0)
        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

>>>>>>> f7a368f13a77b143aa588a320b7113c2fe37bc65

def run_application() -> None:
    app = MiniBankApplication()
    app.mainloop()
