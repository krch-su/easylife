from apps.notifications.services import NotificationService


def get_notification_service() -> NotificationService:
    return NotificationService()
