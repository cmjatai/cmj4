
from random import random

from celery.utils.log import get_task_logger

from cmj4.celery import app
from cmj4.core.models import Teste


logger = get_task_logger(__name__)



@app.task(queue = 'celery', bind = True)
def debug_task(self):

    teste = Teste()
    teste.teste = str(random())
    teste.save()
    
    logger.info(f'teste cadastrado {teste.id} - {teste.teste}')

    return f'result of teste {teste.id}'
