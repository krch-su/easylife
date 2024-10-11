from django.db.models import IntegerChoices


class TransactionType(IntegerChoices):
    DEPOSIT = 1, 'deposit'
    WITHDRAWAL = 2, 'withdrawal'
