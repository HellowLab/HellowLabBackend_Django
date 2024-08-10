from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import * # import all of my serializers
from .models import * # import all of my models

# update movie result
class MovieResultView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        print("user: ", user)
        serializer = MovieResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)