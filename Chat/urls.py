from django.urls import path
from .views import *
from .consumer import *

urlpatterns = [
    path('', ChatView.as_view(), name='Home'),
]

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi()),  # Asegúrate de que esta URL sea la correcta
]