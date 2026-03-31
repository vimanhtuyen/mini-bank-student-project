from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

from src.storage.json_storage import load_bank_data, save_bank_data
from src.core.bank_service import BankService
from src.ui.screens_start import StartFrame
from src.ui.screens_auth import RegisterFrame, LoginFrame
from src.ui.screens_dashboard import DashboardFrame
from src.ui.ui_helpers import (
    BIDV_BACKGROUND,
    BIDV_BLUE,
    BIDV_BORDER,
    BIDV_DARK_BLUE,
    BIDV_LIGHT_BLUE,
    BIDV_MUTED,
    BIDV_RED,
    BIDV_SURFACE,
    BIDV_TEXT,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE_PATH = str(PROJECT_ROOT / 'data' / 'bank_data.json')


class MiniBankApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Mini Bank')
        self.geometry('1180x760')
        self.resizable(False, False)
        self.configure(bg=BIDV_BACKGROUND)

        self.last_created_account_id = ''
        self.last_login_account_id = ''
        self.logged_account_id = None
        self.current_frame_name = 'StartFrame'

        self.setup_style()
        self.setup_menu()

        bank_data = load_bank_data(DATA_FILE_PATH)
        self.bank_service = BankService(bank_data)

        self.build_shell_layout()
        self.frames = {}
        self.create_frames()
        self.build_status_bar()

        self.update_quick_summary()
        self.show_frame('StartFrame')
        self.center_window()

        self.bind_all('<Control-s>', lambda event: self.save_data())
        self.bind_all('<F5>', lambda event: self.refresh_current_frame())
        self.protocol('WM_DELETE_WINDOW', self.on_window_close)

    def setup_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use('clam')
        except Exception:
            pass

        style.configure('TFrame', background=BIDV_BACKGROUND)
        style.configure('App.TFrame', background=BIDV_BACKGROUND)
        style.configure('Surface.TFrame', background=BIDV_SURFACE)
        style.configure('Card.TFrame', background=BIDV_SURFACE, relief='flat')
        style.configure('AppBar.TFrame', background=BIDV_DARK_BLUE)
        style.configure('Hero.TFrame', background=BIDV_BLUE)
        style.configure('Strip.TFrame', background=BIDV_RED)
        style.configure('Footer.TFrame', background=BIDV_DARK_BLUE)

        style.configure('TLabel', background=BIDV_BACKGROUND, foreground=BIDV_TEXT, font=('Segoe UI', 10))
        style.configure('Surface.TLabel', background=BIDV_SURFACE, foreground=BIDV_TEXT)
        style.configure('Muted.TLabel', background=BIDV_SURFACE, foreground=BIDV_MUTED)
        style.configure('BrandTitle.TLabel', background=BIDV_DARK_BLUE, foreground='white', font=('Segoe UI', 20, 'bold'))
        style.configure('BrandSub.TLabel', background=BIDV_DARK_BLUE, foreground='#d5e6fb', font=('Segoe UI', 10))
        style.configure('HeaderTitle.TLabel', background=BIDV_BACKGROUND, foreground=BIDV_DARK_BLUE, font=('Segoe UI', 21, 'bold'))
        style.configure('SectionTitle.TLabel', background=BIDV_SURFACE, foreground=BIDV_DARK_BLUE, font=('Segoe UI', 13, 'bold'))
        style.configure('CardTitle.TLabel', background=BIDV_SURFACE, foreground=BIDV_DARK_BLUE, font=('Segoe UI', 11, 'bold'))
        style.configure('Strong.TLabel', background=BIDV_SURFACE, foreground=BIDV_TEXT, font=('Segoe UI', 11, 'bold'))
        style.configure('HeroTitle.TLabel', background=BIDV_BLUE, foreground='white', font=('Segoe UI', 24, 'bold'))
        style.configure('HeroText.TLabel', background=BIDV_BLUE, foreground='#e5f1ff', font=('Segoe UI', 11))
        style.configure('MetricValue.TLabel', background=BIDV_SURFACE, foreground=BIDV_DARK_BLUE, font=('Segoe UI', 16, 'bold'))
        style.configure('MetricCaption.TLabel', background=BIDV_SURFACE, foreground=BIDV_MUTED, font=('Segoe UI', 9))
        style.configure('Status.TLabel', background=BIDV_DARK_BLUE, foreground='white', font=('Segoe UI', 9))
        style.configure('StatusDim.TLabel', background=BIDV_DARK_BLUE, foreground='#dbe9f9', font=('Segoe UI', 9))

        style.configure('Card.TLabelframe', background=BIDV_SURFACE, bordercolor=BIDV_BORDER, borderwidth=1, relief='solid', padding=14)
        style.configure('Card.TLabelframe.Label', background=BIDV_SURFACE, foreground=BIDV_DARK_BLUE, font=('Segoe UI', 11, 'bold'))

        style.configure('TEntry', padding=8, fieldbackground='white', foreground=BIDV_TEXT, bordercolor=BIDV_BORDER)
        style.map('TEntry', bordercolor=[('focus', BIDV_BLUE)])
        style.configure('TCombobox', padding=6, fieldbackground='white', foreground=BIDV_TEXT, bordercolor=BIDV_BORDER)
        style.map('TCombobox', bordercolor=[('focus', BIDV_BLUE)])
        style.configure('Surface.TCheckbutton', background=BIDV_SURFACE, foreground=BIDV_TEXT, font=('Segoe UI', 10))
        style.map('Surface.TCheckbutton', background=[('active', BIDV_SURFACE)])

        style.configure('Primary.TButton', background=BIDV_RED, foreground='white', borderwidth=0, padding=(18, 10), font=('Segoe UI', 10, 'bold'))
        style.map('Primary.TButton', background=[('active', '#bf1820'), ('pressed', '#a7141b')])
        style.configure('Secondary.TButton', background=BIDV_BLUE, foreground='white', borderwidth=0, padding=(16, 10), font=('Segoe UI', 10, 'bold'))
        style.map('Secondary.TButton', background=[('active', '#004f93'), ('pressed', '#00457f')])
        style.configure('Light.TButton', background='white', foreground=BIDV_DARK_BLUE, borderwidth=1, bordercolor=BIDV_BORDER, padding=(16, 10), font=('Segoe UI', 10, 'bold'))
        style.map('Light.TButton', background=[('active', BIDV_LIGHT_BLUE), ('pressed', '#dfeaf7')])
        style.configure('Danger.TButton', background='#fff2f3', foreground=BIDV_RED, borderwidth=1, bordercolor='#f2b8bc', padding=(16, 10), font=('Segoe UI', 10, 'bold'))
        style.map('Danger.TButton', background=[('active', '#ffdfe1')])

        style.configure('Treeview', background='white', fieldbackground='white', foreground=BIDV_TEXT, rowheight=31, bordercolor=BIDV_BORDER, font=('Segoe UI', 10))
        style.configure('Treeview.Heading', background=BIDV_DARK_BLUE, foreground='white', relief='flat', font=('Segoe UI', 10, 'bold'))
        style.map('Treeview.Heading', background=[('active', BIDV_BLUE)])

    def setup_menu(self) -> None:
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Lưu dữ liệu', command=self.save_data)
        file_menu.add_command(label='Làm mới màn hình', command=self.refresh_current_frame)
        file_menu.add_separator()
        file_menu.add_command(label='Thoát', command=self.on_window_close)
        menu_bar.add_cascade(label='Tệp', menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='Hướng dẫn', command=self.show_help)
        help_menu.add_command(label='Giới thiệu', command=self.show_about)
        menu_bar.add_cascade(label='Trợ giúp', menu=help_menu)

        self.config(menu=menu_bar)

    def build_shell_layout(self) -> None:
        self.main_shell = ttk.Frame(self, style='App.TFrame')
        self.main_shell.pack(fill='both', expand=True)

        red_strip = ttk.Frame(self.main_shell, style='Strip.TFrame', height=5)
        red_strip.pack(fill='x')
        red_strip.pack_propagate(False)

        app_bar = ttk.Frame(self.main_shell, style='AppBar.TFrame', padding=(24, 18))
        app_bar.pack(fill='x')

        left_bar = ttk.Frame(app_bar, style='AppBar.TFrame')
        left_bar.pack(side='left', fill='x', expand=True)
        ttk.Label(left_bar, text='MINI BANK', style='BrandTitle.TLabel').pack(anchor='w')
        ttk.Label(left_bar, text='', style='BrandSub.TLabel').pack(anchor='w', pady=(2, 0))

        right_bar = ttk.Frame(app_bar, style='AppBar.TFrame')
        right_bar.pack(side='right')
        self.page_title_var = tk.StringVar(value='Trang chủ')
        self.current_user_var = tk.StringVar(value='Chưa đăng nhập')
        ttk.Label(right_bar, textvariable=self.page_title_var, style='BrandTitle.TLabel', font=('Segoe UI', 15, 'bold')).pack(anchor='e')
        ttk.Label(right_bar, textvariable=self.current_user_var, style='BrandSub.TLabel').pack(anchor='e', pady=(2, 0))

        self.content_area = ttk.Frame(self.main_shell, style='App.TFrame', padding=(22, 18, 22, 12))
        self.content_area.pack(fill='both', expand=True)

        self.container = ttk.Frame(self.content_area, style='App.TFrame')
        self.container.pack(fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def build_status_bar(self) -> None:
        footer = ttk.Frame(self.main_shell, style='Footer.TFrame', padding=(18, 10))
        footer.pack(fill='x', side='bottom')

        self.status_text = tk.StringVar(value='Sẵn sàng.')
        self.quick_summary_text = tk.StringVar(value='')
        ttk.Label(footer, textvariable=self.status_text, style='Status.TLabel').pack(side='left', fill='x', expand=True)
        ttk.Label(footer, textvariable=self.quick_summary_text, style='StatusDim.TLabel').pack(side='right')

    def show_help(self) -> None:
        text = (
            '1) Tạo tài khoản với tên, PIN và số dư ban đầu.\n'
            '2) Đăng nhập bằng số tài khoản và PIN.\n'
            '3) Trong bảng điều khiển, bạn có thể nạp tiền, rút tiền, chuyển khoản và xem lịch sử.\n'
            '4) Dữ liệu được lưu khi thao tác thành công hoặc khi thoát chương trình.\n'
            '5) Phím tắt: Ctrl+S để lưu, F5 để làm mới màn hình hiện tại.'
        )
        messagebox.showinfo('Hướng dẫn nhanh', text)

    def show_about(self) -> None:
        messagebox.showinfo(
            'Mini Bank',
            'Mini Bank - bản nâng cấp giao diện phong cách BIDV.\n'
            'Dự án giữ nguyên lõi nghiệp vụ nhưng thay mới giao diện, bảng điều khiển và các hộp thoại giao dịch.\n\n'
            f'Tệp dữ liệu hiện dùng:\n{DATA_FILE_PATH}',
        )

    def set_status(self, text: str) -> None:
        self.status_text.set(str(text))

    def update_header_context(self) -> None:
        page_map = {
            'StartFrame': 'Trang chủ',
            'RegisterFrame': 'Mở tài khoản',
            'LoginFrame': 'Đăng nhập',
            'DashboardFrame': 'Tổng quan tài khoản',
        }
        self.page_title_var.set(page_map.get(self.current_frame_name, self.current_frame_name))
        if self.logged_account_id is None:
            self.current_user_var.set('Chưa đăng nhập')
        else:
            account = self.bank_service.get_account(self.logged_account_id)
            if account is None:
                self.current_user_var.set(f'Tài khoản {self.logged_account_id}')
            else:
                self.current_user_var.set(f'{account.owner_name} • {account.account_id}')

    def update_quick_summary(self) -> None:
        account_count = len(self.bank_service.accounts_by_id)
        transaction_count = len(self.bank_service.transaction_list)
        self.quick_summary_text.set(f'Tài khoản: {account_count} | Giao dịch: {transaction_count}')
        self.update_header_context()

    def center_window(self) -> None:
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        pos_x = max((screen_width - width) // 2, 0)
        pos_y = max((screen_height - height) // 2 - 20, 0)
        self.geometry(f'{width}x{height}+{pos_x}+{pos_y}')

    def create_frames(self) -> None:
        self.frames['StartFrame'] = StartFrame(self.container, self)
        self.frames['RegisterFrame'] = RegisterFrame(self.container, self)
        self.frames['LoginFrame'] = LoginFrame(self.container, self)
        self.frames['DashboardFrame'] = DashboardFrame(self.container, self)
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky='nsew')

    def refresh_current_frame(self) -> None:
        current_frame = self.frames.get(self.current_frame_name)
        if current_frame is not None and hasattr(current_frame, 'refresh_information'):
            current_frame.refresh_information()
        if current_frame is not None and hasattr(current_frame, 'on_show'):
            current_frame.on_show()
        self.update_quick_summary()
        self.set_status('Đã làm mới màn hình hiện tại.')

    def show_frame(self, frame_name: str) -> None:
        frame = self.frames.get(frame_name)
        if frame is None:
            return
        self.current_frame_name = frame_name
        if hasattr(frame, 'on_show'):
            frame.on_show()
        if frame_name == 'DashboardFrame' and hasattr(frame, 'refresh_information'):
            frame.refresh_information()
        frame.tkraise()
        self.update_quick_summary()
        self.set_status(f'Đang ở màn hình: {self.page_title_var.get()}')

    def save_data(self) -> None:
        save_bank_data(DATA_FILE_PATH, self.bank_service.build_snapshot_data())
        self.update_quick_summary()
        self.set_status('Đã lưu dữ liệu.')

    def on_window_close(self) -> None:
        self.save_data()
        self.destroy()


def run_application() -> None:
    app = MiniBankApplication()
    app.mainloop()
