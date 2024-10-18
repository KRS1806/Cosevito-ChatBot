import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from Chat.consumer import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LlamaChat.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/', ChatConsumer.as_asgi()),  # Asegúrate de que esta URL sea la correcta
        ])
    ),
})