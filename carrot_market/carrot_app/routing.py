from django.urls import re_path, path

from . import consumers
from . import ai_consumers

websocket_urlpatterns = [
    re_path(r"ws/chat_index/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    path('ws/ai/', ai_consumers.AiConsumer.as_asgi()),
]