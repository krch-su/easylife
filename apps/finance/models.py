from django.db import models
from constants import TransactionType


class Transaction(models.Model):
    id = models.BigAutoField()
    type = models.IntegerField(choices=TransactionType)
    amount = models.DecimalField(
        decimal_places=2
    )
    date = models.DateTimeField(auto_now=True)
