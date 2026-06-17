from datetime import datetime, UTC

from src.domain import NotificationSubscription, BusinessEvent
from src.event_polling import handle_business_fact
from src.tests.event_bus import FakeNotificationBus
from src.tests.repository import FakeUnitOfWork


def test_sends_notification_for_matching_subscription():
    sub = NotificationSubscription(
        id="sub-1",
        event_type="WichtigerBusinessFact",
        target_url="https://example.com/hook",
        enabled=True,
    )

    event = BusinessEvent(
        id="event-1",
        event_type="WichtigerBusinessFact",
        payload={"foo": "bar"},
        occurred_at=datetime.now(UTC),
    )

    uow = FakeUnitOfWork([sub])
    bus = FakeNotificationBus()

    handle_business_fact(event, uow, bus)

    assert uow.committed is True
    assert len(uow.deliveries.items) == 1
    assert bus.sent == [
        {
            "target_url": "https://example.com/hook",
            "payload": {"foo": "bar"},
            "correlation_id": "event-1",
        }
    ]
