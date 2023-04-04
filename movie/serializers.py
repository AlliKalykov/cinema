from rest_framework import serializers

from .models import  *


class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'name', 'start_date', 'end_date', 'company')

class MovieSessionSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField()  # == CharField(source='room.name')
    class Meta:
        model = Session
        fields = ['id', 'room', 'start_date']


class MovieDetailSerializer(serializers.ModelSerializer):
    movie_session = MovieSessionSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'start_date', 'end_date', 'company', 'movie_session')