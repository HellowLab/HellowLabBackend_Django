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
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json
from .models import *
from .serializers import *
import csv

def email_confirm_redirect(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )

#### USER ACCOUNT VIEWS #####
class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print("recieved register user POST")
        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # We create a token than will be used for future auth
            token = Token.objects.create(user=serializer.instance)
            token_data = {"token": token.key}
        return Response(
                {**serializer.data, **token_data},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

def csrf_token_view(request):
    csrf_token = csrf.get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_data(request):
    user = request.user
    data = request.data

    print("update_user_data data: ", data)

    if data:
        if 'profile_image' in request.FILES:
            print("profile_image in request.FILES")
            # Update user's profile image
            user.profile_image = request.FILES['profile_image']
            user.save()
        
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # try:
        #     for field, value in data.items():
        #         if hasattr(user, field):
        #             setattr(user, field, value)
        #         else:
        #             return Response({'error': f'Field {field} does not exist'}, status=400)
        #     user.save()
        #     myuser = CustomUserSerializer(user).data            
        #     return Response(myuser)

        # except Exception as e:
        #     return Response({'error': str(e)}, status=500)
    else:
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No data provided'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_user(request):
    myuser = request.user
    myuser = CustomUserSerializer(myuser).data    
    return Response(myuser)

#### END USER ACCOUNT VIEWS #####