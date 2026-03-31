from tkinter import ttk, messagebox

from src.ui.dialog_money import MoneyDialog
from src.ui.dialog_transfer import TransferDialog
from src.ui.ui_helpers import format_money_vnd, get_transaction_type_display
from src.ui.window_history import HistoryWindow


class DashboardFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, style='App.TFrame')
        self.app = app

        header = ttk.Frame(self, style='Hero.TFrame', padding=(26, 22))
        header.pack(fill='x', pady=(0, 18))
        self.welcome_label = ttk.Label(header, text='Xin chào!', style='HeroTitle.TLabel')
        self.welcome_label.pack(anchor='w')
        self.info_line_label = ttk.Label(header, text='Đang tải thông tin tài khoản...', style='HeroText.TLabel')
        self.info_line_label.pack(anchor='w', pady=(8, 0))

        metrics_wrap = ttk.Frame(self, style='App.TFrame')
        metrics_wrap.pack(fill='x', pady=(0, 16))
        self.account_id_value = self._create_metric_card(metrics_wrap, 0, 'Số tài khoản')
        self.balance_value = self._create_metric_card(metrics_wrap, 1, 'Số dư hiện tại')
        self.transaction_count_value = self._create_metric_card(metrics_wrap, 2, 'Tổng giao dịch')
        self.last_time_value = self._create_metric_card(metrics_wrap, 3, 'Giao dịch gần nhất')

        action_wrap = ttk.Frame(self, style='App.TFrame')
        action_wrap.pack(fill='x', pady=(0, 16))

        left_actions = ttk.Frame(action_wrap, style='Card.TFrame', padding=(22, 18))
        left_actions.pack(side='left', fill='x', expand=True, padx=(0, 10))
        ttk.Label(left_actions, text='Giao dịch nhanh', style='SectionTitle.TLabel').pack(anchor='w')
        row1 = ttk.Frame(left_actions, style='Card.TFrame')
        row1.pack(anchor='w', pady=(14, 0))
        ttk.Button(row1, text='Nạp tiền', command=self.open_deposit, style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), pady=6)
        ttk.Button(row1, text='Rút tiền', command=self.open_withdraw, style='Secondary.TButton').grid(row=0, column=1, padx=(0, 10), pady=6)
        ttk.Button(row1, text='Chuyển khoản', command=self.open_transfer, style='Light.TButton').grid(row=0, column=2, pady=6)
        row2 = ttk.Frame(left_actions, style='Card.TFrame')
        row2.pack(anchor='w', pady=(10, 0))
        ttk.Button(row2, text='Lịch sử giao dịch', command=self.open_history, style='Secondary.TButton').grid(row=0, column=0, padx=(0, 10))
        ttk.Button(row2, text='Copy số tài khoản', command=self.copy_account_id, style='Light.TButton').grid(row=0, column=1, padx=(0, 10))
        ttk.Button(row2, text='Làm mới', command=self.refresh_information, style='Light.TButton').grid(row=0, column=2)

        right_actions = ttk.Frame(action_wrap, style='Card.TFrame', padding=(22, 18))
        right_actions.pack(side='right', fill='y')
        ttk.Label(right_actions, text='Phiên làm việc', style='SectionTitle.TLabel').pack(anchor='w')
        ttk.Label(right_actions, text='Nhấn F5 để tải lại dữ liệu đang hiển thị.', style='Surface.TLabel', wraplength=240, justify='left').pack(anchor='w', pady=(8, 14))
        ttk.Button(right_actions, text='Đăng xuất', command=self.logout, style='Danger.TButton').pack(anchor='w')

        history_card = ttk.Frame(self, style='Card.TFrame', padding=(22, 18))
        history_card.pack(fill='both', expand=True)
        top_bar = ttk.Frame(history_card, style='Card.TFrame')
        top_bar.pack(fill='x')
        ttk.Label(top_bar, text='5 giao dịch gần nhất', style='SectionTitle.TLabel').pack(side='left')
        ttk.Label(top_bar, text='Nhấn đúp vào bảng để mở lịch sử đầy đủ', style='Muted.TLabel').pack(side='right')

        columns = ('time', 'type', 'amount', 'note')
        self.transaction_tree = ttk.Treeview(history_card, columns=columns, show='headings', height=11)
        self.transaction_tree.heading('time', text='Thời gian')
        self.transaction_tree.heading('type', text='Loại')
        self.transaction_tree.heading('amount', text='Số tiền')
        self.transaction_tree.heading('note', text='Ghi chú')
        self.transaction_tree.column('time', width=170, anchor='center')
        self.transaction_tree.column('type', width=130, anchor='center')
        self.transaction_tree.column('amount', width=150, anchor='e')
        self.transaction_tree.column('note', width=520, anchor='w')
        self.transaction_tree.pack(side='left', fill='both', expand=True, pady=(14, 0))

        scrollbar = ttk.Scrollbar(history_card, orient='vertical', command=self.transaction_tree.yview)
        scrollbar.pack(side='right', fill='y', pady=(14, 0), padx=(10, 0))
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        self.transaction_tree.bind('<Double-1>', lambda event: self.open_history())

    def _create_metric_card(self, parent, column_index: int, title: str):
        card = ttk.Frame(parent, style='Card.TFrame', padding=(18, 16))
        card.grid(row=0, column=column_index, sticky='nsew', padx=(0, 10) if column_index < 3 else 0)
        parent.columnconfigure(column_index, weight=1)
        ttk.Label(card, text=title, style='CardTitle.TLabel').pack(anchor='w')
        value_label = ttk.Label(card, text='--', style='MetricValue.TLabel')
        value_label.pack(anchor='w', pady=(12, 2))
        ttk.Label(card, text='Dữ liệu hiện tại', style='MetricCaption.TLabel').pack(anchor='w')
        return value_label

    def get_logged_account_id(self) -> str:
        return '' if self.app.logged_account_id is None else str(self.app.logged_account_id)

    def get_logged_account(self):
        return self.app.bank_service.get_account(self.get_logged_account_id())

    def refresh_recent_transactions(self) -> None:
        for item_id in self.transaction_tree.get_children():
            self.transaction_tree.delete(item_id)
        account_id = self.get_logged_account_id()
        if account_id == '':
            return
        history = self.app.bank_service.get_transaction_history(account_id)
        for transaction in history[:5]:
            note_text = str(transaction.note).strip() if str(transaction.note).strip() != '' else '-'
            self.transaction_tree.insert('', 'end', values=(transaction.time_text, get_transaction_type_display(transaction.transaction_type), format_money_vnd(transaction.amount), note_text))
        if len(history) == 0:
            self.transaction_tree.insert('', 'end', values=('-', '-', '-', 'Chưa có giao dịch nào'))

    def refresh_information(self) -> None:
        account = self.get_logged_account()
        if account is None:
            self.welcome_label.configure(text='Chưa có người dùng đăng nhập.')
            self.info_line_label.configure(text='Hãy quay lại màn hình đăng nhập để truy cập dashboard.')
            for label in [self.account_id_value, self.balance_value, self.transaction_count_value, self.last_time_value]:
                label.configure(text='--')
            self.refresh_recent_transactions()
            return

        history = self.app.bank_service.get_transaction_history(account.account_id)
        latest_time = history[0].time_text if history else 'Chưa có'
        self.welcome_label.configure(text=f'Xin chào, {account.owner_name}!')
        self.info_line_label.configure(text=f'Tài khoản {account.account_id} • Ngày tạo {account.created_at}')
        self.account_id_value.configure(text=account.account_id)
        self.balance_value.configure(text=format_money_vnd(account.balance))
        self.transaction_count_value.configure(text=str(len(history)))
        self.last_time_value.configure(text=latest_time)
        self.refresh_recent_transactions()
        self.app.set_status('Đã làm mới thông tin tài khoản.')

    def on_show(self) -> None:
        self.refresh_information()

    def copy_account_id(self) -> None:
        account = self.get_logged_account()
        if account is None:
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(str(account.account_id))
            self.app.set_status('Đã copy số tài khoản vào clipboard.')
            messagebox.showinfo('Copy', 'Đã copy số tài khoản.')
        except Exception:
            messagebox.showwarning('Lỗi', 'Không thể copy vào clipboard.')

    def logout(self) -> None:
        confirm = messagebox.askyesno('Xác nhận', 'Bạn muốn đăng xuất?')
        if not confirm:
            return
        self.app.logged_account_id = None
        self.app.set_status('Đã đăng xuất khỏi tài khoản hiện tại.')
        self.app.show_frame('StartFrame')

    def open_deposit(self) -> None:
        account = self.get_logged_account()
        if account is None:
            return

        def submit(amount: int, note: str):
            ok, message = self.app.bank_service.deposit_money(account.account_id, amount, note)
            if ok:
                self.app.save_data()
                self.refresh_information()
                self.app.set_status(f'Đã nạp {format_money_vnd(amount)} vào tài khoản {account.account_id}.')
            return ok, message

        MoneyDialog(self, 'Nạp tiền', account.balance, submit)

    def open_withdraw(self) -> None:
        account = self.get_logged_account()
        if account is None:
            return

        def submit(amount: int, note: str):
            ok, message = self.app.bank_service.withdraw_money(account.account_id, amount, note)
            if ok:
                self.app.save_data()
                self.refresh_information()
                self.app.set_status(f'Đã rút {format_money_vnd(amount)} từ tài khoản {account.account_id}.')
            return ok, message

        MoneyDialog(self, 'Rút tiền', account.balance, submit)

    def open_transfer(self) -> None:
        account = self.get_logged_account()
        if account is None:
            return

        def on_success():
            self.app.save_data()
            self.refresh_information()
            self.app.set_status(f'Đã thực hiện chuyển khoản từ tài khoản {account.account_id}.')

        TransferDialog(self, self.app.bank_service, account.account_id, on_success)

    def open_history(self) -> None:
        account = self.get_logged_account()
        if account is None:
            return
        HistoryWindow(self, self.app.bank_service, account.account_id)
