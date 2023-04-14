from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from .models import *

from drf_yasg2.utils import swagger_auto_schema


from rest_framework import generics, viewsets, filters, status, views, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly, AllowAny


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
    ordering_fields = ('start_date', 'end_date')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Movie.objects.all()
        # queryset = Movie.objects.filter(start_date__year=year) == MovieFilter.start_year
        return queryset
    
    def get(self, request, *args, **kwargs):
        print(request.user)
        return self.list(request, *args, **kwargs)
    

class MovieCreateAPIView(generics.CreateAPIView):
    serializer_class = MovieSerializers
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = Movie.objects.all()
        return queryset
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)


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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    # filterset_class = SessionFilter

    # def get(self, request, *args, **kwargs):
    #     now = datetime.now()
    #     first_date = now - 14
    #     last_date = now - 7
    #     queryset = Session.objects.filter(start_date__range=(first_date, last_date))
    

class MovingTicketListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MovingTicketSerializers
    queryset = MovingTicket.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


    # переопределить создание записи
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)


class MovingTicketRetrieveAPIView(generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    serializer_class = MovingTicketSerializers
    queryset = MovingTicket.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    # дать возможность только создателю записи ее редактировать
    def update(self, request, *args, **kwargs):
        # берем запись
        instance = self.get_object()
        # проверяем, что пользователь является создателем записи
        if instance.seller == request.user:
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'detail': 'Вы не владелец данной записи'})

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        return super().patch(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def job_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    # view shcem for api job_list
    if request.method == 'GET':
        snippets = Job.objects.all()
        serializer = JobSerializers(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomViewSerializers
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'number']
    ordering_fields = ['name', 'number']

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class EmployeeView(views.APIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = EmployeeSerializers
    queryset = Employee.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    # swagger для api
    @swagger_auto_schema(
        operation_description="Получение списка сотрудников",
        responses={
            200: EmployeeSerializers(many=True),
            400: "Bad request",
        },
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Создание сотрудника",
        responses={
            201: EmployeeSerializers(),
            400: "Bad request",
        },
        request_body=EmployeeSerializers,

    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse
from .forms import MovieForm

class MovieTemplateView(ListView):
    template_name = 'movie/movie.html'
    model = Movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = self.model.objects.all()
        return context
    

class MovieDetailView(DetailView):
    template_name = 'movie/movie_detail.html'
    model = Movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = self.model.objects.get(pk=self.kwargs['pk'])
        return context


class MovieCreateView(CreateView):
    template_name = 'movie/movie_create.html'
    form_class = MovieForm
    success_url = '/movie_detail/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    # redirect to movie_detail
    def get_success_url(self):
        return reverse('movie:movie_detail', kwargs={'pk': self.object.pk})
    
from django.views.generic.edit import UpdateView

class MovieUpdateView(UpdateView):
    model = Movie
    template_name = 'movie/movie_update.html'
