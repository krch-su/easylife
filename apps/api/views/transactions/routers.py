from ninja import Router

from apps.finance import services

from . import schemes

router = Router()


@router.post("/", response=schemes.AddTransaction)
def add_transaction(_, data: schemes.AddTransaction):
    return services.add_transaction(**data.dict(by_alias=True))
