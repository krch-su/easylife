from ninja import Schema
from decimal import Decimal
from datetime import datetime

from pydantic import Field

from apps.finance.constants import TransactionType


class Transaction(Schema):
    amount: Decimal
    type: TransactionType
    date: datetime


class AddTransaction(Schema):
    amount: Decimal
    type: TransactionType = Field(alias='transaction_type')
