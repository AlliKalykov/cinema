from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from .models import *

from rest_framework import generics
from rest_framework import filters

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


from .serializers import *
import django_filters

from .service import CRUD


# auth
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class AuthTokenView(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user'] # django.contrib.auth.models.User
        token, created = Token.objects.get_or_create(user=user)
        return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'name': user.first_name
            }
        )
    

class RegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializers
    
    
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({
                'username': user.username,
                'token': token.key
            }
        )



class MovieFilter(django_filters.FilterSet):
    start_year = django_filters.NumberFilter(field_name='start_date__year')
    class Meta:
        model = Movie
        fields = ('start_year', )


class MovieListAPIView(generics.ListCreateAPIView):
    serializer_class = MovieSerializers
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    search_fields = ('name', 'company')
    filterset_class = MovieFilter

    def get_queryset(self):

        queryset = Movie.objects.all()
        # queryset = Movie.objects.filter(start_date__year=year) == MovieFilter.start_year
        return queryset
    

class MovieCreateAPIView(generics.CreateAPIView):
    serializer_class = MovieSerializers

    def get_queryset(self):
        queryset = Movie.objects.all()
        return queryset


class MovieRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.all()


class MovieRetrieveAPIView(generics.RetrieveAPIView, generics.DestroyAPIView, ):
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.all()


class SessionFilter(django_filters.FilterSet):
    # разделить DateTimeFiled на два поля date и time
    start_date = django_filters.DateTimeFilter(field_name='start_date', lookup_expr='date')

    class Meta:
        model = Session
        fields = ('start_date', )


class SessionListAPIView(generics.ListCreateAPIView):
    serializer_class = SessionSerializers
    queryset = Session.objects.filter(movie__is_active=False)
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    filters = ('start_date', )

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    # filterset_class = SessionFilter

    # def get(self, request, *args, **kwargs):
    #     now = datetime.now()
    #     first_date = now - 14
    #     last_date = now - 7
    #     queryset = Session.objects.filter(start_date__range=(first_date, last_date))
    