from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .serializers import * # import all of my serializers
from .models import * # import all of my models

User = get_user_model()

# update movie result
class MovieResultView(APIView):
    permission_classes = [IsAuthenticated]

    # POST request to add or update a movie result
    def post(self, request):
        # get User ID for the authorized user
        user_id = self.request.user.id
        if not user_id:
            return Response({"error": "userID is required."}, status=status.HTTP_400_BAD_REQUEST)
        # Fetch the user based on the userID using the custom user model
        user = get_object_or_404(User, id=user_id)
        
        tmdb_id = request.data.get('tmdb_id')
        if not tmdb_id:
            return Response({"error": "tmdb_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the MovieResult object exists
        if MovieResult.objects.filter(user=user, tmdb_id=tmdb_id).exists():
            print("Movie already exists")
            # Fetch the movie result based on the movie_result_id
            movie_result = MovieResult.objects.get(user=user, tmdb_id=tmdb_id)

            # Update the movie result with the new data
            serializer = MovieResultSerializer(movie_result, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Serialize the movie result
        serializer = MovieResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        # Extract userID from query parameters, if none is sent then user the authorized users ID
        user_id = request.query_params.get('userID') or self.request.user.id
        if not user_id:
            return Response({"error": "userID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the user based on the userID using the custom user model
        user = get_object_or_404(User, id=user_id)
        
        # Fetch the list of movie results for this user
        movie_list = MovieResult.objects.filter(user=user)
        
        # Serialize the movie results
        serializer = MovieResultSerializer(movie_list, many=True)
        
        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT request to update a movie result
    def put(self, request):
        # Extract the movie result ID from the request data
        movie_result_id = request.data.get('id')

        if not movie_result_id:
            return Response({"error": "id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the movie result based on the movie_result_id
        movie_result = get_object_or_404(MovieResult, id=movie_result_id)
        
        # Update the movie result with the new data
        serializer = MovieResultSerializer(movie_result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# get a single movie result
class SingleMovieView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # get User ID for the authorized user
        user_id =  self.request.user.id
        if not user_id:
            return Response({"error": "userID is required."}, status=status.HTTP_400_BAD_REQUEST)
        # Fetch the user based on the userID using the custom user model
        user = get_object_or_404(User, id=user_id)

        id = request.query_params.get('id')
        tmdb_id = request.query_params.get('tmdb_id')

        if (id):
            movie_result = get_object_or_404(MovieResult, id=id)
        elif (tmdb_id):
            movie_result = get_object_or_404(MovieResult, user=user, tmdb_id=tmdb_id)
        else:
            return Response({"error": "tmdb_id or id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        print("MovieResult: ", movie_result)
        # Serialize the movie results
        try:
            serializer = MovieResultSerializer(movie_result)
        
            # Return the serialized data as a JSON response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Error saving data."}, status=status.HTTP_400_BAD_REQUEST)

