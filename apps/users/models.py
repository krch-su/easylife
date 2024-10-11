from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db.models import CharField, DateTimeField, QuerySet, BigAutoField, BooleanField


class UserQuerySet(QuerySet):

    def with_transactions(self):
        return self.select_related('transactions')


class User(AbstractBaseUser, PermissionsMixin):
    id = BigAutoField()
    username = CharField(max_length=64)
    created_at = DateTimeField(auto_now=True)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserQuerySet.as_manager()
