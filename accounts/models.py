from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model representing Facebook Messenger user profiles.
    """
    avatar = models.ImageField(
        upload_to="avatars/", 
        default="avatars/default_avatar.png", 
        blank=True
    )
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username


class Contact(models.Model):
    """
    Represents an established friendship or contact connection between two users.
    Ensures a single record represents the bidirectional connection.
    """
    user1 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="contacts_initiated"
    )
    user2 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="contacts_received"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.user1.username} & {self.user2.username}"


class FriendRequest(models.Model):
    """
    Represents a friendship request from one user to another.
    """
    STATUS_CHOICES = (
        ("pending", "Đang chờ"),
        ("accepted", "Đã đồng ý"),
        ("rejected", "Đã từ chối"),
    )
    
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="sent_friend_requests"
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="received_friend_requests"
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("sender", "receiver")

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"
