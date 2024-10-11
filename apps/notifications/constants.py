from django.db.models import TextChoices


class NotificationTypes(TextChoices):
    NEW_TRANSACTION = 'new_transaction'
