from datetime import UTC, datetime
from typing import Protocol

from src.domain import BusinessEvent, NotificationDelivery, NotificationSubscription


class NotificationBus(Protocol):
    def send_http_notification(
        self,
        target_url: str,
        payload: dict,
        correlation_id: str | None = None,
    ) -> None:
        ...


class SubscriptionRepository(Protocol):
    def find_for_event_type(self, event_type: str) -> list[NotificationSubscription]:
        ...


class DeliveryRepository(Protocol):
    def add(self, delivery: NotificationDelivery) -> None:
        ...


class UnitOfWork(Protocol):
    subscriptions: SubscriptionRepository
    deliveries: DeliveryRepository

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...


def handle_business_fact(event: BusinessEvent, uow: UnitOfWork, bus: NotificationBus) -> None:
    try:
        subscriptions = uow.subscriptions.find_for_event_type(event.event_type)

        for sub in subscriptions:
            delivery = NotificationDelivery.create(
                event_id=event.id,
                subscription_id=sub.id,
            )

            uow.deliveries.add(delivery)

            bus.send_http_notification(
                target_url=sub.target_url,
                payload=event.payload,
                correlation_id=str(event.id),
            )

            delivery.mark_delivered(datetime.now(UTC))

        uow.commit()

    except Exception:
        uow.rollback()
        raise
