from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest

from .constants import NotificationTypes
from .models import Notification
from .services import NotificationService
from ..finance.constants import TransactionType


@pytest.fixture
def transaction(user):
    # Create a mock transaction object
    return MagicMock(
        user=user,
        pk=1,
        id=1,
        type=TransactionType.DEPOSIT,
        date=datetime(2004, 1, 1, 0, 0, 0),
        amount=100.0
    )


@pytest.fixture
def notifiers():
    return [MagicMock(), MagicMock()]


@pytest.fixture
def notification_service(notifiers):
    return NotificationService(notifiers=notifiers)


def test_new_transaction_creates_notification(transaction, notification_service):
    n = notification_service.create_new_tx_notification(transaction)
    notification = Notification.objects.filter(pk=n.id).first()

    assert notification
    assert notification.user == transaction.user
    assert notification.type == NotificationTypes.NEW_TRANSACTION
    assert notification.context == {
        'recipient': transaction.user.username,
        'transaction_id': transaction.id,
        'transaction_type': transaction.type,
        'date': '2004-01-01T00:00:00',
        'amount': transaction.amount,
    }


def test_notifiers_are_called(transaction, notification_service, notifiers):
    n = notification_service.create_new_tx_notification(transaction)
    notification_service.notify_async(n)
    for notifier in notifiers:
        notification = Notification.objects.get(pk=n.id)
        notifier.assert_called_once_with(notification)

