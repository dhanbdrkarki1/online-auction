from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/lots/(?P<lot_slug>[-\w]+)/$', consumers.LotConsumer.as_asgi()),
    re_path(r'ws/place-bid/(?P<lot_id>[-\w]+)/$', consumers.BidConsumer.as_asgi()),
]


