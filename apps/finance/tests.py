from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from apps.finance.constants import TransactionType
from apps.finance.models import Transaction
from apps.finance.services import add_transaction, ServiceError, get_statistics


class FakeNotifier:
    def __init__(self):
        self.notifications = []

    def create_new_tx_notification(self, transaction):
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
        with pytest.raises(ServiceError):
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


@pytest.fixture
def create_transaction(user):
    def _inner(date: datetime, amount):
        return Transaction.objects.create(
            user=user,
            date=date,
            amount=amount,
            type=TransactionType.DEPOSIT
        )
    return _inner


@pytest.mark.django_db
class TestGetStatistics:

    @pytest.fixture(autouse=True)
    def setup(self):
        # Setup code if needed can go here
        pass

    def test_get_statistics_no_transactions(self):
        # Given
        start_date = datetime.now() - timedelta(days=10)
        end_date = datetime.now() - timedelta(days=5)

        # When
        stats = get_statistics(start_date, end_date)

        # Then
        assert stats.total_transactions == 0
        assert stats.total_sum == 0.0
        assert stats.start_date == start_date
        assert stats.end_date == end_date
        assert stats.chart_labels == []
        assert stats.chart_data == []

    def test_get_statistics_multiple_transactions(self, create_transaction):
        # Given
        start_date = datetime.now() - timedelta(days=10)
        end_date = datetime.now()

        # Create sample transactions
        create_transaction(date=datetime.now() - timedelta(days=9), amount=100.0)
        create_transaction(date=datetime.now() - timedelta(days=9), amount=50.0)
        create_transaction(date=datetime.now() - timedelta(days=8), amount=200.0)
        create_transaction(date=datetime.now() - timedelta(days=7), amount=150.0)

        # When
        stats = get_statistics(start_date, end_date)

        # Then
        assert stats.total_transactions == 4
        assert stats.total_sum == 500.0
        assert stats.start_date == start_date
        assert stats.end_date == end_date
        assert stats.chart_labels == [
            (datetime.now() - timedelta(days=9)).date().isoformat(),
            (datetime.now() - timedelta(days=8)).date().isoformat(),
            (datetime.now() - timedelta(days=7)).date().isoformat(),
        ]
        assert stats.chart_data == [150.0, 200.0, 150.0]  # Adjust if the amount sum per day changes

    def test_get_statistics_with_no_transactions_in_date_range(self, create_transaction):
        # Given
        start_date = datetime.now() - timedelta(days=10)
        end_date = datetime.now() - timedelta(days=9)

        # Create transactions outside the date range
        create_transaction(date=datetime.now() - timedelta(days=11), amount=100.0)
        create_transaction(date=datetime.now() - timedelta(days=12), amount=150.0)

        # When
        stats = get_statistics(start_date, end_date)

        # Then
        assert stats.total_transactions == 0
        assert stats.total_sum == 0.0
        assert stats.start_date == start_date
        assert stats.end_date == end_date
        assert stats.chart_labels == []
        assert stats.chart_data == []

    def test_get_statistics_single_transaction(self, create_transaction):
        # Given
        start_date = datetime.now() - timedelta(days=10)
        end_date = datetime.now()

        # Create a single transaction
        create_transaction(date=datetime.now() - timedelta(days=5), amount=250.0)

        # When
        stats = get_statistics(start_date, end_date)

        # Then
        assert stats.total_transactions == 1
        assert stats.total_sum == 250.0
        assert stats.start_date == start_date
        assert stats.end_date == end_date
        assert stats.chart_labels == [(datetime.now() - timedelta(days=5)).date().isoformat()]
        assert stats.chart_data == [250.0]
