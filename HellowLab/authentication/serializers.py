# api/serializers.py

from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

from .models import *

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.save()
        return user
class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active',)

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'pk']
        read_only_fields = ['pk', 'username']  # Prevent these from being updated


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source='from_user.username')
    to_user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'timestamp', 'accepted']

    def validate(self, attrs):
        request = self.context.get('request')
        to_user = attrs.get('to_user')
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            raise serializers.ValidationError("Friend request already sent.")
        if Friendship.objects.filter(user1=request.user, user2=to_user).exists() or Friendship.objects.filter(user1=to_user, user2=request.user).exists():
            raise serializers.ValidationError("You are already friends with this user.")
        return attrs

class FriendshipSerializer(serializers.ModelSerializer):
    user1 = serializers.ReadOnlyField(source='user1.username')
    # user2 = serializers.ReadOnlyField(source='user2.username')

    class Meta:
        model = Friendship
        fields = '__all__'
        # read_only_fields = ['user1', 'user2']
