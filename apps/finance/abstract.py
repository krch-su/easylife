import deal
from typing import Protocol

from . import models


class Notifier(Protocol):
    def new_transaction(
            self, transaction: models.Transaction
    ) -> None:
        ...
