import os
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_file_size(value):
    """
    Validates that uploaded files do not exceed the configured maximum size.
    """
    filesize = value.size
    if filesize > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(f"Kích thước file tối đa là {settings.MAX_UPLOAD_SIZE / (1024 * 1024):.1f}MB")


class Conversation(models.Model):
    """
    Represents a chat room. Can be 1-1 or a group chat.
    """
    title = models.CharField(max_length=255, blank=True, null=True, help_text="Để trống nếu là chat 1-1")
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Updated when new message is sent

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        if self.is_group:
            return self.title or f"Group Chat {self.id}"
        return f"Private Chat {self.id}"


class ConversationParticipant(models.Model):
    """
    Mapping table linking Users to Conversations with metadata.
    """
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name="participants"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="chat_participations"
    )
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("conversation", "user")

    def __str__(self):
        return f"{self.user.username} in Room {self.conversation.id}"


class Message(models.Model):
    """
    Represents an individual message within a conversation.
    """
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="sent_messages"
    )
    content = models.TextField(blank=True, null=True)  # Can be blank if attachment only
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Msg {self.id} by {self.sender.username} in Room {self.conversation_id}"


class MessageAttachment(models.Model):
    """
    Represents files or images attached to a message.
    """
    FILE_TYPES = (
        ("image", "Hình ảnh"),
        ("video", "Video"),
        ("file", "Tài liệu"),
    )
    
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE, 
        related_name="attachments"
    )
    file = models.FileField(upload_to="attachments/", validators=[validate_file_size])
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default="file")

    def save(self, *args, **kwargs):
        # Infer file type from extension
        ext = os.path.splitext(self.file.name)[1].lower()
        if ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]:
            self.file_type = "image"
        elif ext in [".mp4", ".mov", ".avi", ".mkv"]:
            self.file_type = "video"
        else:
            self.file_type = "file"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Attachment {self.id} ({self.file_type}) for Msg {self.message_id}"


class MessageStatus(models.Model):
    """
    Tracks the read/unread (seen/unseen) status of messages per participant.
    """
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE, 
        related_name="statuses"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="message_statuses"
    )
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("message", "user")

    def __str__(self):
        return f"User {self.user.username} - Msg {self.message_id} (Read: {self.is_read})"
