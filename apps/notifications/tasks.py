import logging
from datetime import datetime

from celery import shared_task
from django.template.loader import render_to_string

from apps.notifications.models import Notification

logger = logging.getLogger(__name__)


@shared_task
def send_email(notification_id: int):
    notification = Notification.objects.get(pk=notification_id)
    logger.debug('SENDING EMAIL...')
    logger.debug('SUBJECT')
    logger.debug(render_to_string(
        template_name=f'{notification.type}_subject.txt',
        context=notification.context
    ))
    logger.debug('BODY')
    logger.debug(render_to_string(
        template_name=f'{notification.type}_email.html',
        context=notification.context
    ))
    notification.sent_at = datetime.utcnow()
    notification.save()


@shared_task
def send_push(notification_id: int):
    notification = Notification.objects.get(pk=notification_id)
    logger.debug('SENDING PUSH...')
    logger.debug('TITLE')
    logger.debug(render_to_string(
        template_name=f'{notification.type}_subject.txt',
        context=notification.context
    ))
    logger.debug('TEXT')
    logger.debug(render_to_string(
        template_name=f'{notification.type}_push.txt',
        context=notification.context
    ))
    notification.sent_at = datetime.utcnow()
    notification.save()
