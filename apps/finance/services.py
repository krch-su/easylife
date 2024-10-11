from typing import NewType
from decimal import Decimal
import abstract
from models import Transaction
from .constants import TransactionType

TransactionID = NewType('TransactionID', int)


class InvalidTransactionAmount(Exception):
    pass


def add_transaction(
        user_id: int,
        amount: Decimal,
        transaction_type: TransactionType,
        _notifier: abstract.Notifier
) -> TransactionID:
    if amount <= 0:
        raise InvalidTransactionAmount('Transaction amount should be greater than 0')
    transaction = Transaction(
        user_id=user_id,
        amount=amount,
        transaction_type=transaction_type
    )
    transaction.save()
    _notifier.new_transaction(transaction)
    return transaction.id
