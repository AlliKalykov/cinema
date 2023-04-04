from django.urls import path
from .views import MovieListAPIView, MovieCreateAPIView, MovieRetrieveAPIView

urlpatterns = [
    path('movie/', MovieListAPIView.as_view(), name='movie'),
    path('movie/create/', MovieCreateAPIView.as_view(), name='movie_create'),
    path('movie/<int:pk>/', MovieRetrieveAPIView.as_view(), name='movie_retrieve'),
]
