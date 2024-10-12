from typing import NewType
from .constants import MIN_USERNAME_LEN, MIN_PASSWORD_LEN
from .models import User

UserID = NewType('UserID', int)


class ServiceError(Exception):
    pass


def add_user(username: str, password: str) -> UserID:
    if len(username) < MIN_USERNAME_LEN:
        raise ServiceError('Username is too short')
    if len(password) < MIN_PASSWORD_LEN:
        raise ServiceError('Password is too short')

    if User.objects.filter(username=username).exists():
        raise ServiceError('Username is already taken')

    user = User(
        username=username,
        password=password,
    )
    user.save()
    return UserID(user.pk)
