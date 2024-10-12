from __future__ import annotations

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import QuerySet

from apps.notifications.constants import NotificationTypes


class Notification(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING
    )

    type = models.CharField(
        max_length=256,
        choices=NotificationTypes
    )
    context = models.JSONField(encoder=DjangoJSONEncoder)
    created_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True)

    objects: QuerySet[Notification]
