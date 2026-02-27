import tkinter as tk
from tkinter import ttk

from src.ui.ui_helpers import (
    format_money_vnd,
    get_transaction_type_display,
    normalize_text_for_search,
    is_date_yyyy_mm_dd_valid,
    is_time_in_date_range)


class HistoryWindow(tk.Toplevel):

    def __init__(self, parent, bank_service, account_id: str):
        super().__init__(parent)
        self.title("Lịch sử giao dịch")
        self.geometry("980x440")
        self.resizable(True, True)

        self.bank_service = bank_service
        self.account_id = str(account_id)

        ttk.Label(self, text="Lịch sử giao dịch", font=("Segoe UI", 12, "bold")).pack(pady=6)

        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x", padx=10, pady=4)

        ttk.Label(control_frame, text="Lọc loại:").grid(row=0, column=0, padx=6, pady=4, sticky="w")
        self.filter_value = tk.StringVar(value="Tất cả")
        self.filter_combo = ttk.Combobox(
            control_frame,
            textvariable=self.filter_value,
            values=["Tất cả", "Nạp tiền", "Rút tiền", "Chuyển đi", "Chuyển đến"],
            width=14,
            state="readonly",
        )
        self.filter_combo.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(control_frame, text="Tìm ghi chú:").grid(row=0, column=2, padx=6, pady=4, sticky="w")
        self.search_entry = ttk.Entry(control_frame, width=30)
        self.search_entry.grid(row=0, column=3, padx=6, pady=4)

        ttk.Button(control_frame, text="Làm mới", command=self.refresh_table, width=12).grid(row=0, column=4, padx=6, pady=4)

        columns = ("time_text", "transaction_id", "transaction_type", "amount", "detail", "note")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=14)
        self.tree.pack(fill="both", expand=True, padx=10, pady=8)

        self.tree.heading("time_text", text="Thời gian")
        self.tree.heading("transaction_id", text="Mã giao dịch")
        self.tree.heading("transaction_type", text="Loại")
        self.tree.heading("amount", text="Số tiền")
        self.tree.heading("detail", text="Chi tiết")
        self.tree.heading("note", text="Ghi chú")

        self.tree.column("time_text", width=140, anchor="w")
        self.tree.column("transaction_id", width=150, anchor="w")
        self.tree.column("transaction_type", width=120, anchor="w")
        self.tree.column("amount", width=120, anchor="e")
        self.tree.column("detail", width=260, anchor="w")
        self.tree.column("note", width=170, anchor="w")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_table())

        ttk.Button(self, text="Đóng", command=self.destroy, width=16).pack(pady=6)

        self.refresh_table()

    def clear_table(self) -> None:
        for item_id in self.tree.get_children():
            self.tree.delete(item_id)

    def is_match_filter(self, display_type: str) -> bool:
        selected = self.filter_value.get()
        if selected == "Tất cả":
            return True
        return display_type == selected

    def is_match_search(self, note_text: str) -> bool:
        keyword = self.search_entry.get().strip().lower()
        if keyword == "":
            return True
        return keyword in str(note_text).lower()

    def refresh_table(self) -> None:
        self.clear_table()

        history = self.bank_service.get_transaction_history(self.account_id)
        for transaction in history:
            display_type = get_transaction_type_display(transaction.transaction_type)
            if not self.is_match_filter(display_type):
                continue
            if not self.is_match_search(transaction.note):
                continue

            detail_text = ""
            if str(transaction.transaction_type).startswith("TRANSFER"):
                detail_text = f"{transaction.from_account_id} -> {transaction.to_account_id}"

            self.tree.insert(
                "",
                "end",
                values=(
                    transaction.time_text,
                    transaction.transaction_id,
                    display_type,
                    format_money_vnd(transaction.amount),
                    detail_text,
                    transaction.note,
                ),
            )
    def export_csv(self) -> None:
        transcation = self.get_filtered_transcation()
        if len(transcation) == 0:
            messagebox.showinfo("Thong bao", "Khong co giao dich nao de xuat")
            return
        
        default_name = f"history"_{self.account_id}.csv"
        file_path = filedialog.asksaveasfilename(
            title="Luu lich su giao dich",
            defaultextension=".ctv",
            initialfile=default_name,
            filetypes=[("CSV files", "*.csv"), ("All files", ".")]

        )
        if not file_path:
            return
        
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Thoi gian", "Ma giao dich", "Loai", "So tien", "Chi tiet", "Ghi chu" ]
                )

                for transaction in transactions:
                    display_type = get_transaction_type_display(transaction.transaction_type)
                    detail_text = ""
                    if str(transaction.transaction_type).startswith("TRANSFER"):
                        detail_text = f"{transaction.from_account_id} -> {transaction.to_account_id}"

                    writer.writerow([
                        transaction.time_text,
                        transaction.transaction_id,
                        display_type,
                        transaction.amount,
                        detail_text,
                        transaction.note,
                    ])
            
            messagebox.showinfo("Thanh cong", f"Da xuat lich su giao dich ra {file_path}")
        except Exception:
            messagebox.showerror("Loi", "Co loi xay ra khi xuat file CSV")

        def on_double_click(self, event = None) -> None:
            selected = self.tree.selection()
            if not selected:
                return
            values = self.tree.item(selected[0], "values")
        
            detail_text = (
            f"Thời gian: {values[0]}\n"
            f"Mã giao dịch: {values[1]}\n"
            f"Loại: {values[2]}\n"
            f"Số tiền: {values[3]}\n"
            f"Chi tiết: {values[4]}\n"
            f"Ghi chú: {values[5]}"
        )

        messagebox.showinfo("Chi tiết giao dịch", detail_text)

