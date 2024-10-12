from __future__ import annotations
import deal
from typing import TYPE_CHECKING, Callable, Iterable

from .constants import NotificationTypes
from .models import Notification
from .tasks import send_email, send_push

if TYPE_CHECKING:
    from apps.finance.models import Transaction


Notifier = Callable[[Notification], None]

DEFAULT_NOTIFIERS = (
    lambda x: send_email.delay(x.id),
    lambda x: send_push.delay(x.id),
)


class NotificationService:
    def __init__(self, notifiers: Iterable[Notifier] = DEFAULT_NOTIFIERS):
        self.notifiers = notifiers

    def new_transaction(self, transaction: Transaction):
        notification = Notification(
            user=transaction.user,
            type=NotificationTypes.NEW_TRANSACTION,
            context=dict(
                recipient=transaction.user.username,
                transaction_id=transaction.id,
                transaction_type=transaction.type,
                date=transaction.date,
                amount=transaction.amount,
            )
        )
        notification.save()
        self._notify(notification)

    def _notify(self, notification: Notification):
        for notifier in self.notifiers:
            notifier(notification)
