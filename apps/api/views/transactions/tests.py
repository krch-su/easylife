import pytest
from ninja.testing import TestClient

from apps.finance.abstract import Notifier
from apps.finance.constants import TransactionType
from .handlers import router


@pytest.fixture
def client():
    return TestClient(router_or_app=router)


@pytest.mark.django_db
class TestAddTransaction:
    def test_add_transaction_success(
            self,
            client: TestClient,
            user,
            auth_headers_staff,
            container
    ):
        response = client.post('/', json={
                "user_id": user.pk,
                "amount": 100.00,
                "transaction_type": TransactionType.DEPOSIT.value,

        }, headers=auth_headers_staff)
        assert response.status_code == 200
        assert response.data == 1
        container[Notifier].new_transaction.assert_called_once()

    @pytest.mark.django_db
    def test_add_transaction_invalid_amount(self, client: TestClient, user, auth_headers_staff):
        response = client.post('/', json={
            "user_id": user.id,
            "amount": -50.00,  # Invalid amount
            "transaction_type": TransactionType.DEPOSIT,
        }, headers=auth_headers_staff)
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Value error, Amount should be greater than 0'

    @pytest.mark.django_db
    def test_add_transaction_missing_field(self, client: TestClient, user, auth_headers_staff):
        response = client.post('/', json={
            "user_id": user.id,
            "transaction_type": TransactionType.DEPOSIT.value,  # Missing amount
        }, headers=auth_headers_staff)

        assert response.status_code == 422
        assert response.json()['detail'] == [{'type': 'missing', 'loc': ['body', 'data', 'amount'], 'msg': 'Field required'}]


    @pytest.mark.django_db
    def test_add_transaction_unauthorized(self, client: TestClient):
        response = client.post('/', json={
            "user_id": 1,
            "amount": 100.00,
            "transaction_type": TransactionType.DEPOSIT,
        })

        assert response.status_code == 401

    @pytest.mark.django_db
    def test_add_transaction_unauthorized_user(self, client: TestClient, auth_headers_user):
        response = client.post('/', jsno={
            "user_id": 1,
            "amount": 100.00,
            "transaction_type": TransactionType.DEPOSIT,
        }, headers=auth_headers_user)

        assert response.status_code == 401
