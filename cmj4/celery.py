import os
from celery import Celery
from celery.utils.log import get_task_logger
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmj4.settings')
app = Celery('cmj4')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


logger = get_task_logger(__name__)

@app.task(queue='celery', bind = True)
def debug_task(self, teste):
    print('teste: ', teste)
