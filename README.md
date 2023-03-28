pip install django

Создать проект
django-admin startproject <projectname>

Создать приложение
Перед создания проекта переходим в папку с проектом (где manage.py)
python manage.py startapp <appname>

Настройка проекта
Настройки проекта находятся в файле settings.py
В файле settings.py в переменной INSTALLED_APPS добавляем приложение
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '<appname>.apps.<AppnameConfig>',
]

Можно изменить язык
LANGUAGE_CODE = 'ru-ru'

Можно изменить часовой пояс
TIME_ZONE = 'Asia/Bishkek'

Можно настроить статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


Можно настроить медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


Пишем модели


После написания моделей необходимо сделать миграцию
python manage.py makemigrations
python manage.py migrate

makemigrations - создает файл миграции, в котором описываются изменения в моделях. Он нужен для того, чтобы не потерять данные при обновлении базы данных. (Можно сказать, что это промежуточный этап между изменением моделей и обновлением базы данных)
migrate - применяет миграции к базе данных (т.е. создает таблицы в базе данных или вносит изменения в существующие таблицы)


Создаем суперпользователя
python manage.py createsuperuser


Скачать библиотеку для работы с postgresql
pip install psycopg2 или pip install psycopg2-binary


Скачиваем либу environ
pip install django-environ

Создаем файл .env в корне проекта
    SECRET_KEY=<secretkey>

    DEBUG=on

    DB=<dbname> # имя базы данных (база должна быть создана)
    DB_USER=<dbuser> # имя пользователя базы данных
    DB_PASSWORD=<dbpassword> # пароль пользователя базы данных
    DB_HOST=127.0.0.1 # хост базы данных (локальный)
    DB_PORT=5432 # порт базы данных (по умолчанию 5432)


Создаем файл .env.example в корне проекта

Прописываем в settings.py
import environ

env = environ.Env()
environ.Env.read_env(env_file='.env')

изменяем SECRET_KEY
    SECRET_KEY = env('SECRET_KEY')

изменяем DEBUG
    DEBUG = env('DEBUG')

изменяем DATABASES
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('DB'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'),
        }
    }


Проводим миграцию, так как в settings.py изменили DATABASES и база данных пустая
    python manage.py migrate

Создаем суперпользователя, так как сменили базу данных
    python manage.py createsuperuser

ПРОВЕРКА
    python manage.py runserver
    
Инициализируем git
    git init

Создаем файл .gitignore в корне проекта
    *.pyc
    __pycache__
    .env
    .idea
    .vscode
    .DS_Store
    .env.example
    *.sqlite3

Дальше создаем репозиторий на github.com и следуем инструкциям там
