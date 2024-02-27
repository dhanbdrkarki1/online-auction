from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/lots/(?P<slug>[-\w]+)/$', consumers.LotConsumer.as_asgi()),

]