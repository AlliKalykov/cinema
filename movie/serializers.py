

from rest_framework import serializers

from .models import  *


class UserRegistrationSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        return data


class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'long_time', 'name', 'start_date', 'end_date', 'company')

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('Дата начала фильма не может быть больше даты конца')
        return data


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


class SessionSerializers(serializers.ModelSerializer):
    # movie = serializers.StringRelatedField() # == CharField(source='movie.is_active')
    # room = serializers.StringRelatedField()
    class Meta:
        model = Session
        fields = ('id', 'room', 'start_date', 'movie')


class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'sector')


class MovingTicketSerializers(serializers.ModelSerializer):
    class Meta:
        model = MovingTicket
        fields = ('id', 'ticket', 'operation', 'created_at', )
        read_only_fields = ('id', 'created_at',)


class JobSerializers(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RoomViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'capacity', 'description', 'row_count', 'seat_count')
        read_only_fields = ('id',)


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name', 'surname', 'patronymic', 'position', 'password')
        read_only_fields = ('id',)