from typing import List

from ninja import Router
from ninja.errors import HttpError

from apps.users import services
from apps.users.models import User
from apps.users.services import ServiceError
from . import schemes
from ...auth_backends import JWTAuth
from ...permissions import staff_only

router = Router(auth=JWTAuth([staff_only]))


@router.post("/")
def add(*_, data: schemes.AddUser):
    try:
        return services.add_user(**data.dict())
    except ServiceError as e:
        raise HttpError(400, str(e))


@router.get("/{user_id}", response=schemes.User, auth=JWTAuth())
def get(request, user_id: int):
    if request.user.id == user_id or request.user.is_staff:
        return User.objects.with_transactions().get(pk=user_id)
    raise HttpError(401, 'Not authorized')


@router.get("/", response=List[schemes.User])
def get_all(*_):
    return User.objects.with_transactions().all()
