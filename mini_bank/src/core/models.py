from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


def get_current_time_text() -> str:
    """Trả về thời gian hiện tại theo định dạng dễ đọc."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class Account:
    """Thông tin một tài khoản ngân hàng."""
    account_id: str
    owner_name: str
    pin_code: str
    balance: int
    created_at: str

    def to_dictionary(self) -> Dict[str, Any]:
        return {
            "account_id": self.account_id,
            "owner_name": self.owner_name,
            "pin_code": self.pin_code,
            "balance": self.balance,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dictionary(data: Dict[str, Any]) -> "Account":
        return Account(
            account_id=str(data["account_id"]),
            owner_name=str(data["owner_name"]),
            pin_code=str(data["pin_code"]),
            balance=int(data.get("balance", 0)),
            created_at=str(data.get("created_at", get_current_time_text())),
        )


@dataclass
class Transaction:
    """Thông tin một giao dịch."""
    transaction_id: str
    transaction_type: str  # DEPOSIT, WITHDRAW, TRANSFER_IN, TRANSFER_OUT
    amount: int
    time_text: str
    note: str
    from_account_id: Optional[str]
    to_account_id: Optional[str]

    def to_dictionary(self) -> Dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "time_text": self.time_text,
            "note": self.note,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
        }

    @staticmethod
    def from_dictionary(data: Dict[str, Any]) -> "Transaction":
        return Transaction(
            transaction_id=str(data["transaction_id"]),
            transaction_type=str(data["transaction_type"]),
            amount=int(data["amount"]),
            time_text=str(data.get("time_text", get_current_time_text())),
            note=str(data.get("note", "")),
            from_account_id=data.get("from_account_id"),
            to_account_id=data.get("to_account_id"),
        )
