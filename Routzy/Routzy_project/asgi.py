import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from rides.routing import websocket_urlpatterns  # This assumes your routing is in rides.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Routzy_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests as usual
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)  # This will route WebSocket requests to the correct consumer
    ),
})
