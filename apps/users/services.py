from typing import NewType

import deal

from .models import User

UserID = NewType('UserID', int)


@deal.pre(lambda _: len(_.username) > 5, message='Username is too short')
@deal.pre(lambda _: len(_.password) > 5, message='Password id too short')
def add_user(username: str, password: str) -> UserID:
    user = User(
        username=username,
        password=password,
    )
    user.save()
    return UserID(user.id)
