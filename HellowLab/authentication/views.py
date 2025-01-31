# with help from: https://testdriven.io/blog/django-rest-auth/
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.signing import Signer, BadSignature
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LogoutView, LoginView
from django.views.decorators.http import require_GET
from django.db.models import Q


import json
from .models import *
from .serializers import *
import csv

User = get_user_model()
signer = Signer()

def email_confirm_redirect(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )

#### USER ACCOUNT VIEWS #####

# Custom User Registration View
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        """
        Override the create method to include full user details in the response.
        """
        # Call the default create method
        response = super().create(request, *args, **kwargs)

        return response

# Custom User Login View
class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        # Call the default login behavior (authentication and token generation)
        response = super().post(request, *args, **kwargs)
        # Once the user is authenticated and the token is created, include custom fields
        user = request.user
        user_data = CustomRegisterSerializer(user).data  # Serialize the user object

        # Add the serialized user data to the response
        response_data = response.data
        response_data['user'] = user_data  # Include the full user data in the response

        return Response(response_data)

class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

def csrf_token_view(request):
    csrf_token = csrf.get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the currently authenticated user's data
        user = request.user
        serializer = CustomUserSerializer(user)
        print("UserDetailView serializer.data: ", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        # Update all user data (full update)
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        print("patch request received")
        # Update partial user data
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("serializer is not valid")
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
def delete_account(request):
    if request.method == 'POST':
        # if token exists, process based on user's token
        if request.user.is_authenticated:
            user = request.user
            user.delete()
            return HttpResponse("Your account has been successfully deleted.", status=200)
        else:
            username = request.POST['username']
            email = request.POST['email']

            try:
                # find the user based on the username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # if the user is not found, return an error
                return HttpResponse("User not found.", status=400)

            # Validate that the provided username and email match the user
            if user.username == username and user.email == email:
                user.delete()
                return HttpResponse("Your account has been successfully deleted.", status=200)
            else:
                return HttpResponse("Username and email do not match.", status=400)

    return render(request, 'HellowLab/delete_account.html')

##### END USER ACCOUNT VIEWS #####


##### FREINDSHIP VIEWS #####

@require_GET
def search_users(request):
    query = request.GET.get("q", "")  # Get the search query from request parameters
    if not query:
        return JsonResponse({"error": "Query parameter 'q' is required"}, status=400)
    
    # sort by usernames that start with the query, limit to 10 (obsolete)
    # users = User.objects.filter(username__istartswith=query).order_by("username")[:10]

    # sort by usernames that contain the query, limit to 10, sort by username length
    users = sorted(
        User.objects.filter(username__istartswith=query),
        key=lambda user: len(user.username)
    )[:10]

    # TODO: list the number of shared friends between the authenticated user and the searched for user
    # shared_friends = [Friendship.objects.filter(user1=request.user, user2=user) for user in users]
    # print(shared_friends)

    user_list = [{"id": user.id, "username": user.username, "name": user.get_full_name() , "profile_picture": user.profile_picture.url if user.profile_picture else None} for user in users]  

    return JsonResponse({"users": user_list})

class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, receiver_id):
        sender = request.user
        receiver = get_object_or_404(User, id=receiver_id)

        if sender == receiver:
            return Response({"error": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a request already exists
        existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, status="pending").exists()
        if existing_request:
            return Response({"error": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)

class ListFriendRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get all pending friend requests for the authenticated user as the receiver or sender
        friend_requests = FriendRequest.objects.filter(
            Q(receiver=request.user) | Q(sender=request.user),
            status="pending"
        )
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RespondToFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, request_id, action):

        # allow the sender to rescind the request
        if action == "rescind":
            friend_request = get_object_or_404(FriendRequest, id=request_id, status="pending")
            friend_request.rescind()
            return Response({"message": "Friend request rescinded."}, status=status.HTTP_200_OK)
        
        friend_request = get_object_or_404(FriendRequest, id=request_id, status="pending")

        if action == "accept":
            friend_request.accept()
            return Response({"message": "Friend request accepted."}, status=status.HTTP_200_OK)
        elif action == "reject":
            friend_request.reject()
            return Response({"message": "Friend request rejected."}, status=status.HTTP_200_OK)
        elif action == "rescind":
            friend_request.rescind()
            return Response({"message": "Friend request rescinded."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)


class ListFriendsView(generics.ListAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(user1=user) | Friendship.objects.filter(user2=user)

# remove a friends
class RemoveFriendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, friend_id):
        user = request.user
        friend = get_object_or_404(User, id=friend_id)

        # Check if the friendship exists
        friendship = Friendship.objects.filter(
            (Q(user1=user) & Q(user2=friend)) | (Q(user1=friend) & Q(user2=user))
        ).first()

        if not friendship:
            return Response({"error": "Friendship does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        friendship.delete()
        return Response({"message": "Friend removed."}, status=status.HTTP_200_OK)

# Update friendship status
# class FriendshipView(APIView):
#     permission_classes = [IsAuthenticated] # user must have a valid bearer token to make this request

#     # POST request to add a new friend/request
#     def post(self, request):
#         print("entered post)")

#         # Fetch the user based on the userID using the custom user model
#         user2 = get_object_or_404(User, id=request.data.user2)

#         serializer = FriendshipSerializer(data=request.data)

#         print("serializer processed")
#         if serializer.is_valid():
#             serializer.save(user1=self.request.user, user2=user2)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class FriendRequestViewSet(viewsets.ModelViewSet):
#     serializer_class = FriendRequestSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return FriendRequest.objects.filter(to_user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(from_user=self.request.user)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance.to_user != request.user:
#             return Response({"error": "You can't accept this friend request."}, status=status.HTTP_400_BAD_REQUEST)

#         instance.accepted = True
#         instance.save()

#         # Create a Friendship when the request is accepted
#         Friendship.objects.create(user1=instance.from_user, user2=instance.to_user)
#         return Response(FriendRequestSerializer(instance).data)

# class FriendshipViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = FriendshipSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Friendship.objects.filter(user1=user) | Friendship.objects.filter(user2=user)