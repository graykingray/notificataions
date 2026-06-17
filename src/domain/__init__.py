from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import datetime


@dataclass(frozen=True)
class BusinessEvent:
    id: UUID
    event_type: str
    payload: dict
    occurred_at: datetime


@dataclass
class NotificationSubscription:
    id: UUID
    event_type: str
    target_url: str
    enabled: bool = True

    def matches(self, event: BusinessEvent) -> bool:
        return (
            self.enabled
            and self.event_type == event.event_type
        )

@dataclass
class NotificationDelivery:
    id: UUID
    event_id: UUID
    subscription_id: UUID

    attempts: int = 0

    delivered_at: datetime | None = None
    last_error: str | None = None

    @property
    def delivered(self) -> bool:
        return self.delivered_at is not None

    def mark_delivered(self, delivered_at: datetime) -> None:
        self.delivered_at = delivered_at
        self.last_error = None

    def mark_failed(self, error: str) -> None:
        self.attempts += 1
        self.last_error = error

    @classmethod
    def create(
        cls,
        event_id: UUID,
        subscription_id: UUID,
    ) -> "NotificationDelivery":
        return cls(
            id=uuid4(),
            event_id=event_id,
            subscription_id=subscription_id,
        )