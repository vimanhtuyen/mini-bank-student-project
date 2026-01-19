from typing import Optional
from src.storage.json_storage import load_bank_data, save_bank_data
from src.core.bank_service import BankService


DATA_FILE_PATH = "data/bank_data.json"


def format_money_vnd(money: int) -> str:
    text = f"{money:,}".replace(",", ".")
    return text + " VNĐ"


def read_positive_integer(prompt: str) -> Optional[int]:
    """Đọc một số nguyên dương từ bàn phím. Nếu sai thì trả về None."""
    input_text = input(prompt).strip()
    if input_text == "":
        return None
    if not input_text.isdigit():
        return None
    value = int(input_text)
    if value <= 0:
        return None
    return value


def wait_for_enter() -> None:
    input("\nNhấn Enter để tiếp tục...")


def run_application() -> None:
    bank_data = load_bank_data(DATA_FILE_PATH)
    bank_service = BankService(bank_data)

    while True:
        print("\n" + "=" * 60)
        print("MINI BANK - ỨNG DỤNG NGÂN HÀNG MINI (Console)")
        print("=" * 60)
        print("1) Tạo tài khoản mới")
        print("2) Đăng nhập")
        print("3) Thoát")

        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            create_account_screen(bank_service)
            save_bank_data(DATA_FILE_PATH, bank_service.build_snapshot_data())

        elif choice == "2":
            account_id = login_screen(bank_service)
            if account_id is not None:
                session_menu(bank_service, account_id)
                save_bank_data(DATA_FILE_PATH, bank_service.build_snapshot_data())

        elif choice == "3":
            save_bank_data(DATA_FILE_PATH, bank_service.build_snapshot_data())
            print("Đã lưu dữ liệu. Tạm biệt.")
            return

        else:
            print("Lựa chọn không hợp lệ.")
            wait_for_enter()


def create_account_screen(bank_service: BankService) -> None:
    print("\n--- TẠO TÀI KHOẢN ---")
    owner_name = input("Tên chủ tài khoản: ").strip()
    pin_code = input("PIN (4–6 chữ số): ").strip()

    initial_balance_value = input("Số dư ban đầu (VNĐ, Enter nếu 0): ").strip()
    if initial_balance_value == "":
        initial_balance = 0
    elif initial_balance_value.isdigit():
        initial_balance = int(initial_balance_value)
    else:
        print("Số dư ban đầu không hợp lệ. Mặc định = 0.")
        initial_balance = 0

    ok, message, account_id = bank_service.create_account(owner_name, pin_code, initial_balance)
    print(message)

    if ok and account_id is not None:
        ok_balance, _, balance = bank_service.get_balance(account_id)
        if ok_balance and balance is not None:
            print("Số dư hiện tại:", format_money_vnd(balance))

    wait_for_enter()


def login_screen(bank_service: BankService) -> Optional[str]:
    print("\n--- ĐĂNG NHẬP ---")
    account_id = input("Số tài khoản: ").strip()
    pin_code = input("PIN: ").strip()

    ok, message = bank_service.authenticate_login(account_id, pin_code)
    print(message)

    if not ok:
        wait_for_enter()
        return None
    return account_id


def session_menu(bank_service: BankService, account_id: str) -> None:
    while True:
        account = bank_service.get_account(account_id)
        if account is None:
            print("Không tìm thấy tài khoản. Có thể dữ liệu bị lỗi.")
            wait_for_enter()
            return

        print("\n" + "-" * 60)
        print("TÀI KHOẢN:", account.account_id, "| CHỦ TÀI KHOẢN:", account.owner_name)
        print("SỐ DƯ:", format_money_vnd(account.balance))
        print("-" * 60)
        print("1) Nạp tiền")
        print("2) Rút tiền")
        print("3) Chuyển khoản")
        print("4) Xem số dư")
        print("5) Xem lịch sử giao dịch")
        print("6) Đăng xuất")

        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            deposit_screen(bank_service, account_id)
            save_bank_data(DATA_FILE_PATH, bank_service.build_snapshot_data())

        elif choice == "2":
            withdraw_screen(bank_service, account_id)
            save_bank_data(DATA_FILE_PATH, bank_service.build_snapshot_data())

        elif choice == "3":
            transfer_screen(bank_service, account_id)
            save_bank_data(DATA_FILE_PATH, bank_service.build_snapshot_data())

        elif choice == "4":
            ok, _, balance = bank_service.get_balance(account_id)
            if ok and balance is not None:
                print("Số dư hiện tại:", format_money_vnd(balance))
            wait_for_enter()

        elif choice == "5":
            show_history_screen(bank_service, account_id)
            wait_for_enter()

        elif choice == "6":
            print("Đã đăng xuất.")
            return

        else:
            print("Lựa chọn không hợp lệ.")
            wait_for_enter()


def deposit_screen(bank_service: BankService, account_id: str) -> None:
    print("\n--- NẠP TIỀN ---")
    amount = read_positive_integer("Số tiền nạp (VNĐ): ")
    if amount is None:
        print("Số tiền không hợp lệ.")
        wait_for_enter()
        return

    note = input("Ghi chú (Enter nếu bỏ qua): ").strip()
    ok, message = bank_service.deposit_money(account_id, amount, note)
    print(message)
    wait_for_enter()


def withdraw_screen(bank_service: BankService, account_id: str) -> None:
    print("\n--- RÚT TIỀN ---")
    amount = read_positive_integer("Số tiền rút (VNĐ): ")
    if amount is None:
        print("Số tiền không hợp lệ.")
        wait_for_enter()
        return

    note = input("Ghi chú (Enter nếu bỏ qua): ").strip()
    ok, message = bank_service.withdraw_money(account_id, amount, note)
    print(message)
    wait_for_enter()


def transfer_screen(bank_service: BankService, from_account_id: str) -> None:
    print("\n--- CHUYỂN KHOẢN ---")
    to_account_id = input("Số tài khoản nhận: ").strip()

    amount = read_positive_integer("Số tiền chuyển (VNĐ): ")
    if amount is None:
        print("Số tiền không hợp lệ.")
        wait_for_enter()
        return

    note = input("Ghi chú (Enter nếu bỏ qua): ").strip()
    ok, message = bank_service.transfer_money(from_account_id, to_account_id, amount, note)
    print(message)
    wait_for_enter()


def show_history_screen(bank_service: BankService, account_id: str) -> None:
    print("\n--- LỊCH SỬ GIAO DỊCH (mới nhất trước) ---")
    history = bank_service.get_transaction_history(account_id)

    if len(history) == 0:
        print("Chưa có giao dịch.")
        return

    limit_text = input("Xem bao nhiêu giao dịch? (Enter = 10): ").strip()
    if limit_text == "":
        limit = 10
    elif limit_text.isdigit():
        limit = int(limit_text)
    else:
        limit = 10

    if limit < 1:
        limit = 10

    show_list = history[:limit]
    for index, transaction in enumerate(show_list, start=1):
        line = f"{index:02d}) {transaction.time_text} | {transaction.transaction_id} | {transaction.transaction_type} | {format_money_vnd(transaction.amount)}"

        if transaction.transaction_type.startswith("TRANSFER"):
            line += f" | {transaction.from_account_id} -> {transaction.to_account_id}"

        if transaction.note != "":
            line += f" | Ghi chú: {transaction.note}"

        print(line)
