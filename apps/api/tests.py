import pytest
import deal
from unittest.mock import MagicMock
from django.http import HttpRequest
from .auth_backends import JWTAuth
from apps.users.models import User


@pytest.fixture
def mock_request():
    return HttpRequest()


@pytest.fixture
def mock_user():
    return MagicMock(spec=User)


@pytest.fixture
def mock_jwt_auth(mocker):
    """Fixture to mock the base class authentication method."""
    return mocker.patch('ninja_jwt.authentication.JWTAuth.authenticate')


def test_authenticate_with_valid_token_and_permissions(mock_jwt_auth, mock_user, mock_request):
    # Mock the valid token and user
    mock_jwt_auth.return_value = mock_user

    # Define permissions that all return True
    permissions = [lambda u: True, lambda u: True]
    jwt_auth = JWTAuth(permissions=permissions)

    # Authenticate the user
    result = jwt_auth.authenticate(mock_request, 'valid_token')

    # Assert that the user is authenticated
    assert result == mock_user


def test_authenticate_with_valid_token_but_failing_permissions(mock_jwt_auth, mock_user, mock_request):
    # Mock the valid token and user
    mock_jwt_auth.return_value = mock_user

    # Define permissions, one of which returns False
    permissions = [lambda u: True, lambda u: False]
    jwt_auth = JWTAuth(permissions=permissions)

    # Authenticate the user
    result = jwt_auth.authenticate(mock_request, 'valid_token')

    # Assert that the user is not authenticated
    assert result is None


def test_authenticate_with_invalid_token(mock_jwt_auth, mock_request):
    # Mock invalid token
    mock_jwt_auth.return_value = None

    # Create instance of JWTAuth
    jwt_auth = JWTAuth()

    # Authenticate the user
    result = jwt_auth.authenticate(mock_request, 'invalid_token')

    # Assert that no user is authenticated
    assert result is None


def test_authenticate_with_no_permissions(mock_jwt_auth, mock_user, mock_request):
    # Mock the valid token and user
    mock_jwt_auth.return_value = mock_user

    # Authenticate the user without any permissions
    jwt_auth = JWTAuth()
    result = jwt_auth.authenticate(mock_request, 'valid_token')

    # Assert that the user is authenticated
    assert result == mock_user
