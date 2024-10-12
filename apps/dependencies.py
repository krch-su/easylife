from kink import Container

from apps.finance.abstract import Notifier
from apps.notifications.services import NotificationService

container = Container()
container[Notifier] = NotificationService()
