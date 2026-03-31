from tkinter import ttk, messagebox

from src.ui.ui_helpers import format_money_vnd


class StartFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, style='App.TFrame')
        self.app = app

        hero = ttk.Frame(self, style='Hero.TFrame', padding=(28, 28))
        hero.pack(fill='x', pady=(0, 18))

        hero_left = ttk.Frame(hero, style='Hero.TFrame')
        hero_left.pack(side='left', fill='both', expand=True)
        ttk.Label(hero_left, text='Mini Bank', style='HeroTitle.TLabel').pack(anchor='w')
        ttk.Label(
            hero_left,
            text='',
            style='HeroText.TLabel',
            wraplength=620,
            justify='left',
        ).pack(anchor='w', pady=(10, 16))

        action_bar = ttk.Frame(hero_left, style='Hero.TFrame')
        action_bar.pack(anchor='w')
        ttk.Button(action_bar, text='Mở tài khoản ngay', command=self.open_register, style='Primary.TButton').grid(row=0, column=0, padx=(0, 10))
        ttk.Button(action_bar, text='Đăng nhập', command=self.open_login, style='Light.TButton').grid(row=0, column=1)

        hero_right = ttk.Frame(hero, style='Surface.TFrame', padding=(22, 18))
        hero_right.pack(side='right', padx=(22, 0))
        ttk.Label(hero_right, text='Điểm nổi bật', style='CardTitle.TLabel').pack(anchor='w')
        for line in [
            '• Tạo tài khoản nhanh với PIN 4–6 số',
            '• Nạp, rút, chuyển khoản ngay trên giao diện',
            '• Lịch sử giao dịch lọc và tìm kiếm rõ ràng',
            '• Dữ liệu lưu bằng JSON để dễ dạy học sinh',
        ]:
            ttk.Label(hero_right, text=line, style='Surface.TLabel').pack(anchor='w', pady=3)

        metrics_wrap = ttk.Frame(self, style='App.TFrame')
        metrics_wrap.pack(fill='x', pady=(0, 18))
        self.account_value = self._create_metric_card(metrics_wrap, 0, 'Tổng số tài khoản')
        self.transaction_value = self._create_metric_card(metrics_wrap, 1, 'Tổng số giao dịch')
        self.balance_value = self._create_metric_card(metrics_wrap, 2, 'Tổng số dư toàn hệ thống')

        bottom_grid = ttk.Frame(self, style='App.TFrame')
        bottom_grid.pack(fill='both', expand=True)
        bottom_grid.columnconfigure(0, weight=3)
        bottom_grid.columnconfigure(1, weight=2)

        left_card = ttk.Frame(bottom_grid, style='Card.TFrame', padding=(22, 18))
        left_card.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        ttk.Label(left_card, text='Mô tả dự án', style='SectionTitle.TLabel').pack(anchor='w')
        ttk.Label(
            left_card,
            text='',
            style='Surface.TLabel',
            wraplength=620,
            justify='left',
        ).pack(anchor='w', pady=(8, 14))

        for line in [
            '1. Thiết kế màn hình chào mừng và điều hướng nhiều frame.',
            '2. Xử lý biểu mẫu mở tài khoản và đăng nhập có gợi ý realtime.',
            '3. Mở hộp thoại giao dịch và kiểm tra số tiền hợp lệ.',
            '4. Hiển thị bảng điều khiển, số dư, lịch sử và thống kê nhanh.',
            '5. Lưu dữ liệu JSON để nhìn được kết quả sau mỗi lần chạy.',
        ]:
            ttk.Label(left_card, text=line, style='Surface.TLabel').pack(anchor='w', pady=4)

        button_row = ttk.Frame(left_card, style='Card.TFrame')
        button_row.pack(anchor='w', pady=(16, 0))
        ttk.Button(button_row, text='Làm mới số liệu', command=self.refresh_summary, style='Secondary.TButton').grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_row, text='Giới thiệu dự án', command=self.show_project_info, style='Light.TButton').grid(row=0, column=1)

        right_card = ttk.Frame(bottom_grid, style='Card.TFrame', padding=(22, 18))
        right_card.grid(row=0, column=1, sticky='nsew')
        ttk.Label(right_card, text='Thông tin gần nhất', style='SectionTitle.TLabel').pack(anchor='w')
        self.recent_info_label = ttk.Label(right_card, text='Đang cập nhật...', style='Surface.TLabel', wraplength=320, justify='left')
        self.recent_info_label.pack(anchor='w', pady=(10, 14))

        ttk.Label(right_card, text='Mẹo thao tác', style='CardTitle.TLabel').pack(anchor='w')
        ttk.Label(
            right_card,
            text='Tạo tài khoản trước, sau đó bấm “Đăng nhập” để vào bảng điều khiển. Trong dashboard, nhấn đúp vào bảng giao dịch để mở lịch sử đầy đủ.',
            style='Surface.TLabel',
            wraplength=320,
            justify='left',
        ).pack(anchor='w', pady=(8, 10))

        ttk.Label(right_card, text='Phiên bản giao diện mới', style='CardTitle.TLabel').pack(anchor='w', pady=(10, 0))
        ttk.Label(
            right_card,
            text='• Header xanh đậm kiểu ngân hàng\n• Nút hành động đỏ nổi bật\n• Dashboard dạng thẻ thông tin\n• Hộp thoại giao dịch trực quan hơn',
            style='Surface.TLabel',
            justify='left',
        ).pack(anchor='w', pady=(8, 0))

    def _create_metric_card(self, parent, column_index: int, title: str):
        card = ttk.Frame(parent, style='Card.TFrame', padding=(18, 16))
        card.grid(row=0, column=column_index, sticky='nsew', padx=(0, 10) if column_index < 2 else 0)
        parent.columnconfigure(column_index, weight=1)
        ttk.Label(card, text=title, style='CardTitle.TLabel').pack(anchor='w')
        value_label = ttk.Label(card, text='0', style='MetricValue.TLabel')
        value_label.pack(anchor='w', pady=(12, 2))
        ttk.Label(card, text='Cập nhật theo dữ liệu hiện tại', style='MetricCaption.TLabel').pack(anchor='w')
        return value_label

    def refresh_summary(self) -> None:
        account_count = len(self.app.bank_service.accounts_by_id)
        transaction_count = len(self.app.bank_service.transaction_list)
        total_balance = sum(int(account.balance) for account in self.app.bank_service.accounts_by_id.values())
        self.account_value.configure(text=str(account_count))
        self.transaction_value.configure(text=str(transaction_count))
        self.balance_value.configure(text=format_money_vnd(total_balance))

        last_created = str(self.app.last_created_account_id).strip() or 'Chưa có'
        last_login = str(self.app.last_login_account_id).strip() or 'Chưa có'
        self.recent_info_label.configure(
            text=(
                f'Tài khoản vừa tạo gần nhất: {last_created}\n'
                f'Tài khoản đăng nhập gần nhất: {last_login}\n\n'
                'Bạn có thể dùng nút “Đăng nhập” ở phía trên để chuyển sang màn hình xác thực.'
            )
        )
        self.app.set_status('Đã cập nhật thông tin ở màn hình bắt đầu.')

    def on_show(self) -> None:
        self.refresh_summary()

    def show_project_info(self) -> None:
        messagebox.showinfo(
            'Giới thiệu dự án',
            'Mini Bank là dự án thực hành Python Tkinter dành cho học sinh.\n\n'
            'Nội dung phù hợp để dạy:\n'
            '- Chia giao diện thành nhiều màn hình\n'
            '- Kiểm tra dữ liệu nhập\n'
            '- Gọi lớp nghiệp vụ xử lý giao dịch\n'
            '- Cập nhật dữ liệu và lưu xuống JSON',
        )

    def open_register(self) -> None:
        self.app.show_frame('RegisterFrame')

    def open_login(self) -> None:
        self.app.show_frame('LoginFrame')
