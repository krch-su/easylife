from typing import Protocol

from . import models
from ..notifications.models import Notification


class NotificationService(Protocol):
    def create_new_tx_notification(
            self, transaction: models.Transaction
    ) -> Notification:
        ...

    def notify_async(self, notification: Notification) -> None:
        ...
