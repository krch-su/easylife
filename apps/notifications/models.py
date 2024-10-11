from __future__ import annotations
from django.db import models
from django.db.models import QuerySet

from apps.notifications.constants import NotificationTypes


class Notification(models.Model):
    id = models.BigAutoField()
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING
    )

    type = models.CharField(
        max_length=256,
        choices=NotificationTypes
    )
    context = models.JSONField()
    created_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField()

    objects: QuerySet[Notification]
