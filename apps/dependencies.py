from kink import Container

from apps.finance.abstract import NotificationService
from apps.notifications.services import NotificationService

container = Container()
container[NotificationService] = NotificationService()
