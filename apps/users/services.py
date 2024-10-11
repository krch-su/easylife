from typing import NewType
from .models import User

UserID = NewType('UserID', int)


def add_user(username: str, password: str) -> UserID:
    user = User(
        username=username,
        password=password,
    )
    user.save()
    return UserID(user.id)
