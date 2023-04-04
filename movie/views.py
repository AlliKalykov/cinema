from django.shortcuts import render
from django.http import HttpResponse
from .models import *

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework import filters
from .serializers import *
import django_filters


class MovieFilter(django_filters.FilterSet):
    start_year = django_filters.NumberFilter(field_name='start_date__year')
    class Meta:
        model = Movie
        fields = ('start_year', )


class MovieListAPIView(ListAPIView):
    serializer_class = MovieSerializers
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    search_fields = ('name', 'company')
    filterset_class = MovieFilter

    def get_queryset(self):

        queryset = Movie.objects.all()
        # queryset = Movie.objects.filter(start_date__year=year) == MovieFilter.start_year
        return queryset
    

class MovieCreateAPIView(CreateAPIView):
    serializer_class = MovieSerializers

    def get_queryset(self):
        queryset = Movie.objects.all()
        return queryset


class MovieRetrieveAPIView(RetrieveAPIView):
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.all()
