import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import django
from django.core.handlers.asgi import ASGIHandler

import cmj4.core.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmj4.settings")

django.setup()

application = ProtocolTypeRouter({
    'http': ASGIHandler(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            cmj4.core.routing.websocket_urlpatterns
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})
