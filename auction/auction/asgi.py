import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import chat.routing
import lot.routing

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns +
            lot.routing.websocket_urlpatterns
        )
    ),
})
