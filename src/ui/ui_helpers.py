import re

BIDV_DARK_BLUE = '#003b73'
BIDV_BLUE = '#005aa9'
BIDV_LIGHT_BLUE = '#eaf3fb'
BIDV_RED = '#da1f26'
BIDV_TEXT = '#16324f'
BIDV_MUTED = '#6e7f93'
BIDV_SURFACE = '#ffffff'
BIDV_BACKGROUND = '#f3f7fb'
BIDV_BORDER = '#d7e3f1'


def read_non_negative_integer(text: str) -> int:
    raw = str(text).strip()
    if raw == '' or not raw.isdigit():
        return -1
    return int(raw)


def read_positive_integer(text: str) -> int:
    value = read_non_negative_integer(text)
    if value <= 0:
        return -1
    return value


def is_pin_format_valid(pin_code: str) -> bool:
    raw = str(pin_code).strip()
    return raw.isdigit() and 4 <= len(raw) <= 6


def normalize_money_text(text: str) -> str:
    raw = str(text).strip()
    raw = re.sub(r'[\s\.,_]', '', raw)
    return raw


def read_money_amount(text: str) -> int:
    raw = normalize_money_text(text)
    if raw == '' or not raw.isdigit():
        return -1
    value = int(raw)
    if value < 0:
        return -1
    return value


def format_money_vnd(amount: int) -> str:
    try:
        value = int(amount)
    except Exception:
        value = 0
    return f'{value:,} VNĐ'.replace(',', '.')


def mask_pin(pin_code: str) -> str:
    raw = str(pin_code)
    return '' if raw == '' else '*' * len(raw)


def get_transaction_type_display(transaction_type: str) -> str:
    raw = str(transaction_type).strip().lower()
    mapping = {
        'deposit': 'Nạp tiền',
        'withdraw': 'Rút tiền',
        'transfer_out': 'Chuyển đi',
        'transfer_in': 'Nhận tiền',
        'transfer': 'Chuyển khoản',
    }
    return mapping.get(raw, str(transaction_type))


def build_transaction_search_text(transaction) -> str:
    parts = [
        str(getattr(transaction, 'transaction_id', '')),
        str(getattr(transaction, 'time_text', '')),
        str(getattr(transaction, 'transaction_type', '')),
        str(getattr(transaction, 'amount', '')),
        str(getattr(transaction, 'note', '')),
        str(getattr(transaction, 'from_account_id', '')),
        str(getattr(transaction, 'to_account_id', '')),
    ]
    return ' '.join(parts).lower()


def short_account_text(account_id: str) -> str:
    raw = str(account_id).strip()
    if len(raw) <= 4:
        return raw
    return f'...{raw[-4:]}'
