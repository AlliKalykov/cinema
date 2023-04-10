from django.urls import path

# from rest_framework.authtoken import views

from .views import MovieListAPIView, MovieCreateAPIView, MovieRetrieveAPIView, SessionListAPIView, AuthTokenView, RegistrationView

urlpatterns = [
    path('api-token-auth/', AuthTokenView.as_view(), name='api_token_auth'),
    path('registration/', RegistrationView.as_view(), name='registration'),


    path('movie/', MovieListAPIView.as_view(), name='movie'),
    path('movie/create/', MovieCreateAPIView.as_view(), name='movie_create'),
    path('movie/<int:pk>/', MovieRetrieveAPIView.as_view(), name='movie_retrieve'),
    path('session/', SessionListAPIView.as_view(), name='session'),
]
