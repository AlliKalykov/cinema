from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie, Employee


def index(request):
    return HttpResponse("Привет! Моя первая страница!")

def get_movies(request):
    movies = Movie.objects.all()
    print(movies)
    result = ''
    for movie in movies:
        result += f'{movie.name}    {movie.long_time}мин     {movie.start_date} <br><br>'
    return HttpResponse(result)


def get_employee(request):
    emploies = Employee.objects.all()
    print(emploies)
    result = ''
    for emploie in emploies:
        result += f'{emploie.name}    {emploie.surname}    {emploie.patronymic}    {emploie.position.name}    {emploie.password} <br><br>'
    return HttpResponse(result)


# Сделать вьюшки для каждой модели как показано выше
# 
# # 
