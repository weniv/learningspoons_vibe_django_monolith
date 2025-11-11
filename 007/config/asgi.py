"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from game import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Django ASGI application을 먼저 초기화
django_asgi_app = get_asgi_application()

# ProtocolTypeRouter로 HTTP와 WebSocket 모두 처리
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
