import json
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync, sync_to_async
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, ChatRoom

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_user_id = self.scope['url_route']['kwargs']['other_user_id']
        self.room_group_name = f'chat_{self.other_user_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender = self.user.username
        message = text_data_json['message']
        await self.save_message(message)

        full_name = await self.get_user_full_name(username=sender)
        
        # send message to WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type': 'chat_message',
            'message': message,
            'sender': sender,
            'fullName': full_name,
            'datetime': timezone.now().isoformat(),
            }
        )

    # receive message from room group
    async def chat_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_user(self, user_id):
        user = User.objects.get(id=user_id)
        return user
    
    @sync_to_async
    def get_user_full_name(self, username):
        full_name = User.objects.get(username=username).get_user_full_name()
        print("----------------------", full_name)

        return full_name

    @sync_to_async
    def save_message(self, message):
        sender = self.user
        receiver = User.objects.get(id=self.other_user_id)
        # Assuming there is only one chat room between two users
        room = ChatRoom.objects.filter(members__in=[sender, receiver]).first()
        if not room:
            room = ChatRoom.objects.create(name=f"Chat between {sender.username} and {receiver.username}")
            room.members.add(sender, receiver)
        Message.objects.create(room=room, sender=sender, message=message)

