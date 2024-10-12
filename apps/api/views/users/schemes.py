from __future__ import annotations

from typing import List

from ninja import Schema
from pydantic import Field

from apps.users.constants import MIN_USERNAME_LEN, MIN_PASSWORD_LEN
from ..transactions.schemes import Transaction


class User(Schema):
    id: int
    username: str
    transactions: List[Transaction] = Field(default_factory=list)


class AddUser(Schema):
    username: str = Field(min_length=MIN_USERNAME_LEN)
    password: str = Field(min_length=MIN_PASSWORD_LEN)
