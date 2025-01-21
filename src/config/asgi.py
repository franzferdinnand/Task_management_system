import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import re_path
from tasks.consumers import TaskConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# WebSocket маршрути
websocket_urlpatterns = [
    re_path(r'ws/tasks/(?P<task_id>\d+)/$', TaskConsumer.as_asgi()),
]

# ASGI додаток
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Обробка HTTP-запитів
    "websocket": AllowedHostsOriginValidator(  # Обмеження для WebSocket-з'єднань
        AuthMiddlewareStack(  # Автентифікація для WebSocket
            URLRouter(
                websocket_urlpatterns  # Маршрути для WebSocket
            )
        )
    ),
})
