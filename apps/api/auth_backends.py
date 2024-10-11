from typing import Iterable, Optional

from django.http import HttpRequest
from ninja.security import HttpBearer

from apps.api.factories import get_security_service
from apps.api.services import Permission
from apps.users.models import User


class JWTAuth(HttpBearer):
    def __init__(self, permissions: Iterable[Permission] = None):
        self._permissions = permissions or []
        super().__init__()

    def authenticate(self, request: HttpRequest, token: str) -> Optional[User]:
        return get_security_service().authorize(token, self._permissions)
