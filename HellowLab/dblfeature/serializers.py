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