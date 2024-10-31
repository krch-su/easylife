from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Iterable, NewType

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

    def create_new_tx_notification(self, transaction: Transaction) -> Notification:
        notification = Notification(
            user=transaction.user,
            type=NotificationTypes.NEW_TRANSACTION,
            context=dict(
                recipient=transaction.user.username,
                transaction_id=transaction.pk,
                transaction_type=transaction.type,
                date=transaction.date,
                amount=transaction.amount,
            )
        )
        notification.save()
        return notification

    def notify_async(self, notification: Notification):
        for notifier in self.notifiers:
            notifier(notification)
