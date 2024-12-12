# with help from: https://testdriven.io/blog/django-rest-auth/
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
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


# Update friendship status
class FriendshipView(APIView):
    permission_classes = [IsAuthenticated] # user must have a valid bearer token to make this request

    # POST request to add a new friend/request
    def post(self, request):
        print("entered post)")

        # Fetch the user based on the userID using the custom user model
        user2 = get_object_or_404(User, id=request.data.user2)

        serializer = FriendshipSerializer(data=request.data)

        print("serializer processed")
        if serializer.is_valid():
            serializer.save(user1=self.request.user, user2=user2)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user != request.user:
            return Response({"error": "You can't accept this friend request."}, status=status.HTTP_400_BAD_REQUEST)

        instance.accepted = True
        instance.save()

        # Create a Friendship when the request is accepted
        Friendship.objects.create(user1=instance.from_user, user2=instance.to_user)
        return Response(FriendRequestSerializer(instance).data)

class FriendshipViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(user1=user) | Friendship.objects.filter(user2=user)