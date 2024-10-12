import deal
from typing import NewType
from decimal import Decimal
from . import abstract, models
from .constants import TransactionType

TransactionID = NewType('TransactionID', int)


@deal.pre(
    lambda _: _.amount > 0,
    message='Transaction amount should be greater than 0'
)
def add_transaction(
        user_id: int,
        amount: Decimal,
        transaction_type: TransactionType,
        notifier: abstract.Notifier
) -> TransactionID:
    transaction = models.Transaction(
        user_id=user_id,
        amount=amount,
        type=transaction_type
    )
    transaction.save()
    notifier.new_transaction(transaction)
    return transaction.pk
