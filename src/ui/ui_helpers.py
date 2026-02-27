def format_money_vnd(money: int) -> str:
    """Định dạng tiền kiểu Việt Nam: 1000000 -> 1.000.000 VNĐ"""
    text = f"{int(money):,}".replace(",", ".")
    return text + " VNĐ"


def read_non_negative_integer(text: str) -> int:
    """Đọc số nguyên không âm. Nếu sai, trả về -1."""
    text = text.strip()
    if text == "":
        return -1
    if text.startswith("-"):
        return -1
    if not text.isdigit():
        return -1
    return int(text)


def read_positive_integer(text: str) -> int:
    """Đọc số nguyên dương. Nếu sai, trả về -1."""
    value = read_non_negative_integer(text)
    if value <= 0:
        return -1
    return value


def get_transaction_type_display(transaction_type: str) -> str:
    """Chuyển mã giao dịch sang chữ dễ hiểu."""
    mapping = {
        "DEPOSIT": "Nạp tiền",
        "WITHDRAW": "Rút tiền",
        "TRANSFER_OUT": "Chuyển đi",
        "TRANSFER_IN": "Chuyển đến",
    }
    return mapping.get(str(transaction_type), str(transaction_type))


def is_pin_format_valid(pin_code: str) -> bool:
    """PIN hợp lệ: 4-6 chữ số."""
    pin_code = str(pin_code).strip()
    if not pin_code.isdigit():
        return False
    if len(pin_code) < 4 or len(pin_code) > 6:
        return False
    return True
