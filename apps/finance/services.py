from decimal import Decimal
from typing import NewType

from . import abstract, models
from .constants import TransactionType

TransactionID = NewType('TransactionID', int)


class ServiceError(Exception):
    pass


def add_transaction(
        user_id: int,
        amount: Decimal,
        transaction_type: TransactionType,
        notifier: abstract.Notifier
) -> TransactionID:
    if amount <= 0:
        raise ServiceError('Transaction amount should be greater than 0')

    transaction = models.Transaction(
        user_id=user_id,
        amount=amount,
        type=transaction_type
    )
    transaction.save()
    notifier.new_transaction(transaction)
    return transaction.pk
