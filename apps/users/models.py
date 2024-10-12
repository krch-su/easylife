from __future__ import annotations
import deal
from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager as DefaultUserManager
from django.db.models import CharField, DateTimeField, QuerySet, BigAutoField, BooleanField


class UserManager(DefaultUserManager):

    def with_transactions(self):
        return self.prefetch_related('transactions')


class User(AbstractBaseUser, PermissionsMixin):
    username = CharField(max_length=64, unique=True)
    created_at = DateTimeField(auto_now=True)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()
