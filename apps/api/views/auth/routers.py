from django.contrib.auth import authenticate
from ninja import Router

from apps.finance import services
from . import schemes
from ...factories import get_security_service

router = Router()


@router.post("/login", response=schemes.Login)
def login(_, data: schemes.Login):
    token = get_security_service().authenticate(**data.dict())
    if not token:
        return {'error': 'Invalid credentials'}, 401
    return token
