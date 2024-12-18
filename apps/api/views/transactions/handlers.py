from ninja import Router
from ninja.errors import HttpError

from apps.api.auth_backends import JWTAuth
from apps.api.permissions import staff_only
from apps.dependencies import container
from apps.finance import services
from apps.finance.abstract import NotificationService
from apps.finance.services import ServiceError
from . import schemes

router = Router(auth=JWTAuth([staff_only]))


@router.post("/")
def add_transaction(*_, data: schemes.AddTransaction):
    try:
        return services.add_transaction(
            **data.dict(), notifier=container[NotificationService]
        )
    except ServiceError as e:
        raise HttpError(400, str(e))
