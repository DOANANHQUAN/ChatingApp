import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Conversation, Message, MessageStatus, ConversationParticipant
from accounts.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer handling real-time messaging, typing indicators, and seen status updates.
    """
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"
        self.user = self.scope["user"]

        # Reject connection if user is anonymous (unauthenticated)
        if self.user.is_anonymous:
            await self.close()
            return

        # Check if the user is a participant of this conversation
        is_participant = await self.check_participant(self.user, self.conversation_id)
        if not is_participant:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        # Mark all messages in the conversation as read upon joining
        await self.mark_messages_as_read()

        # Update online status
        await self.update_user_online_status(self.user, True)

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            # Update user's last seen time on disconnect
            await self.update_user_online_status(self.user, False)

    # Receive message from WebSocket (Client -> Server)
    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get("type")

        if event_type == "text_message":
            content = data.get("content")
            if content:
                # Save message to database
                message = await self.save_message(self.user, self.conversation_id, content)
                
                # Broadcast the message to the group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message_id": message.id,
                        "sender_id": self.user.id,
                        "sender_username": self.user.username,
                        "sender_avatar": self.user.avatar.url if self.user.avatar else "/static/images/default_avatar.png",
                        "content": content,
                        "attachments": [],
                        "created_at": message.created_at.strftime("%H:%M - %d/%m/%Y")
                    }
                )
                
        elif event_type == "typing":
            # Broadcast typing indicator to others in the room
            is_typing = data.get("is_typing", False)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_typing",
                    "sender_id": self.user.id,
                    "sender_username": self.user.username,
                    "is_typing": is_typing
                }
            )

        elif event_type == "seen":
            # Mark messages up to message_id as seen
            message_id = data.get("message_id")
            if message_id:
                await self.mark_single_message_as_read(message_id)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_seen",
                        "user_id": self.user.id,
                        "message_id": message_id
                    }
                )

    # Receive message from room group (Server -> Client)
    async def chat_message(self, event):
        # Send message event to client
        await self.send(text_data=json.dumps({
            "type": "message",
            "message_id": event["message_id"],
            "sender_id": event["sender_id"],
            "sender_username": event["sender_username"],
            "sender_avatar": event["sender_avatar"],
            "content": event["content"],
            "attachments": event["attachments"],
            "created_at": event["created_at"]
        }))

    # Receive typing event from room group (Server -> Client)
    async def chat_typing(self, event):
        # Prevent echo to sender
        if event["sender_id"] != self.user.id:
            await self.send(text_data=json.dumps({
                "type": "typing",
                "sender_id": event["sender_id"],
                "sender_username": event["sender_username"],
                "is_typing": event["is_typing"]
            }))

    # Receive seen event from room group (Server -> Client)
    async def chat_seen(self, event):
        await self.send(text_data=json.dumps({
            "type": "seen",
            "user_id": event["user_id"],
            "message_id": event["message_id"]
        }))

    # Database Helpers (Decorated with database_sync_to_async)
    
    @database_sync_to_async
    def check_participant(self, user, conversation_id):
        return ConversationParticipant.objects.filter(
            conversation_id=conversation_id, 
            user=user
        ).exists()

    @database_sync_to_async
    def save_message(self, sender, conversation_id, content):
        conv = Conversation.objects.get(id=conversation_id)
        # Create Message
        message = Message.objects.create(
            conversation=conv,
            sender=sender,
            content=content
        )
        # Create MessageStatus instances for other participants
        participants = ConversationParticipant.objects.filter(conversation=conv).exclude(user=sender)
        for part in participants:
            MessageStatus.objects.create(
                message=message,
                user=part.user,
                is_read=False
            )
        # Update conversation timestamp to sort by active
        conv.save()
        return message

    @database_sync_to_async
    def mark_messages_as_read(self):
        unread = MessageStatus.objects.filter(
            message__conversation_id=self.conversation_id,
            user=self.user,
            is_read=False
        )
        for status in unread:
            status.is_read = True
            status.read_at = timezone.now()
            status.save()

    @database_sync_to_async
    def mark_single_message_as_read(self, message_id):
        status = MessageStatus.objects.filter(
            message_id=message_id,
            user=self.user,
            is_read=False
        ).first()
        if status:
            status.is_read = True
            status.read_at = timezone.now()
            status.save()

    @database_sync_to_async
    def update_user_online_status(self, user, is_online):
        u = User.objects.get(id=user.id)
        u.is_online = is_online
        if not is_online:
            u.last_seen = timezone.now()
        u.save()
