import deal
from ninja import Schema
from decimal import Decimal
from datetime import datetime

from pydantic import Field, field_validator

from apps.finance.constants import TransactionType


class Transaction(Schema):
    id: int
    amount: Decimal
    transaction_type: TransactionType = Field(alias='type')
    date: datetime


class AddTransaction(Schema):
    user_id: int
    amount: Decimal
    transaction_type: TransactionType

    @field_validator('amount')
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError('Amount should be greater than 0')
        return v
