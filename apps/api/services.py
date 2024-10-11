from datetime import datetime, timedelta
from typing import Iterable, Callable, Optional, Protocol
from uuid import uuid4

import jwt
from django.views.decorators.debug import sensitive_variables

from apps.users.models import User


Permission = Callable[[User], bool]


class Authenticate(Protocol):
    def __call__(self, username: str, password: str) -> Optional[User]:
        pass


def staff_only(user: User):
    return user.is_staff


class JWTSecurity:
    def __init__(
            self,
            secret: str,
            expiration_delta: timedelta,
            algorithm: str,
            authenticate: Authenticate
    ):
        self.secret = secret
        self.expiration_delta = expiration_delta
        self.algorithm = algorithm
        self._authenticate = authenticate

    def authorize(self, token: str, permissions: Iterable[Permission]) -> Optional[User]:
        data = self._decode_token(token)
        if not data:
            return None

        user = User.objects.filter(pk=data['user_id']).first()

        if not all([perm(user) for perm in permissions]):
            return None
        return user

    @sensitive_variables('password')
    def authenticate(self, username: str, password: str) -> Optional[str]:
        user = self._authenticate(username=username, password=password)
        if not user:
            return None
        jti = str(uuid4())
        payload = {
            'user_id': user.id,
            'username': user.username,
            'jti': jti,
            'exp': datetime.utcnow() + self.expiration_delta,
            'iat': datetime.utcnow(),
        }
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return token

    def _decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
