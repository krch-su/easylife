from ninja import Router
from apps.users import services
from apps.users.models import User
from . import schemes

router = Router()


@router.post("/", response=schemes.AddUser)
def add(_, username: str):
    return services.add_user(username)


@router.get("/<user_id>", response=schemes.User)
def get(_, user_id: int):
    return User.objects.with_transactions().get(pk=user_id)


@router.get("/", response=schemes.User)
def get_all(_):
    return User.objects.with_transactions.all()
