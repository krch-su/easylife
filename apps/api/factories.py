from functools import cache
from django.contrib.auth import authenticate
from .services import JWTSecurity
import settings


@cache
def get_security_service() -> JWTSecurity:

    return JWTSecurity(
        secret=settings.JWT_SECRET,
        expiration_delta=settings.JWT_EXPIRATION_DELTA,
        algorithm=settings.JWT_ALGORITHM,
        authenticate=authenticate,  # noqa
    )
