from django.urls import path
from . import views

urlpatterns = [
    path('firsturl/', view=views.index, name='index'),
    path('movies/', view=views.get_movies, name='movies'),
    path('emploies/', view=views.get_employee, name='emploies'),
]