from rest_framework import serializers

from .models import *

# serializer for movie result
class MovieResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieResult
        fields = '__all__'
        read_only_fields = ['user']

class TmdbIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmdbIndex
        fields = '__all__'
        read_only_fields = ['user']

class MovieListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieListItem
        fields = '__all__'

class MovieListSerializer(serializers.ModelSerializer):
    movies = MovieListItemSerializer(many=True, read_only=True)  # Include items in the list

    class Meta:
        model = MovieList
        fields = '__all__'
        read_only_fields = ['user']
