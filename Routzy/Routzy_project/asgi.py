import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import rides.routing  # Replace with your app's routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Routzy_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                rides.routing.websocket_urlpatterns  # Define your WebSocket routes in rides/routing.py
            )
        )
    ),
})
