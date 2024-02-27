import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone
# from channels.db import database_sync_to_async
# from asgiref.sync import async_to_sync, sync_to_async

User = get_user_model()

class LotConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({'message': message}))
