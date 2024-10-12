from django.db import models
from django.db.models import DO_NOTHING

from .constants import TransactionType


class Transaction(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=DO_NOTHING,
        related_name='transactions',
    )
    type = models.IntegerField(choices=TransactionType)
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    date = models.DateTimeField(auto_now=True)
