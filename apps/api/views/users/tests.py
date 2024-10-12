import pytest
from ninja.testing import TestClient

from .handlers import router


@pytest.fixture
def client():
    return TestClient(router_or_app=router)


@pytest.mark.django_db
class TestUserEndpoints:

    def test_add_user_success(
        self, client: TestClient, mocker, staff, auth_headers_staff
    ):

        response = client.post('/', json={
            'username': 'newuser',
            'password': 'password123'
        }, headers=auth_headers_staff)

        assert response.status_code == 200
        assert response.data == 2

    def test_add_user_missing_field(self, client: TestClient, auth_headers_staff):
        response = client.post('/', json={
            'password': 'password123'  # Missing 'username' field
        }, headers=auth_headers_staff)

        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Field required'

    def test_get_user_authorized(self, client: TestClient, user, mocker, auth_headers_user):        # Mock the User model query to return the test user

        response = client.get(f'/{user.id}', headers=auth_headers_user)

        assert response.status_code == 200
        assert response.json()['id'] == user.id

    def test_get_user_unauthorized(self, client: TestClient, mocker, staff, auth_headers_user):
        response = client.get(f'/{staff.id}', headers=auth_headers_user)

        assert response.status_code == 401
        assert response.json()['detail'] == 'Not authorized'

    def test_get_all_users(self, client: TestClient, mocker, user, staff, auth_headers_staff):
        response = client.get('/', headers=auth_headers_staff)

        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]['id'] == 1
        assert response.json()[1]['id'] == 2

    def test_add_user_unauthorized(self, client: TestClient):
        # This should fail because no auth header is provided
        response = client.post('/', json={
            'username': 'newuser',
            'password': 'password123'
        })

        assert response.status_code == 401
