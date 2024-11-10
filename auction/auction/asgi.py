# Remember to sequence the four key statements in asgi.py while using daphne (even though it works in dev server)
# from django.core.asgi import get_asgi_application
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# django_asgi_app = get_asgi_application()
# from chat.routing import websocket_urlpatterns


import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction.settings')
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import chat.routing
import lot.routing


application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        URLRouter(
            chat.routing.websocket_urlpatterns + lot.routing.websocket_urlpatterns
        )
    ),
})
