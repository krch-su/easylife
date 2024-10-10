import abc
import models


class Notifier(abc.ABCMeta):
    @abc.abstractmethod
    def notify_new_transaction(self, transaction: models.Transaction):
        ...
