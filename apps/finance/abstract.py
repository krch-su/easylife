from typing import Protocol

import models


class Notifier(Protocol):
    def new_transaction(
            self, transaction: models.Transaction
    ) -> None:
        ...
