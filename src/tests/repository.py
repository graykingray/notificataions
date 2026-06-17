class FakeDeliveryRepository:
    def __init__(self):
        self.items = []

    def add(self, delivery):
        self.items.append(delivery)

class FakeSubscriptionRepository:
    def __init__(self, subscriptions):
        self.subscriptions = subscriptions

    def find_for_event_type(self, event_type):
        return [s for s in self.subscriptions if s.event_type == event_type]

class FakeUnitOfWork:
    def __init__(self, subscriptions):
        self.subscriptions = FakeSubscriptionRepository(subscriptions)
        self.deliveries = FakeDeliveryRepository()
        self.committed = False
        self.rolled_back = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True
