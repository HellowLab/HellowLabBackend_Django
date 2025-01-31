from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth import get_user_model # get the currently active user model
from datetime import datetime

### User Models ###
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(blank=True, null=True, upload_to="profile_pictures/")
    bio = models.TextField(blank=True, null=True, max_length=500)

    def __str__(self):
        return self.username



User = get_user_model()

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE, null=True)
    receiver = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE, null=True)
    status = models.CharField(
        max_length=10,
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')  # Prevent duplicate requests

    def accept(self):
        """Accept the friend request and create a friendship"""
        self.status = "accepted"
        self.save()
        Friendship.objects.create(user1=self.sender, user2=self.receiver)

    def reject(self):
        """Reject the friend request"""
        self.status = "rejected"
        self.save()

    def rescind(self):
        """Rescind the friend request"""
        self.delete()


class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name="friends1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="friends2", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  # Prevent duplicate friendships

    def __str__(self):
        return f"{self.user1} - {self.user2}"

    @classmethod
    def are_friends(cls, user_a, user_b):
        """Check if two users are friends"""
        return cls.objects.filter(
            models.Q(user1=user_a, user2=user_b) | models.Q(user1=user_b, user2=user_a)
        ).exists()


# class FriendRequest(models.Model):
#     from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_friend_requests', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_friend_requests', on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(default=timezone.now)
#     accepted = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Friend request from {self.from_user} to {self.to_user}"

# class Friendship(models.Model):
#     STATUS_CHOICES = [
#         ('P', 'Pending'),
#         ('A', 'Accepted'),
#         ('R', 'Rejected'),
#     ]

#     user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendship1', on_delete=models.CASCADE) # user who initiated friend request
#     user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendship2', on_delete=models.CASCADE) # user who recieved friend request
#     # status = models.Choices(["pending", "accepted", "rejected"])
#     status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
#     friends_since = models.DateTimeField(default=timezone.now) # date of friend request of pending/rejected, date of friendship start if accepted

#     def __str__(self):
#         return f"Friendship between {self.user1} and {self.user2}"

#     def save(self, *args, **kwargs):
#         if self.user1 == self.user2:
#             raise ValueError("A user cannot be friends with themselves.")
#         super().save(*args, **kwargs)

#     class Meta:
#         unique_together = ('user1', 'user2')