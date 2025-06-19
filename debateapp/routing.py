# routing.pyはWebSocket用のURLルーティングを設定するファイル
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/debate/<int:pk>', consumers.DebateConsumer.as_asgi()),
]
