import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer handling real-time push notifications.
    Each user joins a channel group based on their user ID.
    """
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
            return

        self.notification_group = f"notifications_{self.user.id}"

        # Join personal notification channel group
        await self.channel_layer.group_add(
            self.notification_group,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "notification_group"):
            await self.channel_layer.group_discard(
                self.notification_group,
                self.channel_name
            )

    # Receive event from group and send it to WebSocket client
    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "notification_id": event["notification_id"],
            "notification_type": event["notification_type"],
            "sender_username": event["sender_username"],
            "content": event["content"],
            "target_id": event.get("target_id")
        }))
