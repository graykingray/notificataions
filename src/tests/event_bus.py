class FakeNotificationBus:
    def __init__(self):
        self.sent = []

    def send_http_notification(self, target_url, payload, correlation_id=None):
        self.sent.append({
            "target_url": target_url,
            "payload": payload,
            "correlation_id": correlation_id,
        })