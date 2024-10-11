from datetime import datetime

from celery import shared_task
from django.template.loader import render_to_string

from apps.notifications.models import Notification


@shared_task
def send_email(notification_id: int):
    notification = Notification.objects.get(pk=notification_id)
    print('SENDING EMAIL...')
    print('SUBJECT')
    print(render_to_string(
        template_name=f'./templates/{notification.template_name}_subject.html',
        context=notification.context
    ))
    print('BODY')
    print(render_to_string(
        template_name=f'./templates/{notification.template_name}_body.html',
        context=notification.context
    ))
    notification.sent_at = datetime.utcnow()
    notification.save()


@shared_task
def send_push(notification_id: int):
    notification = Notification.objects.get(pk=notification_id)
    print('SENDING PUSH...')
    print('TITLE')
    print(render_to_string(
        template_name=f'./templates/{notification.type}_push.txt',
        context=notification.context
    ))
    print('TEXT')
    print(render_to_string(
        template_name=f'./templates/{notification.type}_push.txt',
        context=notification.context
    ))
    notification.sent_at = datetime.utcnow()
    notification.save()
