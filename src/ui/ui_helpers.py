def format_money_vnd(money: int)-> str:
    text = f"{int(money):,}".replace(",", ".")
    return text +" VND"

def read_non_negative_integer(text: str)-> int:
    text = text.strip()
    if text == "":
        return -1
    if text.startswith("-"):
        return -1
    if not text.isdigit():
        return -1
    return int(text)


def read_positive_integer(text: str) -> int:
    value = read_non_negative_integer(text)
    if value <= 0:
        return -1
    return value

def get_transcation_type_display(transcation_type: str) -> str:
    mapping = {
        "DEPOSIT": "NAP TIEN",
        "WITHDRAW": "RUT TIEN",
        "TRANSFER_OUT": "CHUYEN TIEN DI",
        "TRANSFER_IN": "CHUYEN TIEN DEN",
    }
    return mapping.get(str(transcation_type), str(transcation_type))

def is_pin_format_valid(pin_code: str) -> bool:
    pin_code = str(pin_code).strip()
    if not pin_code.isdigit():
        return False
    if len(pin_code) < 4 or len(pin_code) > 6:
        return False
    return True

