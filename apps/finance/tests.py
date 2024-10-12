from decimal import Decimal

import deal
import pytest

from apps.finance.constants import TransactionType
from apps.finance.models import Transaction
from apps.finance.services import add_transaction


class FakeNotifier:
    def __init__(self):
        self.notifications = []

    def new_transaction(self, transaction):
        self.notifications.append(transaction)


@pytest.mark.django_db
class TestAddTransaction:

    def test_add_transaction_success(self, user):
        notifier = FakeNotifier()
        transaction_id = add_transaction(
            user_id=user.pk,
            amount=Decimal('100.50'),
            transaction_type=TransactionType.DEPOSIT,
            notifier=notifier
        )

        transaction = Transaction.objects.get(pk=transaction_id)
        assert transaction
        assert len(notifier.notifications) == 1
        assert notifier.notifications[0] == transaction

    def test_add_transaction_invalid_amount(self, user):
        with pytest.raises(deal.PreContractError):
            add_transaction(
                user_id=user.pk,
                amount=Decimal('0.00'),
                transaction_type=TransactionType.DEPOSIT,
                notifier=FakeNotifier()
            )

    def test_add_transaction_notifier_called(self, user):
        notifier = FakeNotifier()
        tx_id = add_transaction(
            user_id=user.pk,
            amount=Decimal('50.00'),
            transaction_type=TransactionType.WITHDRAWAL,
            notifier=notifier
        )

        tx = Transaction.objects.get(pk=tx_id)

        assert len(notifier.notifications) == 1
        assert notifier.notifications[0] == tx
