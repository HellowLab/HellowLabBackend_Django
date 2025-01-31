# api/serializers.py

from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model

from .models import *

User = get_user_model()

# Custom Register Serializer
class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    bio = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.save()
        return user

    def to_representation(self, instance):
        """Customize the representation of the newly created user"""
        representation = super().to_representation(instance)
        # representation['profile_picture'] = instance.profile_picture.url if instance.profile_picture else None
        # representation['bio'] = instance.bio
        return representation

# Custom Login Serializer
class CustomLoginSerializer(LoginSerializer):
    profile_picture = serializers.ImageField( required=False)
    bio = serializers.CharField(required=False)

    def validate(self, attrs):
        data = super().validate(attrs)  # Perform the default validation

        user = self.context['request'].user  # Access the user after login

        # Check if the user is authenticated
        if user.is_authenticated:
            data['profile_picture'] = user.profile_picture.url if user.profile_picture else None
            data['bio'] = user.bio
        else:
            # You can choose to exclude custom fields or return default values if user is not authenticated
            data['profile_picture'] = None
            data['bio'] = None

        return data
    
# Custom User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'pk', 'bio', 'profile_picture']
        read_only_fields = ['pk', 'username']  # Prevent these from being updated

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at']

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['id', 'user1', 'user2', 'created_at']
