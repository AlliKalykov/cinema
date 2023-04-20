import os
from celery import Celery
from celery.schedules import crontab

import movie

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')

app = Celery('cinema')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Bishkek'

app.conf.beat_schedule = {
    'add-every-5-seconds': {
        'task': 'movie.tasks.create_random_user_accounts',
        'schedule': crontab(hour=11, minute=[53,54,55,56], day_of_week=4),
        'args': (19, )
    },
}

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, movie.tasks.create_random_user_accounts.s(14), name='add every 10')
