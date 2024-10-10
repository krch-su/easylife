from django.db.models import IntegerChoices


class TransactionType(IntegerChoices):
    INCOMING = 1, 'incoming'
    OUTGOING = 2, 'outgoing'
