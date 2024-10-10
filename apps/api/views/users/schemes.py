from typing import List
from ninja import Schema

from ..transactions.schemes import Transaction


class User(Schema):
    id: int
    username: str
    transactions: List[Transaction]


class AddUser(Schema):
    id: int
