from django.apps import AppConfig


class MovieConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie'
    verbose_name = 'Фильм'
    verbose_name_plural = 'Фильмы'
