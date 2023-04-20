from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework import routers

# from rest_framework.authtoken import views

from .views import MovieListAPIView, MovieCreateAPIView, MovieRetrieveAPIView, SessionListAPIView, AuthTokenView, RegistrationView, MovingTicketListCreateAPIView, MovingTicketRetrieveAPIView, job_list, RoomViewSet, EmployeeView, MovieTemplateView, MovieDetailView, MovieCreateView, GenerateRandomUserView

# router

router = routers.DefaultRouter()
router.register(r'room', RoomViewSet, basename='movie')
# router.register(r'Session', SessionViewSet, basename='session')
# router.register(r'MovingTicket', MovingTicketViewSet, basename='moving_ticket')

app_name = 'movie'

urlpatterns = [
    path('users_list/', GenerateRandomUserView.as_view(), name='users_list'),
    path('api/', include(router.urls)),

    path('api-token-auth/', AuthTokenView.as_view(), name='api_token_auth'),
    path('registration/', RegistrationView.as_view(), name='registration'),


    path('movie/', MovieListAPIView.as_view(), name='movie'),
    path('movie/create/', MovieCreateAPIView.as_view(), name='movie_create'),
    path('movie/<int:pk>/', MovieRetrieveAPIView.as_view(), name='movie_retrieve'),
    path('session/', SessionListAPIView.as_view(), name='session'),
    path('moving_ticket/', MovingTicketListCreateAPIView.as_view(), name='moving_ticket'),
    path('moving_ticket/<int:pk>/', MovingTicketRetrieveAPIView.as_view(), name='moving_ticket_retrieve'),
    path('jobdef/', job_list, name='job'),
    path('employee/', EmployeeView.as_view(), name='employee'),
    path('movie_template/', MovieTemplateView.as_view(), name='movie_template'),
    path('movie_detail/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movie_create/', MovieCreateView.as_view(), name='movie_create'),
    path('', TemplateView.as_view(template_name='base.html'), name='base')
]
