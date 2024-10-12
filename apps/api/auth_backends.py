from typing import Iterable, Optional, Callable

from django.http import HttpRequest
from ninja_jwt.authentication import JWTAuth as _JWTAuth

from apps.users.models import User

Permission = Callable[[User], bool]


class JWTAuth(_JWTAuth):
    def __init__(self, permissions: Iterable[Permission] = None):
        self._permissions = permissions or []
        super().__init__()

    def authenticate(self, request: HttpRequest, token: str) -> Optional[User]:
        user = super().authenticate(request, token)
        if not all([perm(user) for perm in self._permissions]):
            return None
        return user
