import json
import nest_asyncio
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from ConfLlama.configuration import query
import gc
import httpx

nest_asyncio.apply()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("chat_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat_group", self.channel_name)
        await self.send(text_data=json.dumps({
            'message': 'WebSocket desconectado, recarga la página para conectarse de nuevo',
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Intentar realizar la consulta con timeout
        try:
            result = await asyncio.wait_for(self.run_query(message), timeout=60.0)
        except asyncio.TimeoutError:
            result = "La consulta tardó demasiado en procesarse. Por favor, intenta de nuevo."

        # Enviar la respuesta de vuelta al WebSocket
        await self.send(text_data=json.dumps({
            'response': result,
            'message': message
        }))

        # Liberar memoria
        gc.collect()

    async def run_query(self, message):
        try:
            return query(message)
        except httpx.ReadTimeout:
            # Enviar un mensaje de error al cliente para que el WebSocket no se cierre abruptamente
            await self.send(text_data=json.dumps({
                'message': 'Error: La consulta a la IA tardó demasiado tiempo. Recarga la web e intentalo de nuevo.'
            }))
            return None
