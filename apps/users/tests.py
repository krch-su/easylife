import pytest
import deal

from apps.users.models import User
from apps.users.services import add_user


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

        with pytest.raises(deal.PreContractError):
            add_user(username=username, password=password)

    def test_add_user_with_empty_password(self):
        username = "testuser"
        password = ""

        with pytest.raises(deal.PreContractError):
            add_user(username=username, password=password)
