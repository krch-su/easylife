from typing import NewType
from decimal import Decimal

from apps.finance.constants import TransactionType

TransactionID = NewType('TransactionID', int)


def add_transaction(
        user_id: int,
        amount: Decimal,
        transaction_type: TransactionType,
        _notifier: abstract.Notifier
) -> TransactionID:
    pass
