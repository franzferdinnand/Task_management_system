import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import re_path


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()

# WebSocket routes
def websocket_urlpatterns():
    from tasks.consumers import TaskConsumer
    return [
        re_path(r'ws/tasks/(?P<task_id>\d+)/$', TaskConsumer.as_asgi()),
    ]

# ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns()
            )
        )
    ),
})
