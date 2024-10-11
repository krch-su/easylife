from typing import NewType
from decimal import Decimal
import abstract
from models import Transaction
from .constants import TransactionType

TransactionID = NewType('TransactionID', int)


def add_transaction(
        user_id: int,
        amount: Decimal,
        transaction_type: TransactionType,
        _notifier: abstract.Notifier
) -> TransactionID:
    transaction = Transaction(
        user_id=user_id,
        amount=amount,
        transaction_type=transaction_type
    )
    transaction.save()
    _notifier.new_transaction(transaction)
    return transaction.id
