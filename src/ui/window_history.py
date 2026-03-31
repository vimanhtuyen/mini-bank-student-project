import tkinter as tk
from tkinter import ttk, messagebox

from src.ui.ui_helpers import build_transaction_search_text, format_money_vnd, get_transaction_type_display


class HistoryWindow(tk.Toplevel):
    def __init__(self, parent, bank_service, account_id):
        super().__init__(parent)
        self.bank_service = bank_service
        self.account_id = str(account_id)

        self.title(f'Lịch sử giao dịch - {self.account_id}')
        self.geometry('980x620')
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.search_var = tk.StringVar()
        self.summary_var = tk.StringVar(value='')
        self.filter_var = tk.StringVar(value='Tất cả')
        self.all_history = []

        main = ttk.Frame(self, style='Card.TFrame', padding=(20, 18))
        main.pack(fill='both', expand=True)

        ttk.Label(main, text=f'Lịch sử giao dịch của tài khoản {self.account_id}', style='SectionTitle.TLabel').pack(anchor='w')
        ttk.Label(main, text='Bạn có thể lọc theo loại giao dịch hoặc tìm kiếm theo thời gian, ghi chú và mã tài khoản.', style='Surface.TLabel', wraplength=860, justify='left').pack(anchor='w', pady=(6, 14))

        filter_frame = ttk.LabelFrame(main, text='Tìm kiếm và lọc', style='Card.TLabelframe')
        filter_frame.pack(fill='x')
        filter_frame.columnconfigure(1, weight=1)

        ttk.Label(filter_frame, text='Từ khóa', style='Surface.TLabel').grid(row=0, column=0, padx=8, pady=8, sticky='w')
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=34)
        search_entry.grid(row=0, column=1, padx=8, pady=8, sticky='ew')
        search_entry.bind('<KeyRelease>', lambda event: self.apply_filters())

        ttk.Label(filter_frame, text='Loại giao dịch', style='Surface.TLabel').grid(row=0, column=2, padx=8, pady=8, sticky='w')
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=['Tất cả', 'Nạp tiền', 'Rút tiền', 'Chuyển đi', 'Nhận tiền', 'Chuyển khoản'], width=18, state='readonly')
        filter_combo.grid(row=0, column=3, padx=8, pady=8, sticky='w')
        filter_combo.bind('<<ComboboxSelected>>', lambda event: self.apply_filters())

        ttk.Button(filter_frame, text='Làm mới', command=self.refresh_history, style='Secondary.TButton').grid(row=0, column=4, padx=8, pady=8)
        ttk.Button(filter_frame, text='Xóa lọc', command=self.clear_filters, style='Light.TButton').grid(row=0, column=5, padx=8, pady=8)

        table_card = ttk.Frame(main, style='Card.TFrame', padding=(0, 14, 0, 0))
        table_card.pack(fill='both', expand=True)

        columns = ('time', 'type', 'amount', 'note')
        self.tree = ttk.Treeview(table_card, columns=columns, show='headings', height=16)
        self.tree.heading('time', text='Thời gian')
        self.tree.heading('type', text='Loại giao dịch')
        self.tree.heading('amount', text='Số tiền')
        self.tree.heading('note', text='Ghi chú')
        self.tree.column('time', width=170, anchor='center')
        self.tree.column('type', width=140, anchor='center')
        self.tree.column('amount', width=150, anchor='e')
        self.tree.column('note', width=470, anchor='w')
        self.tree.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(table_card, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y', padx=(10, 0))
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind('<Double-1>', self.show_selected_detail)

        bottom_frame = ttk.Frame(main, style='Card.TFrame')
        bottom_frame.pack(fill='x', pady=(14, 0))
        ttk.Label(bottom_frame, textvariable=self.summary_var, style='Strong.TLabel').pack(side='left')
        ttk.Button(bottom_frame, text='Đóng', command=self.destroy, style='Light.TButton').pack(side='right')

        self.refresh_history()
        self.center_window()

    def center_window(self) -> None:
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = max((screen_width - width) // 2, 0)
        y = max((screen_height - height) // 2 - 20, 0)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def refresh_history(self) -> None:
        self.all_history = self.bank_service.get_transaction_history(self.account_id)
        self.apply_filters()

    def clear_filters(self) -> None:
        self.search_var.set('')
        self.filter_var.set('Tất cả')
        self.apply_filters()

    def apply_filters(self) -> None:
        keyword = self.search_var.get().strip().lower()
        selected_type = self.filter_var.get().strip()
        for item_id in self.tree.get_children():
            self.tree.delete(item_id)

        filtered_history = []
        for transaction in self.all_history:
            display_type = get_transaction_type_display(transaction.transaction_type)
            search_text = build_transaction_search_text(transaction)
            if selected_type != 'Tất cả' and display_type != selected_type:
                continue
            if keyword != '' and keyword not in search_text and keyword not in display_type.lower():
                continue
            filtered_history.append(transaction)

        for transaction in filtered_history:
            note_text = str(transaction.note).strip() if str(transaction.note).strip() != '' else '-'
            self.tree.insert('', 'end', values=(transaction.time_text, get_transaction_type_display(transaction.transaction_type), format_money_vnd(transaction.amount), note_text))

        if len(filtered_history) == 0:
            self.tree.insert('', 'end', values=('-', '-', '-', 'Không có giao dịch phù hợp'))

        total_amount = sum(int(getattr(item, 'amount', 0)) for item in filtered_history)
        self.summary_var.set(f'Số giao dịch hiển thị: {len(filtered_history)} | Tổng giá trị: {format_money_vnd(total_amount)}')

    def show_selected_detail(self, event=None) -> None:
        selected_items = self.tree.selection()
        if len(selected_items) == 0:
            return
        values = self.tree.item(selected_items[0], 'values')
        if not values or values[0] == '-':
            return
        messagebox.showinfo('Chi tiết giao dịch', f'Thời gian: {values[0]}\nLoại giao dịch: {values[1]}\nSố tiền: {values[2]}\nGhi chú: {values[3]}')
