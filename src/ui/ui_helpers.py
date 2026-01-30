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