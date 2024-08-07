from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.contrib import admin

from datetime import datetime

### User Models ###
class CustomUser(AbstractUser):
    company = models.CharField(max_length=30, blank = True, null = True)
    profile_image = models.ImageField(blank = True, null = True, upload_to="profile_images/")
    # email = models.CharField(max_length=30) # 
    # username = models.CharField(max_length=30) # 
    
    # Customize the user model by specifying the AUTH_USER_MODEL setting
    class Meta:
        swappable = 'AUTH_USER_MODEL'

# class Company(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255, blank=True)
