"""Test fakes: a notifier that records instead of delivering."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SentNotification:
    """One notification captured by FakeNotifier."""

    customer_id: str
    template: str
    context: dict[str, object] = field(default_factory=dict)


class FakeNotifier:
    """Records notifications so tests can inspect what was sent."""

    def __init__(self) -> None:
        self.sent: list[SentNotification] = []

    def send(self, customer_id: str, template: str, **context: object) -> None:
        self.sent.append(SentNotification(customer_id, template, dict(context)))