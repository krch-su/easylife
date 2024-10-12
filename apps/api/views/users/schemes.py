from __future__ import annotations

from typing import List

from ninja import Schema
from pydantic import Field

from ..transactions.schemes import Transaction


class User(Schema):
    id: int
    username: str
    transactions: List[Transaction] = Field(default_factory=list)


class AddUser(Schema):
    username: str
    password: str
