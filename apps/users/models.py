from __future__ import annotations

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager as DefaultUserManager
from django.db.models import CharField, DateTimeField, BooleanField


class UserManager(DefaultUserManager):

    def with_transactions(self):
        return self.prefetch_related('transactions')

    def create_user(self, username, password=None, **extra_fields):
        """
        Create and return a user with a username and password.
        """
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and return a superuser with a username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = CharField(max_length=64, unique=True)
    created_at = DateTimeField(auto_now=True)
    is_staff = BooleanField(default=False)
    email = None

    USERNAME_FIELD = 'username'

    objects = UserManager()
