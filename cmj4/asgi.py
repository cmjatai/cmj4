import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import django
from django.core.handlers.asgi import ASGIHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmj4.settings")

django.setup()

application = ProtocolTypeRouter({
    'http': ASGIHandler(),
})
