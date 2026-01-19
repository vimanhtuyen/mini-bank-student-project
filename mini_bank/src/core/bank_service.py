from typing import Dict, Any, List, Optional, Tuple
from src.core.models import Account, Transaction, get_current_time_text


class BankService:
    """
    Lớp xử lý nghiệp vụ Mini Bank:
    - Tạo tài khoản
    - Xác thực đăng nhập
    - Nạp / Rút / Chuyển khoản
    - Lấy số dư
    - Lấy lịch sử giao dịch
    """

    def __init__(self, bank_data: Dict[str, Any]):
        self.bank_data = bank_data

        self.accounts_by_id: Dict[str, Account] = {}
        self.transaction_list: List[Transaction] = []

        for account_dict in self.bank_data.get("accounts", []):
            account = Account.from_dictionary(account_dict)
            self.accounts_by_id[account.account_id] = account

        for transaction_dict in self.bank_data.get("transactions", []):
            transaction = Transaction.from_dictionary(transaction_dict)
            self.transaction_list.append(transaction)

    # -------------------------
    # Các hàm kiểm tra dữ liệu
    # -------------------------
    def is_pin_code_valid(self, pin_code: str) -> bool:
        if not pin_code.isdigit():
            return False
        if len(pin_code) < 4 or len(pin_code) > 6:
            return False
        return True

    def is_amount_valid(self, amount: int) -> bool:
        if not isinstance(amount, int):
            return False
        if amount <= 0:
            return False
        return True

    # -------------------------
    # Tạo ID
    # -------------------------
    def create_new_account_id(self) -> str:
        new_id = str(int(self.bank_data["next_account_id"]))
        self.bank_data["next_account_id"] = int(self.bank_data["next_account_id"]) + 1
        return new_id

    def create_new_transaction_id(self) -> str:
        number = int(self.bank_data["next_transaction_number"])
        self.bank_data["next_transaction_number"] = number + 1
        return f"TRANSACTION_{number:08d}"

    # -------------------------
    # Đồng bộ dữ liệu để lưu file
    # -------------------------
    def build_snapshot_data(self) -> Dict[str, Any]:
        self.bank_data["accounts"] = [account.to_dictionary() for account in self.accounts_by_id.values()]
        self.bank_data["transactions"] = [transaction.to_dictionary() for transaction in self.transaction_list]
        return self.bank_data

    # -------------------------
    # API chính
    # -------------------------
    def create_account(self, owner_name: str, pin_code: str, initial_balance: int) -> Tuple[bool, str, Optional[str]]:
        owner_name = owner_name.strip()

        if owner_name == "":
            return False, "Tên chủ tài khoản không được để trống.", None

        if not self.is_pin_code_valid(pin_code):
            return False, "PIN không hợp lệ. PIN phải gồm 4 đến 6 chữ số.", None

        if initial_balance < 0:
            return False, "Số dư ban đầu không được âm.", None

        account_id = self.create_new_account_id()
        new_account = Account(
            account_id=account_id,
            owner_name=owner_name,
            pin_code=pin_code,
            balance=int(initial_balance),
            created_at=get_current_time_text(),
        )
        self.accounts_by_id[account_id] = new_account

        if initial_balance > 0:
            self.add_transaction(
                transaction_type="DEPOSIT",
                amount=int(initial_balance),
                note="Nạp tiền ban đầu",
                from_account_id=None,
                to_account_id=account_id,
            )

        return True, f"Tạo tài khoản thành công. Số tài khoản: {account_id}", account_id

    def authenticate_login(self, account_id: str, pin_code: str) -> Tuple[bool, str]:
        account = self.accounts_by_id.get(str(account_id))
        if account is None:
            return False, "Không tồn tại số tài khoản."
        if account.pin_code != str(pin_code):
            return False, "PIN không đúng."
        return True, "Đăng nhập thành công."

    def get_account(self, account_id: str) -> Optional[Account]:
        return self.accounts_by_id.get(str(account_id))

    def get_balance(self, account_id: str) -> Tuple[bool, str, Optional[int]]:
        account = self.get_account(account_id)
        if account is None:
            return False, "Không tồn tại số tài khoản.", None
        return True, "OK", account.balance

    def add_transaction(
        self,
        transaction_type: str,
        amount: int,
        note: str,
        from_account_id: Optional[str],
        to_account_id: Optional[str],
    ) -> None:
        transaction = Transaction(
            transaction_id=self.create_new_transaction_id(),
            transaction_type=transaction_type,
            amount=int(amount),
            time_text=get_current_time_text(),
            note=note.strip(),
            from_account_id=from_account_id,
            to_account_id=to_account_id,
        )
        self.transaction_list.append(transaction)

    def deposit_money(self, account_id: str, amount: int, note: str) -> Tuple[bool, str]:
        account = self.get_account(account_id)
        if account is None:
            return False, "Không tồn tại số tài khoản."

        if not self.is_amount_valid(amount):
            return False, "Số tiền nạp phải là số nguyên dương."

        account.balance = account.balance + int(amount)

        self.add_transaction(
            transaction_type="DEPOSIT",
            amount=int(amount),
            note=note,
            from_account_id=None,
            to_account_id=account.account_id,
        )
        return True, "Nạp tiền thành công."

    def withdraw_money(self, account_id: str, amount: int, note: str) -> Tuple[bool, str]:
        account = self.get_account(account_id)
        if account is None:
            return False, "Không tồn tại số tài khoản."

        if not self.is_amount_valid(amount):
            return False, "Số tiền rút phải là số nguyên dương."

        if int(amount) > account.balance:
            return False, "Không đủ số dư để rút."

        account.balance = account.balance - int(amount)

        self.add_transaction(
            transaction_type="WITHDRAW",
            amount=int(amount),
            note=note,
            from_account_id=account.account_id,
            to_account_id=None,
        )
        return True, "Rút tiền thành công."

    def transfer_money(self, from_account_id: str, to_account_id: str, amount: int, note: str) -> Tuple[bool, str]:
        from_account = self.get_account(from_account_id)
        if from_account is None:
            return False, "Tài khoản chuyển không tồn tại."

        to_account = self.get_account(to_account_id)
        if to_account is None:
            return False, "Tài khoản nhận không tồn tại."

        if str(from_account_id) == str(to_account_id):
            return False, "Không thể chuyển khoản cho chính mình."

        if not self.is_amount_valid(amount):
            return False, "Số tiền chuyển phải là số nguyên dương."

        if int(amount) > from_account.balance:
            return False, "Không đủ số dư để chuyển."

        money = int(amount)
        from_account.balance = from_account.balance - money
        to_account.balance = to_account.balance + money

        self.add_transaction(
            transaction_type="TRANSFER_OUT",
            amount=money,
            note=note,
            from_account_id=from_account.account_id,
            to_account_id=to_account.account_id,
        )
        self.add_transaction(
            transaction_type="TRANSFER_IN",
            amount=money,
            note=note,
            from_account_id=from_account.account_id,
            to_account_id=to_account.account_id,
        )

        return True, "Chuyển khoản thành công."

    def get_transaction_history(self, account_id: str) -> List[Transaction]:
        account_id_text = str(account_id)
        history: List[Transaction] = []

        for transaction in self.transaction_list:
            if transaction.from_account_id == account_id_text or transaction.to_account_id == account_id_text:
                history.append(transaction)

        # Sắp xếp mới nhất trước (theo time_text dạng YYYY-MM-DD HH:MM:SS)
        history.sort(key=lambda item: item.time_text, reverse=True)
        return history
