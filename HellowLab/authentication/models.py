from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from datetime import datetime

### User Models ###
class CustomUser(AbstractUser):
    company = models.CharField(max_length=30, blank = True, null = True)
    profile_image = models.ImageField(blank = True, null = True, upload_to="profile_images/")
    
    # Customize the user model by specifying the AUTH_USER_MODEL setting
    class Meta:
        swappable = 'AUTH_USER_MODEL'

class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_friend_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Friend request from {self.from_user} to {self.to_user}"

class Friendship(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    ]

    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendship1', on_delete=models.CASCADE) # user who initiated friend request
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendship2', on_delete=models.CASCADE) # user who recieved friend request
    # status = models.Choices(["pending", "accepted", "rejected"])
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    friends_since = models.DateTimeField(default=timezone.now) # date of friend request of pending/rejected, date of friendship start if accepted

    def __str__(self):
        return f"Friendship between {self.user1} and {self.user2}"

    def save(self, *args, **kwargs):
        if self.user1 == self.user2:
            raise ValueError("A user cannot be friends with themselves.")
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('user1', 'user2')