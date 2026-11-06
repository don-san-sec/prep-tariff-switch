"""Customer notifications."""

from __future__ import annotations

from typing import Protocol


class Notifier(Protocol):
    """Sends a notification to a customer.

    Implementations render the named template with the given context and
    deliver it through the app's notification channel.
    """

    def send(self, customer_id: str, template: str, **context: object) -> None:
        ...