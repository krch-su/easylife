import deal
from apps.users.models import User


def staff_only(user: User):
    return user.is_staff
