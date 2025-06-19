"""
ASGI config for hackathonproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
# Djangoでasgi使うためのアプリケーションオブジェクトを使うためにインポート
from django.core.asgi import get_asgi_application

# どの設定ファイルを使えばいいか指定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackathonproject.settings')

# 本来はapplication = get_asgi_application()だけで動くが、
# 今回はchannelsを使うため、django_asgi_appというアプリを作ってしまう
# application = get_asgi_application()
django_asgi_app = get_asgi_application()

# channelsの部品で、httpとかwebsocketとかを判断して処理を分けるものをインポート
from channels.routing import ProtocolTypeRouter

# WebSocketのURLをrouting.pyに書いたwebsocket_urlpatternsにルーティングしてくれる
from channels.routing import URLRouter
# WebSocket通信でもDjangoのユーザー認証情報(request.user)を使えるよにしてくれるミドルウェア
from channels.auth import AuthMiddlewareStack
import debateapp.routing

# 文字通りプロトコルのタイプでルーティングを変更する
# applicationの記述でasgiの通信をどうしていくか決定するようだ
application = ProtocolTypeRouter({
    # httpリクエストはdjango_asgi_appに任せる
    'http':django_asgi_app,
    # websocket通信はrouting.pyに書いたurlパターンに回される
    'websocket':AuthMiddlewareStack(URLRouter(debateapp.routing.websocket_urlpatterns)),
})
