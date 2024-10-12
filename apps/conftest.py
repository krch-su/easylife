from unittest.mock import MagicMock

import pytest

from apps.finance.abstract import Notifier
from apps.users.models import User
from ninja_jwt.schema import TokenObtainPairInputSchema


@pytest.fixture(autouse=True)
def container():
    from apps.dependencies import container
    container.clear_cache()
    container[Notifier] = MagicMock(return_value=MagicMock())
    return container


@pytest.fixture(scope='function')
def staff(db):
    user = User(
        username='teststaff',
        password='testpass',
        is_staff=True,
    )
    user.save()
    return user


@pytest.fixture(scope='function')
def user(db):
    user = User(
        username='testuser',
        password='testpass',
    )
    user.save()
    return user


@pytest.fixture
def auth_headers_staff(staff):
    token = TokenObtainPairInputSchema.get_token(staff)
    return {'Authorization': f'Bearer {token["access"]}'}


@pytest.fixture
def auth_headers_user(user):
    token = TokenObtainPairInputSchema.get_token(user)
    return {'Authorization': f'Bearer {token["access"]}'}