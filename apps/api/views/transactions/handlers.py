import deal
from ninja import Router

from apps.api.auth_backends import JWTAuth
from apps.api.permissions import staff_only
from apps.dependencies import container
from apps.finance import services
from apps.finance.abstract import Notifier
from . import schemes

router = Router(auth=JWTAuth([staff_only]))


@router.post("/")
def add_transaction(
        *_, data: schemes.AddTransaction
):
    return services.add_transaction(
        **data.dict(), notifier=container[Notifier]
    )
