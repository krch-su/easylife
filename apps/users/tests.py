import pytest

from apps.users.models import User
from apps.users.services import add_user, ServiceError


@pytest.mark.django_db
class TestAddUser:

    def test_add_user_success(self):
        # Arrange
        username = "testuser"
        password = "securepassword"

        user_id = add_user(username=username, password=password)

        user = User.objects.get(pk=user_id)
        assert user.username == "testuser"
        assert user.password == "securepassword"

    def test_add_user_with_empty_username(self):
        username = ""
        password = "securepassword"

        with pytest.raises(ServiceError):
            add_user(username=username, password=password)

    def test_add_user_with_empty_password(self):
        username = "testuser"
        password = ""

        with pytest.raises(ServiceError):
            add_user(username=username, password=password)

    def test_error_when_username_already_exists(self):
        username = "username"
        password = "securepassword"

        add_user(username=username, password=password)

        with pytest.raises(ServiceError):
            add_user(username=username, password=password)