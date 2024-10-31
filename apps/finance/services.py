from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import NewType, List

from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.db.transaction import atomic, on_commit

from . import abstract, models
from .constants import TransactionType
from .models import Transaction

TransactionID = NewType('TransactionID', int)


class ServiceError(Exception):
    pass


@atomic
def add_transaction(
        user_id: int,
        amount: Decimal,
        transaction_type: TransactionType,
        notifier: abstract.NotificationService
) -> TransactionID:
    if amount <= 0:
        raise ServiceError('Transaction amount should be greater than 0')

    transaction = models.Transaction(
        user_id=user_id,
        amount=amount,
        date=datetime.now(),
        type=transaction_type
    )
    transaction.save()

    notification = notifier.create_new_tx_notification(transaction)

    on_commit(lambda: notifier.notify_async(notification))
    return transaction.pk


@dataclass
class Statistics:
    total_transactions: int
    total_sum: float
    start_date: datetime
    end_date: datetime
    chart_labels: List[str]
    chart_data: List[float]


def get_statistics(
        start_date: datetime,
        end_date: datetime
) -> Statistics:
    transactions = Transaction.objects.filter(date__range=[start_date, end_date])
    total_transactions = transactions.count()

    transactions = (
        transactions
        .annotate(date_only=TruncDate('date'))
        .values('date_only')
        .annotate(daily_total=Sum('amount'))
        .order_by('date_only')
    )

    total_sum = transactions.aggregate(total=Sum('daily_total'))['total'] or 0

    chart_labels = [t['date_only'].isoformat() for t in transactions]
    chart_data = [float(t['daily_total']) for t in transactions]
    return Statistics(
        total_transactions=total_transactions,
        total_sum=total_sum,
        start_date=start_date,
        end_date=end_date,
        chart_labels=chart_labels,
        chart_data=chart_data
    )
