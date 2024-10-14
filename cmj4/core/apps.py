import inspect
from django.apps import AppConfig
from cmj4.celery import debug_task
from django.conf import settings

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'cmj4.core'
    label = 'core'

    def ready(self):
        AppConfig.ready(self)

        # ATENÇÃO:
        # péssimo local para chamar uma task...
        # no método ready ela executará quantas vezes o
        # manage rodar (collectstatic, migrate) ou outros serviços como worker do celery
        # e não falhará na geração da imagem sem os teste abaixo

        for i in inspect.stack():
            try:
                if i.frame.f_locals['subcommand'] in ('migrate', 'collectstatic'):
                    return
            except:
                pass

        debug_task.apply_async(
            args = ('debug task enviado de core.apps.CoreConfig.ready',),
            countdown=5)
